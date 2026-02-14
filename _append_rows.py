import csv, json, sys

in_json = sys.stdin.read()
obj = json.loads(in_json)
rows = obj.get('jobs', [])
out_path = r'C:\Users\Administrator\.openclaw\workspace\workopolis_canada_qa_companies.csv'

# de-dupe by company name already in file
seen=set()
with open(out_path, newline='', encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        seen.add((row['company'] or '').strip().lower())

new=[]
for j in rows:
    c=(j.get('company') or '').strip()
    if not c: continue
    key=c.lower()
    if key in seen: continue
    seen.add(key)
    new.append({
        'company': c,
        'example_job_title': (j.get('title') or '').strip(),
        'example_job_url': (j.get('url') or '').strip(),
        'location': (j.get('location') or '').strip(),
        'source': 'Workopolis'
    })

with open(out_path, 'a', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['company','example_job_title','example_job_url','location','source'])
    for row in new:
        w.writerow(row)

print(len(new))
