import sys, urllib.request
from pathlib import Path

url = sys.argv[1]
out = Path(sys.argv[2])
out.parent.mkdir(parents=True, exist_ok=True)

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r, open(out, 'wb') as f:
    while True:
        chunk = r.read(1024*1024)
        if not chunk:
            break
        f.write(chunk)

print(str(out))
