"""Cut the B-roll from my-assets/ per edl.py into one silent 24 fps track, then into JPEG frames for the page."""
import subprocess, os, sys
from edl import EDL, DUR
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, '../../../my-assets')
seg = os.path.join(HERE, 'seg'); os.makedirs(seg, exist_ok=True)
lst = []
for i, (t0, c, s, n) in enumerate(EDL):
    t1 = EDL[i + 1][0] if i + 1 < len(EDL) else DUR
    nf = round(t1 * 24) - round(t0 * 24)
    o = f'{seg}/s{i:03d}.mp4'; lst.append(o)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-i', f'{A}/Clip{c}.mp4', '-an', '-vf', 'fps=24,scale=1280:720,setsar=1',
                    '-frames:v', str(nf), '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', o], check=True)
open(f'{seg}/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in lst))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{seg}/list.txt', '-c', 'copy', f'{HERE}/bg.mp4'], check=True)
fr = os.path.join(HERE, 'bg'); os.makedirs(fr, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{HERE}/bg.mp4', '-q:v', '3', f'{fr}/%05d.jpg'], check=True)
print('frames', len(os.listdir(fr)), 'expected', round(DUR * 24))
