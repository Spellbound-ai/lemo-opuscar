import subprocess,sys
from edl import EDL,DUR
out=sys.argv[1]
for i,(t0,c,s,n) in enumerate(EDL):
    t1=EDL[i+1][0] if i+1<len(EDL) else DUR
    d=t1-t0
    for k,ts in enumerate([s+0.05, s+d-0.1]):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ts),'-i',f'../../../my-assets/Clip{c}.mp4','-frames:v','1','-vf',f"scale=240:-1,drawtext=text='{i} {k} c{c}':x=2:y=2:fontsize=16:fontcolor=yellow:box=1:boxcolor=black",f'{out}/e{i:03d}_{k}.jpg'])
