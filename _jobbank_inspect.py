import ssl, urllib.request
url='https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=qa+engineer&locationstring=Canada'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    html=r.read().decode('utf-8','replace')
print('len',len(html))
for needle in ['resultJobItem','jobTitle','data-jobid','job-posting','positionTitle','employer']:
    print(needle, html.find(needle))
i=html.find('resultJobItem')
print(html[i-200:i+1200] if i!=-1 else html[:2000])
