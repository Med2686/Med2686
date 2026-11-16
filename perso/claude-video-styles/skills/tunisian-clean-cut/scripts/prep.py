"""Start a project: write project.json, extract the 16 kHz audio, optionally a 540p SDR proxy for gaze.

  python -I prep.py -p <project dir> --camera "~/Downloads/IMG_2874.MOV"
                    [--mic latest | --mic "<file.m4a>" | --mic none] [--proxy] [--remotion remotion-video]

--mic latest = the newest .m4a in Documents\\Sound Recordings by modification time (his mic take is the last
one recorded; the names « Recording (52) » are not reliable for order). Check the printed times: the mic
should have been recorded within minutes of the camera clip. --mic none = single source (camera audio).
Out: project.json, work/mic16k.wav, work/cam16k.wav (if a separate mic), work/proxy540.mp4 (--proxy).
Next: sync.py (separate mic only), then regions.py.
"""
import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import Project, add_project_arg  # noqa: E402
from make_face import probe, tonemap_chain  # noqa: E402

REC = Path.home() / "Documents" / "Sound Recordings"


def stamp(p):
    return dt.datetime.fromtimestamp(Path(p).stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")


def duration(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def to16k(src, dst):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", str(dst)], check=True)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--camera", required=True)
    ap.add_argument("--mic", default="latest")
    ap.add_argument("--proxy", action="store_true", help="also make work/proxy540.mp4 (fps grid, SDR) for gaze")
    ap.add_argument("--remotion", default=None)
    a = ap.parse_args()
    root = Path(a.project or os.getcwd())
    root.mkdir(parents=True, exist_ok=True)
    P = Project(root)
    P.cfg["camera"] = str(Path(a.camera).resolve())
    if a.mic == "none":
        P.cfg["mic"] = None
        P.cfg["offset"] = 0.0
    elif a.mic == "latest":
        recs = sorted(REC.glob("*.m4a"), key=lambda p: p.stat().st_mtime)
        if not recs:
            sys.exit(f"no .m4a in {REC}")
        P.cfg["mic"] = str(recs[-1])
        print("newest recordings: " + " | ".join(f"{p.name} {stamp(p)}" for p in recs[-3:]))
    else:
        P.cfg["mic"] = str(Path(a.mic).resolve())
    if a.remotion:
        P.cfg["remotion"] = a.remotion
    st = probe(P.camera)
    P.cfg["camera_info"] = {k: st.get(k) for k in ("width", "height", "avg_frame_rate", "color_transfer", "pix_fmt")}
    P.save()
    print(f"camera {P.camera.name}  {stamp(P.camera)}  {duration(P.camera):.1f} s  {st.get('width')}x{st.get('height')} "
          f"{st.get('avg_frame_rate')} {st.get('color_transfer') or 'sdr'}")
    if P.cfg["mic"]:
        print(f"mic    {Path(P.cfg['mic']).name}  {stamp(P.cfg['mic'])}  {duration(P.cfg['mic']):.1f} s")
        to16k(P.cfg["mic"], P.work / "mic16k.wav")
        to16k(P.camera, P.work / "cam16k.wav")
        print("next: sync.py (camera_t = mic_t + offset)")
    else:
        to16k(P.camera, P.work / "mic16k.wav")
    if a.proxy:
        out = P.work / "proxy540.mp4"
        vf = f"fps={P['fps']},scale=540:-2:flags=bilinear,{tonemap_chain(st.get('color_transfer', ''))}"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-stats", "-y", "-i", str(P.camera), "-vf", vf, "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", str(out)], check=True)
        print("proxy ->", out)
    print("project.json ->", P.cfg_path)


if __name__ == "__main__":
    main()
