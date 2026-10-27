"""Find stable shots in my-assets clips (hard cuts AND soft dissolves), 10 fps luma diff."""
import subprocess, numpy as np, json, sys
FPS = 10; W, H = 96, 54
out = {}
for c in range(1, 8):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'../../../my-assets/Clip{c}.mp4', '-vf', f'fps={FPS},scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(p, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))           # d[i] = change between frame i and i+1
    moving = d > 2.0                                              # any noticeable change (cut or dissolve or fast motion)
    cut = d > 12.0
    # a shot = maximal run of frames with no cut, and we trim any dissolve run (>=3 consecutive moving frames with total change > 25) at edges
    shots = []; s = 0
    for i in range(len(d)):
        if cut[i]: shots.append((s, i)); s = i + 1
    shots.append((s, len(fr) - 1))
    res = []
    for a, b in shots:
        # split further on dissolves: windows of 1 s whose cumulative change > 30
        cum = np.convolve(d[a:b], np.ones(FPS), 'same') if b - a > FPS else np.zeros(max(0, b - a))
        bad = cum > 30
        k = a
        for j in range(len(bad) + 1):
            if j == len(bad) or bad[j]:
                if (a + j) - k >= 1: res.append((k / FPS, (a + j) / FPS))
                k = a + j + 1
    out[c] = [r for r in res if r[1] - r[0] >= 2.0]
    print(c, len(out[c]), 'shots >=2s')
json.dump(out, open('shots.json', 'w'))
