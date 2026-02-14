import os, json, csv, re, io, urllib.request, urllib.parse, sys

zone='mypcown'
access_key='a1187d33-cd54-4c8c-a43cb8aefb2e-93c6-44c1'
base='https://storage.bunnycdn.com'
path='unknown/'
out_dir=r'C:\Users\Administrator\.openclaw\workspace\bunny_unknown'
os.makedirs(out_dir, exist_ok=True)

TARGET_HEADERS=[
    'First Name','Last Name','Title','Company Name','Email','Mobile Phone','Other Phone','Corporate Phone',
    'Employee Size','Industry','Person LinkedIn URL','Website','Company LinkedIn URL'
]

MAP={
    'first name':'First Name','firstname':'First Name','given name':'First Name','first':'First Name',
    'last name':'Last Name','lastname':'Last Name','surname':'Last Name','family name':'Last Name','last':'Last Name',
    'title':'Title','job title':'Title','position':'Title','role':'Title','job title (current)':'Title',
    'company':'Company Name','company name':'Company Name','organization':'Company Name','organisation':'Company Name',
    'account name':'Company Name','employer':'Company Name','company / account name':'Company Name',
    'email':'Email','email address':'Email','work email':'Email','email (work)':'Email','primary email':'Email',
    'employee size':'Employee Size','company size':'Employee Size','employees':'Employee Size','employee count':'Employee Size',
    'industry':'Industry','industry name':'Industry','category':'Industry',
    'linkedin':'Person LinkedIn URL','linkedin url':'Person LinkedIn URL','person linkedin':'Person LinkedIn URL','linkedin profile':'Person LinkedIn URL','profile url':'Person LinkedIn URL',
    'website':'Website','company website':'Website','domain':'Website','url':'Website',
    'company linkedin url':'Company LinkedIn URL','company linkedin':'Company LinkedIn URL','linkedin company':'Company LinkedIn URL','company profile url':'Company LinkedIn URL',
}

CONTACT_HINTS=set(list(MAP.keys()) + ['phone','mobile','cell','tel','telephone','direct','work phone','home phone'])


def norm_header(h):
    return re.sub(r'\s+',' ',h.strip().lower())


def split_numbers(val):
    if not val: return []
    parts=re.split(r'[;|,/\n]+', str(val))
    nums=[]
    for p in parts:
        p=p.strip()
        if not p: continue
        filtered=''.join(ch for ch in p if ch.isdigit() or ch=='+')
        if filtered.count('+')>1:
            filtered='+'+filtered.replace('+','')
        if len(re.sub(r'\D','',filtered))<7:
            continue
        nums.append(filtered)
    seen=set(); out=[]
    for n in nums:
        if n not in seen:
            seen.add(n); out.append(n)
    return out


def is_contact_row(r):
    return (
        (r.get('First Name','') or '').strip() or (r.get('Last Name','') or '').strip() or (r.get('Email','') or '').strip() or
        (r.get('Mobile Phone','') or '').strip() or (r.get('Other Phone','') or '').strip() or (r.get('Corporate Phone','') or '').strip() or
        (r.get('Title','') or '').strip() or (r.get('Company Name','') or '').strip() or (r.get('Person LinkedIn URL','') or '').strip()
    )


def score(r):
    s=0
    for k in TARGET_HEADERS:
        if (r.get(k,'') or '').strip():
            s+=1
    if (r.get('Mobile Phone','') or '').strip(): s+=5
    if (r.get('Corporate Phone','') or '').strip(): s+=3
    if (r.get('Other Phone','') or '').strip(): s+=2
    return s


def key_for(r):
    email=(r.get('Email') or '').strip().lower()
    if email: return ('email', email)
    li=(r.get('Person LinkedIn URL') or '').strip().lower()
    if li: return ('li', li)
    name=((r.get('First Name','')+' '+r.get('Last Name','')).strip().lower())
    comp=(r.get('Company Name','') or '').strip().lower()
    return ('nameco', name+'|'+comp)


def infer_phone_bucket(header_norm: str):
    h=header_norm
    if 'mobile' in h or 'cell' in h or 'personal' in h:
        return 'Mobile Phone'
    if 'work direct' in h or ('direct' in h and 'phone' in h) or 'desk' in h or 'office phone' in h:
        return 'Other Phone'
    if 'corporate' in h or 'company phone' in h or 'main phone' in h or 'switchboard' in h or 'hq phone' in h:
        return 'Corporate Phone'
    if 'phone' in h or 'tel' in h or 'telephone' in h:
        return 'Other Phone'
    return None


def infer_linkedin_bucket(header_norm: str):
    h=header_norm
    if 'linkedin' in h:
        if 'company' in h or 'account' in h:
            return 'Company LinkedIn URL'
        return 'Person LinkedIn URL'
    return None

# list files
list_url=f'{base}/{zone}/{path}'
req=urllib.request.Request(list_url, headers={'AccessKey': access_key})
with urllib.request.urlopen(req, timeout=30) as resp:
    items=json.loads(resp.read())
files=[it for it in items if (not it.get('IsDirectory')) and it.get('ObjectName','').lower().endswith('.csv')]
files=sorted(files, key=lambda x: x.get('Length',0))
print('files', len(files), flush=True)

best={}
rows_seen=0
rows_kept=0

for idx, it in enumerate(files, 1):
    name=it['ObjectName']
    url=f"{base}/{zone}/{path}{urllib.parse.quote(name)}"

    # header sniff
    req_head=urllib.request.Request(url, headers={'AccessKey': access_key, 'Range': 'bytes=0-65535'})
    try:
        with urllib.request.urlopen(req_head, timeout=60) as rh:
            head_bytes=rh.read()
    except Exception:
        continue
    head_text=head_bytes.decode('utf-8', errors='ignore')
    first_line=head_text.splitlines()[0] if head_text else ''
    if not first_line:
        continue
    try:
        sample_reader=csv.reader([first_line])
        headers=next(sample_reader)
    except Exception:
        continue
    norm_headers=[norm_header(h) for h in headers]
    if not any(h in CONTACT_HINTS or 'phone' in h or 'linkedin' in h or 'email' in h for h in norm_headers):
        continue

    # stream full file
    req=urllib.request.Request(url, headers={'AccessKey': access_key})
    with urllib.request.urlopen(req, timeout=180) as r:
        text=io.TextIOWrapper(r, encoding='utf-8', errors='ignore', newline='')
        reader=csv.DictReader(text)
        if reader.fieldnames is None:
            continue
        col_map={}
        for h in reader.fieldnames:
            nh=norm_header(h)
            if nh in MAP:
                col_map[h]=MAP[nh]
            else:
                li= infer_linkedin_bucket(nh)
                if li:
                    col_map[h]=li
                    continue
                ph= infer_phone_bucket(nh)
                if ph:
                    col_map[h]=ph
        for row in reader:
            rows_seen+=1
            out={k:'' for k in TARGET_HEADERS}
            for h, tgt in col_map.items():
                val=row.get(h,'')
                if val is None: val=''
                val=str(val).strip()
                if not val: continue
                if tgt in ['Mobile Phone','Other Phone','Corporate Phone']:
                    nums=split_numbers(val)
                    if not nums: continue
                    cur=set(split_numbers(out[tgt]))
                    for n in nums:
                        if n not in cur:
                            out[tgt]= (out[tgt]+'; ' if out[tgt] else '') + n
                            cur.add(n)
                else:
                    if not out[tgt]:
                        out[tgt]=val
            mob=set(split_numbers(out['Mobile Phone']))
            corp=set(split_numbers(out['Corporate Phone']))
            oth=set(split_numbers(out['Other Phone']))
            corp=corp - mob
            oth=oth - mob - corp
            out['Corporate Phone']='; '.join(list(corp))
            out['Other Phone']='; '.join(list(oth))
            if not is_contact_row(out):
                continue
            rows_kept+=1
            k=key_for(out)
            if k not in best or score(out) > score(best[k]):
                best[k]=out

    if idx % 25 == 0 or idx == len(files):
        print(f"processed {idx}/{len(files)}", flush=True)

final_rows=list(best.values())

out_csv=os.path.join(out_dir,'unknown_contacts_cleaned.csv')
with open(out_csv,'w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=TARGET_HEADERS)
    writer.writeheader()
    for r in final_rows:
        writer.writerow({h: r.get(h,'') for h in TARGET_HEADERS})

print('rows_seen', rows_seen, 'rows_kept', rows_kept, 'rows_final', len(final_rows), flush=True)
