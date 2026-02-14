import csv, ssl, urllib.request, urllib.parse, re, time

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent':'Mozilla/5.0'}

TERMS = [
  'qa',
  'qa engineer',
  'quality assurance',
  'qa tester',
  'software tester',
  'test engineer',
  'sdet',
  'automation tester',
  'quality assurance engineer',
]

MAX_COMPANIES = 220  # buffer for dedupe/cleanup
MAX_PAGES_PER_TERM = 40
SLEEP_S = 0.8


def fetch(url: str) -> str:
  req = urllib.request.Request(url, headers=UA)
  with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
    return r.read().decode('utf-8','replace')


def parse_jobs(html: str):
  # Each card contains a jobposting link and business
  # Example: <a href="/jobsearch/jobposting/48913997;jsessionid=..."> and <li class="business">Company</li>
  links = re.findall(r'href="(/jobsearch/jobposting/\d+[^\"]*)"', html)
  companies = re.findall(r'<li class="business">\s*([^<]+?)\s*</li>', html)
  titles = re.findall(r'<span class="noctitle">\s*([^<]+?)\s*</span>', html)
  # align by order best-effort
  jobs=[]
  n = min(len(links), len(companies), len(titles))
  for i in range(n):
    jobs.append({
      'company': re.sub(r'\s+',' ',companies[i]).strip(),
      'title': re.sub(r'\s+',' ',titles[i]).strip(),
      'job_url': 'https://www.jobbank.gc.ca' + links[i].replace('&amp;','&')
    })
  return jobs


def find_search_base(term: str):
  # start with a generic query to get fcids for Canada-wide search
  url = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?' + urllib.parse.urlencode({
    'searchstring': term,
    'locationstring': 'Canada'
  })
  html = fetch(url)
  # Extract a canonical link that contains term=..., page=1, sort=M, fcid=...
  m = re.search(r'href="(/jobsearch/jobsearch\?term=[^\"]*?page=1[^\"]*)"', html)
  if not m:
    return None
  href = m.group(1)
  href = href.replace('&amp;','&')
  # Ensure term is set to the provided term
  # (some pages may use term=qa even if searchstring differed)
  parsed = urllib.parse.urlsplit('https://www.jobbank.gc.ca' + href)
  q = urllib.parse.parse_qs(parsed.query)
  q['term'] = [term]
  q['page'] = ['1']
  q.setdefault('sort',['M'])
  new_query = urllib.parse.urlencode({k:v[0] for k,v in q.items()})
  return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, new_query, parsed.fragment))


def set_page(url: str, page: int) -> str:
  parsed = urllib.parse.urlsplit(url)
  q = urllib.parse.parse_qs(parsed.query)
  q['page'] = [str(page)]
  new_query = urllib.parse.urlencode({k:v[0] for k,v in q.items()})
  return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, new_query, parsed.fragment))


def main():
  seen = {}  # company -> row
  for term in TERMS:
    base = find_search_base(term)
    if not base:
      continue

    for page in range(1, MAX_PAGES_PER_TERM+1):
      url = set_page(base, page)
      html = fetch(url)
      jobs = parse_jobs(html)
      if not jobs:
        break

      for j in jobs:
        c = j['company']
        if not c:
          continue
        if c not in seen:
          seen[c] = {
            'company': c,
            'example_job_title': j['title'],
            'example_job_url': j['job_url'],
            'source': 'JobBank.gc.ca',
            'term': term,
          }
        if len(seen) >= MAX_COMPANIES:
          break

      if len(seen) >= MAX_COMPANIES:
        break

      time.sleep(SLEEP_S)

    if len(seen) >= MAX_COMPANIES:
      break

  rows = list(seen.values())
  out_path = r'C:\Users\Administrator\.openclaw\workspace\canada_qa_companies_jobbank.csv'
  with open(out_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['company','example_job_title','example_job_url','source','term'])
    w.writeheader()
    w.writerows(rows)

  print('companies', len(rows))
  print('out', out_path)


if __name__ == '__main__':
  main()
