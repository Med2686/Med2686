# usage: python matte.py cut-video.mp4 cut.json rvm.onnx out-matte.mp4
# Person matte (white = the speaker, black = background) for every frame, with Robust Video Matting.
# The recurrent memory is reset at every jump cut so edges never "drag" across a cut.
import sys, json, subprocess, numpy as np, onnxruntime as ort

src, cutf, model, out = sys.argv[1:5]
W, H = 1080, 1920
cut_starts = {c["cutStartF"] for c in json.load(open(cutf))["clips"]}
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                       stdout=subprocess.PIPE, bufsize=W * H * 3 * 2)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
ratio = np.array([0.25], np.float32)
zero = lambda: [np.zeros((1, 1, 1, 1), np.float32)] * 4
rec = zero()
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    if n in cut_starts:
        rec = zero()
    x = np.frombuffer(buf, np.uint8).reshape(H, W, 3).transpose(2, 0, 1)[None].astype(np.float32) / 255
    fgr, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ratio})
    enc.stdin.write((np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8).tobytes())
    n += 1
    if n % 150 == 0:
        print(f"{n} frames", flush=True)
enc.stdin.close(); enc.wait()
print("done", n)
