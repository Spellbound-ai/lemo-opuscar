"""Original voice + very soft whooshes at scene changes -> out/mix.wav"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
LIB = os.environ.get('LIB', os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.join(LIB, 'core/audio'))
import sfx
HERE = os.path.dirname(os.path.abspath(__file__))
SR = sfx.SR
wav = os.path.join(HERE, 'out/voice.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'voice.mp3'), '-ar', str(SR), '-ac', '2', wav], check=True)
v, _ = sf.read(wav)
buf = v.copy()
cuts = [0, 46.3, 62.9, 78.7, 93.7, 108.7, 157.1, 203.1, 232.1, 254.2, 282.8, 322.5, 393.8, 410.5, 423.6, 458.6][1:]
for t in cuts:
    sfx.add(buf, sfx.whoosh(.45), t - .1, gain=0.03)
sf.write(os.path.join(HERE, 'out/mix.wav'), np.clip(buf, -1, 1), SR)
print('mix ok', len(buf) / SR)
