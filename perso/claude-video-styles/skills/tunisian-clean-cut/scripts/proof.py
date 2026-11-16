"""Proof slices for every cut decision in keep.json: never clip a word, never lose the phrase.

  python -I proof.py -p <project> [--keep work/keep.json] [--lines 34,47] [--langs en,fr]

For each kept line:
  START  transcribe from the line start (and from every `cut` end inside it) to the line end, as it will be
         heard. The whole intended phrase must be there: if the first word is missing or mangled, the start
         is too late (or inside the word); if a stutter is still there, it is too early.
  END    [b-1.3, b] vs [b-1.3, b+0.45]. If the longer slice ends on a fuller form of the last word
         (« tekh » -> « tekhdem », « -si » -> « -sion »), the end clips the word: move b to the next dip.
         French nasal endings: the « s » of « -tion » is not the end, the voiced « on » is.
  BOUND  every bound (a, b, both edges of each cut) must sit in a dip: level under T_low+6 dB and no frame
         above T_high in the 80 ms on the removed side. Otherwise it is inside a sound.
Cut points come from the 10 ms strip (listen.py --strip), not from Whisper word times (+-0.2 s, the
first word is pinned to the slice start). Out: work/proof.txt
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, db_strip, load_audio, norm_tokens, slice_of,  # noqa: E402
                        thresholds_from, tok_eq, transcribe)


def heard(y, a, b, cuts):
    parts, t = [], a
    for x, z in sorted(cuts):
        if z <= a or x >= b:
            continue
        parts.append(slice_of(y, t, max(t, x)))
        t = max(t, z)
    parts.append(slice_of(y, t, b))
    return np.concatenate(parts)


def bound_check(db, t, side, hi, lo, inner=False):
    """inner = an edge of a `cut` inside the line: the removed side is loud by definition (the false start),
    so only the level AT the bound counts there."""
    i = int(round(t * 100))
    here = db[max(0, i - 1):i + 2].max()
    out = db[i:i + 8] if side == "end" else db[max(0, i - 8):i]
    bad = here > lo + 6 or (not inner and len(out) and out.max() > hi)
    return bad, here, (out.max() if len(out) else -99)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--keep")
    ap.add_argument("--lines")
    ap.add_argument("--langs", default="en,fr")
    ap.add_argument("--audio")
    a = ap.parse_args()
    P = Project(a.project)
    from build_clean import load_keep
    keep = load_keep(a.keep or P.work / "keep.json")
    only = {int(x) for x in a.lines.split(",")} if a.lines else None
    y = load_audio(a.audio or P.mic16())
    db = db_strip(y)
    ref, hi, lo = thresholds_from(db, [(k["a"], k["b"]) for k in keep])
    langs = a.langs.split(",")
    out = [f"ref {ref:.1f} dB  T_high {hi:.1f}  T_low {lo:.1f}"]
    nflag = 0
    for li, k in enumerate(keep, 1):
        if only and li not in only:
            continue
        A, B, cuts = k["a"], k["b"], k["cut"]
        lines, flags = [f"#{li:3} [{A:.2f}-{B:.2f}] « {k['text']} »"], []
        # bounds
        bounds = [(A, "start", False), (B, "end", False)] + [(x, "end", True) for x, _ in cuts] + [(z, "start", True) for _, z in cuts]
        for t, side, inner in bounds:
            bad, here, outside = bound_check(db, t, side, hi, lo, inner)
            if bad:
                flags.append(f"BOUND {side} {t:.2f} inside a sound (level {here:.0f} dB, removed side max {outside:.0f})")
        # start proofs: from the line start and from every cut end
        for t in [A] + [z for _, z in sorted(cuts)]:
            for lang in langs:
                txt = transcribe(heard(y, t, B, cuts), lang, t, words=False)[0]
                lines.append(f"     from {t:7.2f} {lang}: {txt or '(nothing)'}")
        # end proof
        for lang in langs:
            s0 = max(A, B - 1.3)
            short = transcribe(heard(y, s0, B, cuts), lang, s0, words=False)[0]
            long = transcribe(slice_of(y, s0, B + 0.45), lang, s0, words=False)[0]
            st, lt = norm_tokens(short), norm_tokens(long)
            lines.append(f"     end  {lang}: …{short}  ||  +0.45 s: …{long}")
            if st and lt and st[-1] != lt[min(len(st), len(lt)) - 1] and lt[min(len(st), len(lt)) - 1].startswith(st[-1]):
                flags.append(f"END {lang}: « {st[-1]} » -> « {lt[min(len(st), len(lt)) - 1]} » with 0.45 s more: the end may clip the word")
            elif st and len(lt) == len(st) and len(lt[-1]) > len(st[-1]) + 1 and tok_eq(st[-1], lt[-1]):
                flags.append(f"END {lang}: last word longer with 0.45 s more (« {st[-1]} » -> « {lt[-1]} »)")
        lines += [f"  !! {f}" for f in flags]
        nflag += bool(flags)
        block = "\n".join(lines)
        print(block, flush=True)
        out.append(block)
    (P.work / "proof.txt").write_text("\n".join(out) + "\n", encoding="utf8")
    print(f"\n{nflag} lines with a bound/end flag -> {P.work / 'proof.txt'}. Read every « from » line against the "
          "intended text too: the script cannot judge meaning.")


if __name__ == "__main__":
    main()
