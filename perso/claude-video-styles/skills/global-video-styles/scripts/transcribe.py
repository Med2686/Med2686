# usage: python transcribe.py in.wav out.json   (French, word timestamps, no VAD so every take is kept)
import os
import sys, json
from faster_whisper import WhisperModel
import wave, numpy as np
wf = wave.open(sys.argv[1]); audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs, info = m.transcribe(audio, language=os.environ.get("WHISPER_LANG", "fr"), word_timestamps=True, vad_filter=False, beam_size=5,
                          condition_on_previous_text=False,
                          initial_prompt=os.environ.get("WHISPER_PROMPT", "the speaker, Claude, la tech, le cloud, l'IA, wesh, frère."))
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for w in s.words]})
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}", flush=True)
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
