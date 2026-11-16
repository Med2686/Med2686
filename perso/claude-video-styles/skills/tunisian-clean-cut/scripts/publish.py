"""Put clean cut version N into the project's Remotion folder, ready to check in Studio.

  python -I publish.py -p <project> --version 2 [--small] [--scaffold] [--port 3211]

- copies work/clean.json -> <remotion>/src/data/clean.json
- copies work/voice-clean.wav -> <remotion>/public/audio/voice-clean-vN.wav (never overwrites: Studio locks it)
- points CleanCut.tsx at footage/talk-clean-vN.mp4 (or -small) and audio/voice-clean-vN.wav
- --scaffold: creates the Remotion project from assets/remotion (package.json, config, Root with the
  CleanCut composition) with node_modules as a junction to Desktop/videos/remotion-video/node_modules,
  and adds a launch entry « <project>-studio » to Desktop/videos/.claude/launch.json.
Then start Studio (preview_start with that name), and send him the link + what to check.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import SKILL, Project, add_project_arg  # noqa: E402

SHARED_NM = Path.home() / "Desktop" / "reel-project" / "remotion-video" / "node_modules"
LAUNCH = Path.home() / "Desktop" / "reel-project" / ".claude" / "launch.json"


def scaffold(P, port, launch=LAUNCH):
    R = P.remotion
    (R / "src" / "data").mkdir(parents=True, exist_ok=True)
    (R / "public" / "footage").mkdir(parents=True, exist_ok=True)
    (R / "public" / "audio").mkdir(parents=True, exist_ok=True)
    A = SKILL / "assets" / "remotion"
    for f, dst in [("package.json", R), ("remotion.config.ts", R), ("tsconfig.json", R), ("index.ts", R / "src"),
                   ("Root.tsx", R / "src"), ("CleanCut.tsx", R / "src")]:
        if not (dst / f).exists():
            shutil.copy(A / f, dst / f)
    if not (R / "node_modules").exists() and SHARED_NM.exists():
        subprocess.run(["cmd", "/c", "mklink", "/J", str(R / "node_modules"), str(SHARED_NM)], check=True)
    if launch.exists():
        L = json.loads(launch.read_text(encoding="utf8"))
        name = f"{P.root.name}-studio"
        if not any(c.get("name") == name for c in L["configurations"]):
            rel = os.path.relpath(R.resolve(), launch.parent.parent.resolve()).replace("\\", "/")
            if rel.startswith(".."):
                rel = str(R.resolve()).replace("\\", "/")
            L["configurations"].append({"name": name, "runtimeExecutable": "npm",
                                        "runtimeArgs": ["--prefix", rel, "run", "dev", "--", "--no-open", "--port", str(port)],
                                        "port": port})
            launch.write_text(json.dumps(L, indent=2), encoding="utf8")
            print(f"launch entry {name} on port {port} added")


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--version", "-v", type=int, required=True)
    ap.add_argument("--small", action="store_true", help="point at the -small preview face file")
    ap.add_argument("--scaffold", action="store_true")
    ap.add_argument("--port", type=int, default=3211)
    ap.add_argument("--launch", default=str(LAUNCH), help="launch.json to add the Studio entry to")
    a = ap.parse_args()
    P = Project(a.project)
    R = P.remotion
    if a.scaffold:
        scaffold(P, a.port, Path(a.launch))
    if not (R / "src").exists():
        sys.exit(f"{R} has no src/: run with --scaffold first")
    (R / "src" / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy(P.work / "clean.json", R / "src" / "data" / "clean.json")
    voice = R / "public" / "audio" / f"voice-clean-v{a.version}.wav"
    voice.parent.mkdir(parents=True, exist_ok=True)
    if voice.exists():
        sys.exit(f"{voice} exists (Studio may hold it): use the next --version")
    shutil.copy(P.work / "voice-clean.wav", voice)
    face = f"footage/talk-clean-v{a.version}{'-small' if a.small else ''}.mp4"
    cc = R / "src" / "CleanCut.tsx"
    if not cc.exists():
        shutil.copy(SKILL / "assets" / "remotion" / "CleanCut.tsx", cc)
    s = cc.read_text(encoding="utf8")
    s = re.sub(r'FACE_FILE = "[^"]*"', f'FACE_FILE = "{face}"', s)
    s = re.sub(r'VOICE_FILE = "[^"]*"', f'VOICE_FILE = "audio/{voice.name}"', s)
    cc.write_text(s, encoding="utf8")
    if not (R / "public" / face).exists():
        print(f"[note] {face} not built yet: run make_face.py --version {a.version}{' --small' if a.small else ''}")
    root = (R / "src" / "Root.tsx").read_text(encoding="utf8") if (R / "src" / "Root.tsx").exists() else ""
    if "CleanCut" not in root:
        print("[note] Root.tsx has no CleanCut composition: add the one from assets/remotion/Root.tsx")
    print(f"published v{a.version}: {cc.name} -> {face} + audio/{voice.name}")


if __name__ == "__main__":
    main()
