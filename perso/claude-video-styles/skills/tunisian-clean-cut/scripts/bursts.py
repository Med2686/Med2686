"""Structural false-start / repeat detector: the pass that finds what whole-line transcripts hide.

  python -I bursts.py -p <project> --keep            # every line of work/keep.json   (after a draft keep list)
  python -I bursts.py -p <project> --regions         # every region of work/regions.json (raw, before deciding)
  python -I bursts.py -p <project> 237.9-241.0 ...   # explicit spans (mic seconds)
         [--langs en,fr] [--echo-gate 0.8] [--out name]

Whisper on a whole line tidies repeats: « ou la cap… ou la capacité de juger » comes back as one clean
phrase, « learn, learn how to » as « learn how to ». So inside each span:
  1. find every boundary where a take can restart: gaps (>= 60 ms under T_low) AND notches (a 20-30 ms
     valley >= 18 dB deep that reaches T_low; the false start is often glued to the retake);
  2. at each boundary, transcribe the chunk just before it ALONE, the chunk after it ALONE, and both
     TOGETHER (en + fr, 0.25 s zero padding, no context);
  3. score the evidence:
       PAIR-REPEAT  the pair transcript holds a repeated n-gram (« learn learn how to »)          +3
       PREFIX       the left chunk's words are the opening of the right chunk (« so don't | so don't just »)  +3
       SOUNDS-LIKE  the left text, letter by letter, is like the start of the right text (« oulika » ~ « oulacapa ») +2
       ECHO         MFCC/DTW: the left chunk SOUNDS like the start of the right one (z >= 2: +2, >= 1.2: +1)
       TIDY         the pair has fewer words than left + right: Whisper merged something         +1
  "!!" = score >= 3 with text evidence (or >= 4): very likely a false start, keep from the boundary;
  "! " = score >= 2 or acoustic-only evidence: check it with listen.py. Parallel phrasing (« nchoufou X,
  nchoufou Y ») also lights PAIR-REPEAT: that is content, judge from the meaning.
Every flag is a lead for YOU to judge with listen.py and the meaning of the line, never an automatic cut.

Out: work/<out>.json and work/<out>.txt (default out = bursts-keep / bursts-regions / bursts-spans).
Speed on the RTX 1000 Ada: ~1.5-3 s per Whisper call, ~6 calls per boundary -> run it in the background.
"""
import argparse
import os
import sys
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, boundaries_in, db_strip, echo_z, find_repeats,  # noqa: E402
                        is_prefix_take, load_audio, norm_tokens, read_json, slice_of, speech_edges,
                        thresholds_from, transcribe, write_json)

_CACHE = {}


def tx(y, a, b, lang):
    key = (round(a, 2), round(b, 2), lang)
    if key not in _CACHE:
        _CACHE[key] = transcribe(slice_of(y, a, b), lang, a, pad=0.25, words=False)[0]
    return _CACHE[key]


def sounds_like(L, R):
    jl, jr = "".join(L), "".join(R)
    if len(jl) < 4 or len(jr) < 4:
        return 0.0
    return round(SequenceMatcher(None, jl, jr[: len(jl)]).ratio(), 2)


def analyse_span(y, db, hi, lo, a, b, langs, echo_gate=None, label=""):
    s0, s1 = speech_edges(db, a, b, lo)
    bnds = [x for x in boundaries_in(db, s0, s1, hi, lo) if s0 + 0.12 < x[0] < s1 - 0.12]
    edges = [s0] + [t for t, _, _ in bnds] + [s1]
    res = {"a": a, "b": b, "s0": s0, "s1": s1, "label": label, "boundaries": []}
    for t, kind, depth in bnds:
        prev = [e for e in edges if e <= t - 0.25]
        la = max(prev) if prev else s0
        la = max(la, round(t - 1.2, 2))
        nxt = [e for e in edges if e >= t + 0.8]
        rb = min(min(nxt) if nxt else s1, round(t + 2.0, 2), s1)
        if rb - t < 0.2 or t - la < 0.1:
            continue
        ez = echo_z(y, la, t, s0, s1)
        row = {"t": t, "kind": kind, "depth": depth, "left": [la, t], "right": [t, rb], "echo": ez, "tx": {}, "why": []}
        score = 2 if ez >= 2 else 1 if ez >= 1.2 else 0
        if ez >= 1.2:
            row["why"].append(f"ECHO z{ez:+.1f}")
        if echo_gate is None or ez >= echo_gate or kind == "gap":
            best = {"rep": 0, "pre": 0, "snd": 0, "tidy": 0}
            for lang in langs:
                L, R, P = tx(y, la, t, lang), tx(y, t, rb, lang), tx(y, la, rb, lang)
                row["tx"][lang] = {"left": L, "right": R, "pair": P}
                Lt, Rt, Pt = norm_tokens(L), norm_tokens(R), norm_tokens(P)
                reps = [h for h in find_repeats(Pt) if h[0] == "repeat"]
                if reps:
                    best["rep"] = 3
                    row["why"].append(f"PAIR-REPEAT {lang} « {reps[0][4]} »")
                for m in range(min(4, len(Lt)), 0, -1):
                    tail = Lt[-m:]
                    if sum(len(w) for w in tail) >= 3 and is_prefix_take(tail, Rt):
                        best["pre"] = 3
                        row["why"].append(f"PREFIX {lang} « {' '.join(tail)} » | « {' '.join(Rt[:m + 2])} »")
                        break
                sl = sounds_like(Lt, Rt)
                if sl >= 0.6:
                    best["snd"] = 2
                    row["why"].append(f"SOUNDS-LIKE {lang} {sl:.2f}")
                if Lt and Rt and len(Pt) + 1 < len(Lt) + len(Rt):
                    best["tidy"] = 1
                    row["why"].append(f"TIDY {lang} {len(Lt)}+{len(Rt)}->{len(Pt)} words")
            score += sum(best.values())
            row["text_evidence"] = bool(best["rep"] or best["pre"] or best["snd"])
        # acoustic-only evidence (ECHO + TIDY) stays a "! " lead: it fires on parallel phrasing too
        row["score"] = score if row.get("text_evidence") or score < 3 else min(score, 3)
        row["strong"] = score >= 3 and (row.get("text_evidence") or score >= 4)
        res["boundaries"].append(row)
    return res


def fmt(res):
    out = [f"=== [{res['a']:.2f}-{res['b']:.2f}] speech {res['s0']:.2f}-{res['s1']:.2f}  {res['label']}"]
    for r in res["boundaries"]:
        tag = "!!" if r.get("strong") else "! " if r["score"] >= 2 else "  "
        head = f" {tag} {r['t']:7.2f} {r['kind']:5} {r['depth']:3.0f}dB echo {r['echo']:+.1f} score {r['score']}"
        if r.get("strong"):
            head += f"  -> FALSE START? cut {r['left'][0]:.2f}-{r['t']:.2f}, keep from {r['t']:.2f} (check it)"
        out.append(head + ("  [" + "; ".join(r["why"]) + "]" if r["why"] else ""))
        if r["score"] >= 2 or not r["tx"]:
            for lang, d in r["tx"].items():
                out.append(f"        {lang} left  {r['left'][0]:.2f}-{r['left'][1]:.2f}: {d['left']}")
                out.append(f"        {lang} right {r['right'][0]:.2f}-{r['right'][1]:.2f}: {d['right']}")
                out.append(f"        {lang} pair : {d['pair']}")
    # clusters: a stutter often lights up 2-3 neighbouring boundaries (« so | don't | so don't just… »).
    # The take to keep starts at the LAST flagged boundary of the cluster, if the proof slice holds the phrase.
    fl = [r for r in res["boundaries"] if r["score"] >= 2]
    groups, cur = [], []
    for r in fl:
        if cur and r["t"] - cur[-1]["t"] > 0.6:
            groups.append(cur)
            cur = []
        cur.append(r)
    if cur:
        groups.append(cur)
    for g in groups:
        if len(g) > 1:
            out.append(f"   CLUSTER {g[0]['t']:.2f}..{g[-1]['t']:.2f}: the retake most likely starts at the LAST one "
                       f"({g[-1]['t']:.2f}). Prove it: listen.py {g[-1]['t']:.2f}-{res['s1']:.2f} must hold the whole phrase.")
    return "\n".join(out)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("spans", nargs="*")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--regions", action="store_true")
    ap.add_argument("--audio")
    ap.add_argument("--langs", default="en,fr")
    ap.add_argument("--echo-gate", type=float, default=None,
                    help="only transcribe notches whose echo z >= this (faster, may miss); gaps always")
    ap.add_argument("--out")
    a = ap.parse_args()
    P = Project(a.project)
    y = load_audio(a.audio or P.mic16())
    db = db_strip(y)
    spans = []
    if a.keep:
        from build_clean import load_keep
        spans = [(k["a"], k["b"], f"keep #{i + 1} « {k['text']} »") for i, k in enumerate(load_keep(P.work / "keep.json"))]
        name = "bursts-keep"
    elif a.regions:
        spans = [(r[0], r[1], f"region #{i + 1}") for i, r in enumerate(read_json(P.work / "regions.json"))]
        name = "bursts-regions"
    else:
        spans = [(*map(float, s.split("-")), "") for s in a.spans]
        name = "bursts-spans"
    name = a.out or name
    ref, hi, lo = thresholds_from(db, [(s, e) for s, e, _ in spans] if a.keep else None)
    langs = a.langs.split(",")
    allres = []
    txt = open(P.work / f"{name}.txt", "w", encoding="utf8")
    txt.write(f"ref {ref:.1f} dB  T_high {hi:.1f}  T_low {lo:.1f}\n")
    for s, e, label in spans:
        r = analyse_span(y, db, hi, lo, s, e, langs, a.echo_gate, label)
        allres.append(r)
        block = fmt(r)
        print(block, flush=True)
        txt.write(block + "\n")
        txt.flush()
    txt.close()
    write_json(P.work / f"{name}.json", {"ref": ref, "hi": hi, "lo": lo, "spans": allres})
    flagged = [(r["label"], b["t"], b["score"]) for r in allres for b in r["boundaries"] if b["score"] >= 2]
    print(f"\n{len(flagged)} boundaries flagged (score >= 2) -> {P.work / (name + '.txt')}")


if __name__ == "__main__":
    main()
