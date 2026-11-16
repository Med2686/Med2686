"""Shortlist library candidates for every bank role (ranked against a reference cut or a synth prototype), with a spectrogram montage.
usage: python build_bank.py restore              -> rebuilds the missing sfx/bank/*.wav from bank.json (after `sfx_fetch.py mixkit-all`)
       python build_bank.py shortlist            -> sfx/bank/_shortlist/<role>.png + shortlist.json
       python build_bank.py pick role=key ...    -> copies the chosen files to sfx/bank/<role>.wav and writes bank.json
The uisfx 'glass' pack is excluded everywhere (the user hates the glass sound)."""
import os, sys, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from sfx_match import rank, montage, LIB, fpath

ROOT = os.path.join(os.path.dirname(__file__), "..")
REF, BANK, SYN = (os.path.join(ROOT, "sfx", d) for d in ("refs", "bank", "synth"))
ROLES = {  # role: (reference file, keyword family, what it is for)
    "scene_in_riser":  ("ref_teal_scene_riser_in.wav", "whoosh,swoosh,woosh,air,zoom,transition,sweep,riser,swell", "into a fluted scene (bridge-dot dissolve)"),
    "scene_out_whoosh": ("ref_teal_scene_whoosh_out.wav", "whoosh,swoosh,woosh,air,swish", "back to the speaker"),
    "word_prelap":     ("ref_teal_prelap_whoosh.wav", "whoosh,swoosh,woosh,air,sweep,swish", "ends on a chrome word (1 in 3 max)"),
    "card_ping":       ("ref_teal_card_ping.wav", "notification,ping,tone,interface,pop,bubble,bleep,select", "card / plate lands"),
    "violet_whoomp":   ("ref_violet_streak_whoomp.wav", "whoosh,woosh,swoosh,bass,boom,impact,transition", "Violet Glass streak transition"),
    "glass_sparkle":   ("ref_violet_glass_sparkle.wav", "sparkle,magic,fairy,shimmer,glitter,spell,chime", "Violet card/ribbon appears"),
    "click_smear":     ("ref_violet_click_smear.wav", "swoosh,sweep,transition,whoosh,zap", "Violet button click smear"),
    "ui_blip":         ("ref_violet_ui_blip.wav", "blip,beep,interface,tone,pop,select,tap", "quiet UI blip (bars, nodes)"),
    "node_tick":       ("SYN:tick.wav", "tick,click,tap,interface,step,blip", "comet reaches a node / chip pops"),
    "counter_roll":    ("SYN:roll.wav", "clock,tick,slot,counter,progress,spin", "number rolling"),
    "dive_whoosh":     ("SYN:whoosh.wav", "whoosh,zoom,swoosh,woosh", "dive into a thumbnail / fly-over"),
    "click":           ("SYN:click.wav", "click,mouse,tap,press", "button press"),
    "typing":          ("SYN:typing.wav", "typing,keyboard,type,keys", "search bar / terminal typing"),
    "stamp":           ("SYN:stamp.wav", "stamp,thud,punch,hit,impact", "stamp slam"),
}


def ref_path(r):
    return os.path.join(SYN, r[4:]) if r.startswith("SYN:") else os.path.join(REF, r)


def shortlist():
    out = os.path.join(BANK, "_shortlist"); os.makedirs(out, exist_ok=True)
    res = {}
    for role, (ref, kw, _) in ROLES.items():
        info, hits = rank(ref_path(ref), top=12, kw=kw)
        hits = [h for h in hits if "uisfx-glass" not in h[0]][:5]
        res[role] = [(k, round(d, 2), m.get("title", ""), m["dur"]) for k, d, m in hits]
        montage(ref_path(ref), hits, os.path.join(out, f"{role}.png"))
        print(role, "->", [(k.split('/')[-1][:40], d) for k, d, _, _ in res[role]])
    json.dump(res, open(os.path.join(out, "shortlist.json"), "w"), indent=1)


def pick(pairs):
    ix = json.load(open(os.path.join(LIB, "index.json"), encoding="utf-8"))
    bank = json.load(open(os.path.join(BANK, "bank.json"))) if os.path.exists(os.path.join(BANK, "bank.json")) else {}
    for role, key in pairs:
        if key.startswith("synth:"):
            src = os.path.join(SYN, key[6:] + ".wav"); meta = {"source": "synth", "title": key, "license": "own (procedural)"}
        else:
            meta = ix[key] if key in ix else json.load(open(os.path.join(LIB, "..", "packs", "index.json"), encoding="utf-8"))[key]
            src = fpath(meta)
        shutil.copy(src, os.path.join(BANK, f"{role}.wav"))
        bank[role] = {"file": f"{role}.wav", "from": key, "title": meta.get("title"), "license": meta.get("license"),
                      "page": meta.get("page", ""), "use": ROLES[role][2]}
    json.dump(bank, open(os.path.join(BANK, "bank.json"), "w"), indent=1, ensure_ascii=False)
    print("bank:", list(bank))


def restore():
    """The repo ships bank.json but not the Mixkit wavs (Mixkit's licence forbids sharing the raw files).
    Rebuild them from the local library, made by `sfx_fetch.py mixkit-all`."""
    ix = json.load(open(os.path.join(LIB, "index.json"), encoding="utf-8"))
    bank = json.load(open(os.path.join(BANK, "bank.json"), encoding="utf-8"))
    for role, b in bank.items():
        out = os.path.join(BANK, b["file"])
        if os.path.exists(out):
            continue
        src = b["from"]
        rev = src.startswith("reversed ")
        key = src.split(" ")[-1]
        if src.startswith("synth:"):
            shutil.copy(os.path.join(SYN, src[6:] + ".wav"), out)
        elif src.startswith("synth "):  # synth layer + a Mixkit layer: the synth prototype is close enough
            shutil.copy(os.path.join(SYN, src.split(" ")[1] + ".wav"), out)
        elif key in ix:
            if rev:
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", fpath(ix[key]), "-af", "areverse", out], check=True)
            else:
                shutil.copy(fpath(ix[key]), out)
        else:
            print(f"{role}: {key} not in the library yet (run sfx_fetch.py mixkit-all first)")
            continue
        print(role, "<-", src)


if __name__ == "__main__":
    if sys.argv[1] == "restore": restore(); sys.exit()
    if sys.argv[1] == "shortlist": shortlist()
    elif sys.argv[1] == "pick": pick([a.split("=", 1) for a in sys.argv[2:]])
