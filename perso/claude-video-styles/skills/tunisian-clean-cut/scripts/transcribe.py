"""Whisper large-v3 passes on the mic (GPU), in Arabic (Derja prompt), French and English.

  python -I transcribe.py -p <project> --regions [--langs ar,fr,en]    # each region ALONE (the main "hear" pass)
  python -I transcribe.py -p <project> --full    [--langs ar,fr]       # whole file, for the overall topic

Why three languages: he speaks Tunisian Derja mixed with French and English, and no single pass is right.
- language="ar" TRANSLATES Derja into Modern Standard Arabic: « ana personnellement ma nchouf ken zouz 7ajet »
  comes back as « أنا شخصياً لا أرى إلا شيئين ». Clean-looking, but not his words: useless to judge retakes.
- fr writes the French words right and phonetises the Derja (« ena kinshuv » = « ena ki nchouf »).
- en is the best proxy for repeats (« so don't, so don't just learn AI »).
Each region is cut out alone, padded with 0.25 s of zeros, condition_on_previous_text=False, so the context
of the last line cannot be reused to « tidy » this one. Hallucinations (Sous-titrage ST' 501, ترجمة نانسي,
Thanks for watching, اشتركوا في القناة, the prompt recited back) are blanked and mark NON-speech.
Out: work/tx-regions.json + .txt, or work/tx-mic-<lang>.json + .txt
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (PROMPTS, Project, add_project_arg, is_hallu, load_audio, model, prompt_echo,  # noqa: E402
                        read_json, slice_of, transcribe, write_json)


def full_pass(P, y, langs):
    for lang in langs:
        ss, _ = model().transcribe(y, language=lang, word_timestamps=True, beam_size=5, initial_prompt=PROMPTS.get(lang),
                                   vad_filter=False, condition_on_previous_text=False)
        out = []
        for s in ss:
            t = s.text.strip()
            junk = is_hallu(t) or prompt_echo(t, PROMPTS.get(lang))
            out.append({"s": round(s.start, 2), "e": round(s.end, 2), "t": t, "nonspeech": junk,
                        "w": [[w.word.strip(), round(w.start, 2), round(w.end, 2), round(w.probability, 2)] for w in s.words or []]})
        write_json(P.work / f"tx-mic-{lang}.json", out, indent=0)
        with open(P.work / f"tx-mic-{lang}.txt", "w", encoding="utf8") as f:
            for s in out:
                f.write(f"[{s['s']:7.2f}-{s['e']:7.2f}] {'(NON-SPEECH) ' if s['nonspeech'] else ''}{s['t']}\n")
        print("done", lang, len(out), "segments", flush=True)


def region_pass(P, y, langs):
    reg = read_json(P.work / "regions.json")
    out = []
    txt = open(P.work / "tx-regions.txt", "w", encoding="utf8")
    for i, (a, b) in enumerate(reg, 1):
        row = {"i": i, "a": a, "b": b}
        lines = [f"#{i:3} [{a:7.2f}-{b:7.2f}] ({b - a:.2f} s)"]
        for lang in langs:
            text, ws = transcribe(slice_of(y, a, b), lang, a, pad=0.25, raw=True)
            row[lang] = text
            row[lang + "_w"] = ws
            lines.append(f"      {lang.upper()}: {text or '(nothing)'}")
        out.append(row)
        block = "\n".join(lines)
        print(block, flush=True)
        txt.write(block + "\n")
        txt.flush()
    txt.close()
    write_json(P.work / "tx-regions.json", out, indent=0)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--regions", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--langs", default=None)
    a = ap.parse_args()
    P = Project(a.project)
    y = load_audio(P.mic16())
    if a.full:
        full_pass(P, y, (a.langs or "ar,fr").split(","))
    if a.regions or not a.full:
        region_pass(P, y, (a.langs or "ar,fr,en").split(","))


if __name__ == "__main__":
    main()
