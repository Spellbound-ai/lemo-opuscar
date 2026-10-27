"""Original narration (Tap_35.MP3) + very soft whooshes on chapter wipes -> out/mix.wav. my-assets audio is not used."""
import os, sys, subprocess
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get('LIB', os.path.abspath(os.path.join(HERE, '../../..')))
sys.path.insert(0, os.path.join(LIB, 'core/audio'))
import sfx
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
wav = os.path.join(HERE, 'out/voice.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, '../voice.mp3'), '-ar', str(sfx.SR), '-ac', '2', wav], check=True)
buf, _ = sf.read(wav)
for t in [46.3, 62.9, 78.7, 93.45, 108.7, 157.1, 203.1, 232.1, 254.2, 282.8, 322.5, 393.8, 410.5, 423.6]:
    sfx.add(buf, sfx.whoosh(.45), t - .1, gain=0.03)
sf.write(os.path.join(HERE, 'out/mix.wav'), np.clip(buf, -1, 1), sfx.SR)
print('mix ok', len(buf) / sfx.SR)
