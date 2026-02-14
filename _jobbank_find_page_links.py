import ssl, urllib.request, re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
base='https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=qa&locationstring=Canada'
req=urllib.request.Request(base, headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req, context=ctx).read().decode('utf-8','replace')
# find any jobsearch links containing page=
urls=set(re.findall(r'href="(/jobsearch/[^\"]*page=[^\"]*)"', html))
print('page urls', len(urls))
for u in sorted(list(urls))[:30]:
    print(u)
# also find any "page=" occurrences context
for m in re.finditer('page=', html):
    start=max(0,m.start()-80); end=min(len(html), m.start()+120)
    snippet=html[start:end]
    if 'href' in snippet:
        print('\nSNIP:', snippet.replace('\n',' ')[:200])
        break
