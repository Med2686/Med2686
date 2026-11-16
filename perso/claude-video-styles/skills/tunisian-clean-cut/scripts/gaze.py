# usage: python gaze.py video.mp4 face_landmarker.task out.json
# Per frame: eye-gaze blendshapes + head pose, to find the moments the speaker looks up-left at his script.
import sys, json, math, subprocess, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

video, model, out = sys.argv[1:4]
W, H = 540, 960
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={W}:{H}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                        stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO,
    output_face_blendshapes=True, output_facial_transformation_matrixes=True, num_faces=1))
KEYS = ["eyeLookUpLeft", "eyeLookUpRight", "eyeLookDownLeft", "eyeLookDownRight",
        "eyeLookInLeft", "eyeLookInRight", "eyeLookOutLeft", "eyeLookOutRight", "eyeBlinkLeft", "eyeBlinkRight"]
rows, i = [], 0
while True:
    buf = proc.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    r = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(buf, np.uint8).reshape(H, W, 3)), int(i * 1000 / 30))
    if r.face_landmarks:
        bs = {c.category_name: round(c.score, 3) for c in r.face_blendshapes[0]}
        m = np.array(r.facial_transformation_matrixes[0])
        yaw = math.degrees(math.atan2(m[0, 2], m[2, 2]))
        pitch = math.degrees(math.asin(-m[1, 2]))
        p = r.face_landmarks[0]
        # iris position inside each eye (0..1 across, 0..1 down), image-space
        def iris(c, a, b, t, btm):
            return ((p[c].x - p[a].x) / (p[b].x - p[a].x + 1e-6), (p[c].y - p[t].y) / (p[btm].y - p[t].y + 1e-6))
        ir = iris(468, 33, 133, 159, 145)   # subject's right eye (image left)
        il = iris(473, 362, 263, 386, 374)  # subject's left eye (image right)
        rows.append([i] + [bs.get(k, 0) for k in KEYS] + [round(yaw, 1), round(pitch, 1), round(ir[0], 3), round(ir[1], 3), round(il[0], 3), round(il[1], 3)])
    else:
        rows.append([i] + [None] * (len(KEYS) + 6))
    i += 1
json.dump({"cols": ["f"] + KEYS + ["yaw", "pitch", "irRx", "irRy", "irLx", "irLy"], "rows": rows}, open(out, "w"))
print("frames", i, "faces", sum(r[1] is not None for r in rows))
