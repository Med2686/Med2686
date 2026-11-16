"""The reading pack: everything you need to understand each phrase and decide, on one page.

  python -I reading_pack.py -p <project> [--seed 0.4]

Merges, per speech region (work/regions.json):
  - the region transcripts in AR (Derja prompt; often translated to MSA, read for gist), FR, EN
    (tx-regions.json from transcribe.py --regions),
  - the structural flags inside it (bursts-regions.json from bursts.py --regions, if run),
  - loudness: duration, gap before / after, the 20 ms strip (# speech, + soft, . quiet),
  - gaze: frames looking at the screen side (gaze-raw.json, if made) -> READING? while talking,
  - cross-region leads: RETAKE (this region's words open the next one: he restarted), SIMILAR (same idea
    said again: keep the last unless the first adds meaning), REPEAT / REOPEN / FILLER inside it,
    NON-SPEECH (every pass empty or hallucinated: breath, noise, mouth click).
Then YOU write, per region, what he meant in Derja (arabizi like the keep list: 7=ح 3=ع 9=ق 5=خ ch=ش),
and the decision. Out: work/reading-pack.md
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, db_strip, filler_hits, find_repeats, is_prefix_take,  # noqa: E402
                        load_audio, norm_tokens, read_json, reopen_hits, similar, strip_text, thresholds_from)

HEAD = """# Reading pack: {name}

How to read: per region, AR is often Modern Standard Arabic (Whisper TRANSLATES Derja); trust it for the
gist only. FR gets the French words right and phonetises Derja (« ena kinshuv » = « ena ki nchouf »).
EN is the best proxy for repeats. Empty = non-speech (hallucination filtered).
Strip: one char per 20 ms, # above T_high, + above T_low, . quiet.
For each region write: **meant:** the Derja sentence in arabizi, **decision:** KEEP / CUT (why) /
KEEP FROM t / CUT t1-t2 inside / FLAG (unclear). The findings list for the user comes from these lines.
"""


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--seed", type=float, default=None)
    a = ap.parse_args()
    P = Project(a.project)
    W = P.work
    reg = read_json(W / "regions.json")
    tx = {r["i"]: r for r in read_json(W / "tx-regions.json")} if (W / "tx-regions.json").exists() else {}
    bj = read_json(W / "bursts-regions.json") if (W / "bursts-regions.json").exists() else None
    G = read_json(W / "gaze-raw.json") if (W / "gaze-raw.json").exists() else None
    y = load_audio(P.mic16())
    db = db_strip(y)
    ref, hi, lo = thresholds_from(db)
    seed = a.seed if a.seed is not None else float(P.cfg.get("gaze_seed", 0.4))
    S = None
    if G:
        ix = {k: i for i, k in enumerate(G["cols"])}
        ko, ki = ("eyeLookOutRight", "eyeLookInLeft") if P.cfg.get("screen_side", "left") == "left" else ("eyeLookOutLeft", "eyeLookInRight")
        S = np.array([0.0 if r[1] is None else (r[ix[ko]] + r[ix[ki]]) / 2 for r in G["rows"]])
    fps, off, rate = int(P["fps"]), float(P["offset"]), float(P.cfg.get("rate", 1.0))
    langs = ["ar", "fr", "en"]
    toks = {i: {l: norm_tokens(tx.get(i, {}).get(l, "")) for l in langs} for i in range(1, len(reg) + 1)}
    md = [HEAD.format(name=P.root.name), f"T_high {hi:.1f} dB, T_low {lo:.1f} dB, offset {off} s\n"]
    for i, (s, e) in enumerate(reg, 1):
        r = tx.get(i, {})
        gap_b = s - reg[i - 2][1] if i > 1 else s
        gap_a = reg[i][0] - e if i < len(reg) else 0
        leads = []
        if not any(r.get(l) for l in langs) and r:
            leads.append("NON-SPEECH? (all passes empty)")
        for l in ("en", "fr"):
            t = toks[i][l]
            for kind, n, x, z, ph in find_repeats(t):
                leads.append(f"{kind.upper()} {l} « {ph} »")
            leads += [f"{h} ({l})" for h in reopen_hits(t) + filler_hits(t)]
            for j in (i + 1, i + 2):
                if j in toks and t:
                    nt = toks[j][l]
                    if is_prefix_take(t[: max(1, min(len(t), 4))], nt) and len(t) <= len(nt):
                        leads.append(f"RETAKE? {l}: region #{j} opens with the same words -> keep #{j} (the last take)")
                        break
                    sm = similar(t, nt)
                    if sm >= 0.5:
                        leads.append(f"SIMILAR {l} {sm:.2f} to #{j}: same idea again? keep the last unless this adds meaning")
                        break
        if S is not None:
            f0, f1 = int(round((s * rate + off) * fps)), int(round((e * rate + off) * fps))
            seg = S[max(0, f0):max(0, min(len(S), f1))]
            nlook = int((seg > seed).sum()) if len(seg) else 0
            if nlook >= 10:
                leads.append(f"READING? {nlook} frames look at the screen while talking (max {seg.max():.2f}) -> COVER, check the frames")
        if bj:
            for sp in bj["spans"]:
                if abs(sp["a"] - s) < 0.05:
                    for b in sp["boundaries"]:
                        if b["score"] >= 2:
                            leads.append(f"BURST {b['t']:.2f} score {b['score']}: {'; '.join(b['why'])}")
        md.append(f"## #{i}  {s:.2f}-{e:.2f}  ({e - s:.2f} s, gap before {gap_b:.2f}, after {gap_a:.2f})")
        md.append("```")
        md.append("strip " + strip_text(db, s, e, lo, hi))
        for l in langs:
            md.append(f"{l.upper()}: {r.get(l) or '(nothing)'}")
        md.append("```")
        md += [f"- lead: {x}" for x in dict.fromkeys(leads)]
        md.append("- **meant:** \n- **decision:** \n")
    (W / "reading-pack.md").write_text("\n".join(md), encoding="utf8")
    print(f"{len(reg)} regions -> {W / 'reading-pack.md'}")


if __name__ == "__main__":
    main()
