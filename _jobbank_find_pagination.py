import ssl, urllib.request, re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
url='https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=qa&locationstring=Canada'
req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
html=urllib.request.urlopen(req, context=ctx).read().decode('utf-8','replace')
# find pagination links
links=re.findall(r'href="([^"]+)"[^>]*>\s*(\d+|Next)\s*<', html)
print('some links', links[:20])
# find any occurrences of start= or page=
for pat in ['page=', 'start=', 'p=']:
    m=re.search(pat, html)
    print(pat, bool(m))
# print around "View next" or "Next"
idx=html.find('View next')
print('View next idx', idx)
if idx!=-1:
    print(html[idx-200:idx+400])
idx=html.find('Next')
print('Next idx', idx)
print(html[idx-200:idx+400] if idx!=-1 else '')
