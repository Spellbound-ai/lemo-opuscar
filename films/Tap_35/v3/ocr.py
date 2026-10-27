"""OCR every stable shot (start, middle, end) and record Latin words, to reject shots with English text."""
import json, subprocess, re, os
from concurrent.futures import ThreadPoolExecutor
os.environ['OMP_THREAD_LIMIT'] = '1'
S = json.load(open('shots.json'))
os.makedirs('ocr', exist_ok=True)

def extract(c):   # one decode pass per clip, 2 fps
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'../../../my-assets/Clip{c}.mp4', '-vf', 'fps=2,scale=960:-1', '-q:v', '3', f'ocr/c{c}_%04d.jpg'], check=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(extract, S.keys()))

def fr(c, t): return f'ocr/c{c}_{int(t * 2) + 1:04d}.jpg'
def ocr(f):
    o = subprocess.run(['tesseract', f, '-', '--psm', '11', '-l', 'eng', 'tsv'], capture_output=True, text=True).stdout
    w = []
    for ln in o.splitlines()[1:]:
        p = ln.split('\t')
        if len(p) == 12 and p[11].strip() and float(p[10]) > 70:
            x = re.sub(r'[^A-Za-z]', '', p[11])
            if len(x) >= 3: w.append(x)
    return w

def job(j):
    c, i, a, b = j; toks = []
    for t in sorted({a + .5, (a + b) / 2, b - .5}):
        if os.path.exists(fr(c, t)): toks += ocr(fr(c, t))
    return (c, i, a, b, sorted(set(toks)))

jobs = [(int(c), i, a, b) for c, L in S.items() for i, (a, b) in enumerate(L)]
with ThreadPoolExecutor(4) as ex: R = list(ex.map(job, jobs))
json.dump(R, open('ocr.json', 'w'))
for r in R: print(r[0], r[1], f'{r[2]:.1f}-{r[3]:.1f}', ' '.join(r[4])[:100])
