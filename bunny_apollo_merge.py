import os, json, csv, urllib.request, urllib.parse
from datetime import datetime
zone='mypcown'
key='a1187d33-cd54-4c8c-a43cb8aefb2e-93c6-44c1'
base='https://storage.bunnycdn.com'
path='apollo/'
out_dir=r'C:\Users\Administrator\.openclaw\workspace\bunny_apollo'
os.makedirs(out_dir, exist_ok=True)
list_url=f'{base}/{zone}/{path}'
req=urllib.request.Request(list_url, headers={'AccessKey': key})
with urllib.request.urlopen(req, timeout=30) as resp:
    items=json.loads(resp.read())
files=[it for it in items if (not it.get('IsDirectory')) and it.get('ObjectName','').lower().endswith('.csv')]
print('files', len(files))
for idx, it in enumerate(files, 1):
    name=it['ObjectName']
    url=f"{base}/{zone}/{path}{urllib.parse.quote(name)}"
    dest=os.path.join(out_dir, name)
    if not os.path.exists(dest):
        req=urllib.request.Request(url, headers={'AccessKey': key})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest,'wb') as f:
            f.write(r.read())
    if idx % 10 == 0 or idx == len(files):
        print(f"downloaded {idx}/{len(files)}")

headers=[]
rows=[]
for idx, it in enumerate(files, 1):
    name=it['ObjectName']
    fp=os.path.join(out_dir, name)
    with open(fp, 'r', newline='', encoding='utf-8-sig', errors='ignore') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames is None:
            continue
        for h in reader.fieldnames:
            if h not in headers:
                headers.append(h)
        for row in reader:
            rows.append(row)
    if idx % 20 == 0 or idx == len(files):
        print(f"merged {idx}/{len(files)}")

out_csv=os.path.join(out_dir,'combined_apollo.csv')
with open(out_csv,'w', newline='', encoding='utf-8') as f:
    writer=csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    for r in rows:
        writer.writerow({h: r.get(h, '') for h in headers})
print('combined rows', len(rows), 'headers', len(headers))
