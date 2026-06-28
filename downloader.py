
import os, subprocess, sys, json
from pathlib import Path
Path('output').mkdir(exist_ok=True)
url = os.environ.get('TARGET_URL','')
mode = os.environ.get('MODE','auto')
if not url:
    print('No URL provided'); sys.exit(1)
print(f'Downloading: {url} (mode={mode})')
if mode == 'audio':
    cmd=['yt-dlp','--no-playlist','-x','--audio-format','mp3','--audio-quality','0','-o','output/%(title)s.%(ext)s',url]
else:
    cmd=['yt-dlp','--no-playlist','-f','best[filesize<80M]/best','-o','output/%(title)s.%(ext)s',url]
result=subprocess.run(cmd,capture_output=True,text=True)
print(result.stdout)
if result.returncode!=0:
    print(result.stderr)
    # Try direct download
    import requests
    r=requests.get(url,stream=True,timeout=30)
    fname='output/file'+os.path.splitext(url.split('/')[-1])[1] or '.bin'
    with open(fname,'wb') as f:
        for chunk in r.iter_content(8192): f.write(chunk)
    print(f'Direct download: {fname}')
files=list(Path('output').iterdir())
meta={'url':url,'mode':mode,'files':[str(f.name) for f in files],'success':len(files)>0}
with open('output/meta.json','w') as f: import json; json.dump(meta,f)
print(f'Done. Files: {[str(f) for f in files]}')
