"""Cut the camera file on the frames of work/clean.json -> <remotion>/public/footage/talk-clean-vN.mp4.

  python -I make_face.py -p <project> --version 1 [--small] [--clean work/clean.json] [--out file.mp4] [--force]

One decode of the camera file, normalised to the fps grid (iPhone "30 fps" is 29.997: fps=30 first, so
frame n of the grid = camF), then select the kept frames with a BALANCED-TREE expression (a flat chain of
113 between() crashes ffmpeg's parser), then tone map if the source is HDR:
  HLG (arib-std-b67, iPhone) / PQ (smpte2084) -> SDR BT.709 with zscale + tonemap=mobius:param=0.3, npl=203
and one x264 encode (CRF 14 full res; --small = 1080x1920 CRF 18 preview, much faster). Full 4K is kept by
default: he insists on « same quality », and punch-ins stay sharp. Rotation is applied by ffmpeg itself.
Never overwrite a file Remotion Studio has open: each version gets a new name (talk-clean-v2.mp4 ...).
ffmpeg 9 reads the graph from a file with -/filter_complex.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import Project, add_project_arg, read_json  # noqa: E402


def probe(src):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,avg_frame_rate,color_transfer,color_primaries,pix_fmt:stream_side_data=rotation",
                        "-of", "json", str(src)], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["streams"][0]


def tree(t):
    return t[0] if len(t) == 1 else f"({tree(t[:len(t) // 2])}+{tree(t[len(t) // 2:])})"


def tonemap_chain(transfer):
    if transfer in ("arib-std-b67", "smpte2084"):
        return (f"zscale=tin={transfer}:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
                "tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
    return "format=yuv420p"


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--version", "-v", type=int, default=1)
    ap.add_argument("--small", action="store_true")
    ap.add_argument("--clean")
    ap.add_argument("--out")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    P = Project(a.project)
    fps = int(P["fps"])
    C = read_json(a.clean or P.work / "clean.json")
    out = Path(a.out) if a.out else P.remotion / "public" / "footage" / f"talk-clean-v{a.version}{'-small' if a.small else ''}.mp4"
    if out.exists() and not a.force:
        sys.exit(f"{out} exists: Studio may have it open. Use a new --version (or --force if Studio is stopped).")
    out.parent.mkdir(parents=True, exist_ok=True)
    st = probe(P.camera)
    transfer = st.get("color_transfer", "")
    print(f"camera {st.get('width')}x{st.get('height')} {st.get('avg_frame_rate')} transfer={transfer or 'sdr'} "
          f"rotation={[d.get('rotation') for d in st.get('side_data_list', [])]}")
    terms = [f"between(n,{p['camF']},{p['camF'] + p['n'] - 1})" for p in C["pieces"]]
    scale = "scale=-2:1920:flags=lanczos," if a.small else ""
    graph = f"[0:v]fps={fps},select='{tree(terms)}',setpts=N/{fps}/TB,{scale}{tonemap_chain(transfer)}[v]"
    gf = P.work / f"face-graph-v{a.version}.txt"
    gf.write_text(graph, encoding="utf8")
    # stop reading the camera 1 s after the last kept frame (select alone would decode the whole file)
    last = max(p["camF"] + p["n"] for p in C["pieces"]) / fps + 1.0
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-stats", "-y", "-t", f"{last:.3f}", "-i", str(P.camera),
           "-/filter_complex", str(gf),
           "-map", "[v]", "-an", "-r", str(fps), "-c:v", "libx264", "-preset", "fast" if a.small else "medium",
           "-crf", "18" if a.small else "14", "-g", "15", "-bf", "0", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    n = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout
    n = int(n.strip().strip(","))
    print(f"frames written {n}, wanted {C['totalF']} -> {out}")
    if n != C["totalF"]:
        sys.exit("frame count mismatch: the picture would drift from the voice. Check fps / camF.")


if __name__ == "__main__":
    main()
