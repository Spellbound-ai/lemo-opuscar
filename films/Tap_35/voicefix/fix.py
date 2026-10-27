"""Make the narration sound like one speaker: per-sentence partial pitch normalisation (formant-preserving
rubberband) + partial spectral-envelope matching, stitched back with short crossfades."""
import json, subprocess, os, numpy as np, soundfile as sf, librosa
from scipy.signal import fftconvolve
SR = 48000
R = {r['i']: r for r in json.load(open('stats.json'))}
cues = json.load(open('../cues.json'))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '../voice.mp3', '-ac', '1', '-ar', str(SR), 'orig.wav'], check=True)
y, _ = sf.read('orig.wav')
med = np.median([r['f0'] for r in R.values() if r['f0'] > 0])
STRENGTH, CLAMP = 0.75, 3.0          # correct 75 % of the deviation, at most 3 semitones

# spectral envelope (1/3-octave bands) per cue and global
edges = 50 * 2 ** (np.arange(0, 28) / 3); edges = edges[edges < 15000]
def bands(x):
    S = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2 if len(x) < 4096 else np.mean([np.abs(np.fft.rfft(f * np.hanning(4096))) ** 2 for f in np.lib.stride_tricks.sliding_window_view(x, 4096)[::2048]], axis=0)
    fr = np.fft.rfftfreq(4096 if len(x) >= 4096 else len(x), 1 / SR)
    return np.array([10 * np.log10(S[(fr >= a) & (fr < b)].mean() + 1e-12) for a, b in zip(edges[:-1], edges[1:])])

segs = []
for i, c in enumerate(cues):
    a, b = int((c['t0'] - .06) * SR), int((c['t1'] + .12) * SR)
    segs.append((i, max(0, a), min(len(y), b)))
B = {i: bands(y[a:b]) for i, a, b in segs if b - a > SR // 2}
G = np.median(np.array(list(B.values())), axis=0)
out = y.copy(); fade = int(.03 * SR); log = []
for i, a, b in segs:
    x = y[a:b].copy(); semi = 0.0
    if i in R and R[i]['f0'] > 0:
        dev = 12 * np.log2(R[i]['f0'] / med)
        semi = float(np.clip(-STRENGTH * dev, -CLAMP, CLAMP))
    if abs(semi) > .25:
        sf.write('tmp_in.wav', x, SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'tmp_in.wav', '-af', f'rubberband=pitch={2 ** (semi / 12):.5f}:formant=preserved:pitchq=quality:transients=smooth', 'tmp_out.wav'], check=True)
        x2, _ = sf.read('tmp_out.wav'); x = x2[:len(x)] if len(x2) >= len(x) else np.pad(x2, (0, len(x) - len(x2)))
    if i in B:   # partial EQ toward the global envelope
        gain = np.clip(.6 * (G - bands(x)), -6, 6)
        gain -= np.average(gain)                       # keep loudness, change only tilt/colour
        centres = np.sqrt(edges[:-1] * edges[1:]); fr = np.fft.rfftfreq(1024, 1 / SR)
        H = 10 ** (np.interp(np.log(fr + 1), np.log(centres), gain) / 20)
        h = np.fft.fftshift(np.fft.irfft(H)) * np.hanning(1024)
        x = fftconvolve(x, h, mode='same')
    w = np.ones(len(x)); w[:fade] = np.linspace(0, 1, fade); w[-fade:] = np.linspace(1, 0, fade)
    out[a:b] = out[a:b] * (1 - w) + x * w
    log.append((c := cues[i])['t0']); log[-1] = (round(cues[i]['t0'], 2), round(semi, 2))
sf.write('voice_fixed.wav', out, SR)
json.dump(log, open('fixlog.json', 'w'))
print('done', sum(1 for _, s in log if abs(s) > .25), 'sentences pitch-adjusted')
