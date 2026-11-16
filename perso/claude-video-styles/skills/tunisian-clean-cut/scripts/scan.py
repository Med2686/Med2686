"""Repeat / restart / filler scanner on every kept line (raw mic), in en + fr + ar, with fuzzy n-grams.

  python -I scan.py -p <project> [--keep work/keep.json] [--langs en,fr,ar] [--no-verbatim] [--lines 34,47]

Per kept line (cut sub-spans removed, i.e. what the viewer will hear):
  - the line transcribed alone (0.25 s zero padding) in each language, plus en/fr with a disfluent prompt;
  - REPEAT / RESTART: fuzzy n-grams up to 6 words said twice (« ça reflète ce que tu fais, ça reflète ce que
    tu fais »; « ou la cap ou la capacité »; « learn learn »), spelling normalised (accents, alef/ta marbuta,
    the Arabic article), truncated words match their full form;
  - REOPEN: the opening said twice with words between (« ena personnellement, donc ena, ki nchouf »);
  - OPENER / TRAILING / FILLER: tics from the lexicon (ena personnellement, donc, ok, d'accord, fhemt, ya3ni,
    euh, et cetera, a trailing wala …);
  - SIMILAR-NEXT: this line and the next say nearly the same thing (a reformulated duplicate: keep the last,
    unless the second adds meaning).
A whole-line transcript TIDIES repeats, so a clean scan proves nothing on its own: bursts.py is the
structural pass, this is the lexical one. Read both, then decide from the meaning.
Out: work/scan.txt + work/scan.json
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (VERBATIM, Project, add_project_arg, filler_hits, find_repeats, load_audio,  # noqa: E402
                        norm_tokens, reopen_hits, similar, slice_of, transcribe, whisper_loop, write_json)


def kept_audio(y, k):
    """The line as it will be heard: [a,b] minus its `cut` sub-spans."""
    parts, t = [], k["a"]
    for x, z in sorted(k["cut"]):
        parts.append(slice_of(y, t, x))
        t = z
    parts.append(slice_of(y, t, k["b"]))
    return np.concatenate(parts)


def analyse_texts(texts: dict) -> list[str]:
    flags = []
    for key, text in texts.items():
        toks = norm_tokens(text)
        if whisper_loop(toks):
            flags.append(f"({key} pass looped: ignored)")
            continue
        for kind, n, i, j, ph in find_repeats(toks):
            flags.append(f"{kind.upper()} {key} « {ph} » x2")
        if key.endswith("plain"):
            flags += [f"{h} ({key})" for h in reopen_hits(toks) + filler_hits(toks)]
    # same flag from several passes counts once
    seen, out = set(), []
    for f in flags:
        k = (f.split(" ")[0], f.split("«")[1].split("»")[0].strip() if "«" in f else f)
        if k not in seen:
            seen.add(k)
            out.append(f)
    return out


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--keep")
    ap.add_argument("--langs", default="en,fr,ar")
    ap.add_argument("--no-verbatim", action="store_true")
    ap.add_argument("--lines", help="only these line numbers (1-based), e.g. 34,47")
    ap.add_argument("--audio")
    a = ap.parse_args()
    P = Project(a.project)
    from build_clean import load_keep
    keep = load_keep(a.keep or P.work / "keep.json")
    only = {int(x) for x in a.lines.split(",")} if a.lines else None
    y = load_audio(a.audio or P.mic16())
    langs = a.langs.split(",")
    rows = []
    txt = open(P.work / "scan.txt", "w", encoding="utf8")
    for li, k in enumerate(keep, 1):
        if only and li not in only:
            continue
        seg = kept_audio(y, k)
        texts = {}
        for lang in langs:
            texts[f"{lang}-plain"] = transcribe(seg, lang, k["a"], words=False)[0]
            if not a.no_verbatim and VERBATIM.get(lang):
                texts[f"{lang}-verb"] = transcribe(seg, lang, k["a"], prompt=VERBATIM[lang], words=False)[0]
        rows.append({"line": li, "a": k["a"], "b": k["b"], "text": k["text"], "tx": texts, "flags": analyse_texts(texts)})
    # neighbour similarity on the en pass (a reformulated duplicate across a cut)
    for r, n in zip(rows, rows[1:]):
        if n["line"] != r["line"] + 1:
            continue
        s = max(similar(norm_tokens(r["tx"].get(f"{l}-plain", "")), norm_tokens(n["tx"].get(f"{l}-plain", ""))) for l in langs)
        if s >= 0.5:
            r["flags"].append(f"SIMILAR-NEXT {s:.2f}: same idea as line #{n['line']}? keep the LAST unless the 1st adds meaning")
    for r in rows:
        tag = "!!" if r["flags"] else "  "
        block = [f"{tag} #{r['line']:3} [{r['a']:.2f}-{r['b']:.2f}] {r['text']}"]
        block += [f"       {k:9}: {v}" for k, v in r["tx"].items()]
        block += [f"       -> {f}" for f in r["flags"]]
        s = "\n".join(block)
        print(s, flush=True)
        txt.write(s + "\n")
    txt.close()
    write_json(P.work / "scan.json", rows)
    print(f"\n{sum(bool(r['flags']) for r in rows)} of {len(rows)} lines flagged -> {P.work / 'scan.txt'}")


if __name__ == "__main__":
    main()
