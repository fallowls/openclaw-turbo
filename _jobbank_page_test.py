import ssl, urllib.request, re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

def fetch(url):
  req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
  return urllib.request.urlopen(req, context=ctx).read().decode('utf-8','replace')

base='https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=qa&locationstring=Canada'
for u in [base, base+'&page=2', base+'&page=3']:
  html=fetch(u)
  jobs=re.findall(r'/jobsearch/jobposting/(\d+)', html)
  biz=re.findall(r'<li class="business">(.*?)</li>', html)
  print(u, 'jobs', len(set(jobs)), 'biz', len(biz), 'firstbiz', (biz[0] if biz else None))
