import ssl, urllib.request, re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ua={'User-Agent':'Mozilla/5.0'}
url='https://www.workopolis.com/search?q=qa&l=canada'
req=urllib.request.Request(url, headers=ua)
html=urllib.request.urlopen(req, context=ctx, timeout=45).read().decode('utf-8','replace')
print('search len', len(html))
# get first viewjob link
m=re.search(r'https://www\.workopolis\.com/jobsearch/viewjob/[^\"\s]+', html)
print('first viewjob', m.group(0) if m else None)
if m:
  v=m.group(0)
  req=urllib.request.Request(v, headers=ua)
  vh=urllib.request.urlopen(req, context=ctx, timeout=45).read().decode('utf-8','replace')
  print('view len', len(vh))
  for needle in ['hiringOrganization','company','employer','Organization','jobLocation']:
    print(needle, vh.find(needle))
  # try schema.org JSON-LD
  j=re.search(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', vh, re.S)
  if j:
    js=j.group(1)
    print('ldjson snippet', js[:400].replace('\n',' '))
  # fallback: find 'Company' label
  t=re.search(r'Company\s*</[^>]+>\s*<[^>]+>\s*([^<]+)', vh, re.I)
  print('company_match', t.group(1).strip() if t else None)
