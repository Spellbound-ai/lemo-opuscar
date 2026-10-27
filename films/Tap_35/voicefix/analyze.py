import json, numpy as np, librosa, soundfile as sf
y, sr = librosa.load('../voice.mp3', sr=16000)
cues = json.load(open('../cues.json'))
rows = []
for i, c in enumerate(cues):
    seg = y[int(c['t0']*sr):int(c['t1']*sr)]
    if len(seg) < sr * .5: continue
    f0, v, _ = librosa.pyin(seg, fmin=120, fmax=450, sr=sr, frame_length=1024)
    f0 = f0[v]
    S = np.abs(librosa.stft(seg, n_fft=1024))
    cen = librosa.feature.spectral_centroid(S=S, sr=sr).mean()
    mf = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=13).mean(axis=1)
    rows.append(dict(i=i, t0=c['t0'], f0=float(np.median(f0)) if len(f0) else 0, f0sd=float(np.std(f0)) if len(f0) else 0, cen=float(cen), mf=mf.tolist()))
json.dump(rows, open('stats.json', 'w'))
F = np.array([r['f0'] for r in rows]); M = np.array([r['mf'] for r in rows]); mu = M.mean(0)
d = np.linalg.norm(M - mu, axis=1)
print('median F0 overall %.1f  IQR %.1f-%.1f' % (np.median(F), *np.percentile(F, [25, 75])))
for r, dd in zip(rows, d):
    flag = ('*' if abs(12*np.log2(r['f0']/np.median(F))) > 1.5 else ' ') + ('#' if dd > np.percentile(d, 90) else ' ')
    print(f"{flag} {int(r['t0']//60)}:{r['t0']%60:05.2f} f0={r['f0']:.0f} semi={12*np.log2(r['f0']/np.median(F)):+.1f} cen={r['cen']:.0f} mfccdist={dd:.1f}")
