import os, sys, csv, re
from urllib.parse import urlparse
import psycopg

INP = sys.argv[1]
BATCH = sys.argv[2]

num_re = re.compile(r"(\d+[\d,]*)")

def parse_int_from_any(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s or s.lower() in {'na','n/a','nan','null','none','-'}:
        return None
    m = num_re.search(s)
    if not m:
        return None
    try:
        return int(m.group(1).replace(',',''))
    except:
        return None

def parse_money_to_bigint(v):
    # Accepts "$10M - $50M", "$500M - $1B", "1000000".
    if v is None:
        return None
    s = str(v).strip()
    if not s or s.lower() in {'na','n/a','nan','null','none','-'}:
        return None
    # pick first token like 10M, 1B, 250K
    m = re.search(r"(\d+(?:\.\d+)?)\s*([KMB])?", s.replace('$','').replace(',',''), re.I)
    if not m:
        return parse_int_from_any(s)
    val = float(m.group(1))
    mult = (m.group(2) or '').upper()
    if mult == 'K':
        val *= 1_000
    elif mult == 'M':
        val *= 1_000_000
    elif mult == 'B':
        val *= 1_000_000_000
    return int(val)

def domain_from_url(u):
    if u is None:
        return None
    s = str(u).strip()
    if not s:
        return None
    if not re.match(r'^https?://', s, re.I):
        s2 = 'https://' + s
    else:
        s2 = s
    try:
        p = urlparse(s2)
        host = (p.netloc or '').lower()
        host = host.split('@')[-1]
        host = host.split(':')[0]
        if host.startswith('www.'):
            host = host[4:]
        return host or None
    except:
        return None

DSN = os.environ['NEON_DSN']

# Ensure table exists (fresh connection)
with psycopg.connect(DSN) as conn:
  with conn.cursor() as cur:
    cur.execute("""
      create extension if not exists pgcrypto;
      create table if not exists company (
        company_id uuid primary key default gen_random_uuid(),
        company_domain text unique,
        company_name text,
        company_website text,
        company_linkedin_url text,
        industry text,
        technologies text[],
        employee_count int,
        revenue bigint,
        year_founded int,
        company_city text,
        company_state text,
        company_country text,
        total_funding bigint,
        latest_funding bigint,
        last_raised_at date,
        source text,
        batch_id text,
        created_at timestamp default now(),
        updated_at timestamp default now()
      );
    """)

rows = []
with open(INP, 'r', encoding='utf-8-sig', newline='') as f:
    r = csv.DictReader(f)
    for rec in r:
        website = rec.get('Website')
        domain = domain_from_url(website)
        if not domain:
            continue
        tech = rec.get('Technologies')
        techs = None
        if tech and tech.strip():
            techs = [t.strip() for t in tech.split(',') if t.strip()]
        lra = (rec.get('Last Raised At') or '').strip()
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', lra):
            lra = None

        rows.append({
            'company_domain': domain,
            'company_name': (rec.get('Company Name') or '').strip() or None,
            'company_website': website.strip() if website else None,
            'company_linkedin_url': (rec.get('Company Linkedin Url') or '').strip() or None,
            'industry': (rec.get('Industry') or '').strip() or None,
            'technologies': techs,
            'employee_count': parse_int_from_any(rec.get('# Employees')),
            'revenue': parse_money_to_bigint(rec.get('Annual Revenue')),
            'year_founded': parse_int_from_any(rec.get('Founded Year')),
            'company_city': (rec.get('Company City') or '').strip() or None,
            'company_state': (rec.get('Company State') or '').strip() or None,
            'company_country': (rec.get('Company Country') or '').strip() or None,
            'total_funding': parse_money_to_bigint(rec.get('Total Funding')),
            'latest_funding': parse_money_to_bigint(rec.get('Latest Funding Amount') or rec.get('Latest Funding')),
            'last_raised_at': lra,
            'source': 'Apollo',
            'batch_id': BATCH,
        })

# Upsert
try:
  with psycopg.connect(DSN) as conn:
    with conn.cursor() as cur:
      cur.executemany("""
        insert into company (
          company_domain, company_name, company_website, company_linkedin_url,
          industry, technologies, employee_count, revenue, year_founded,
          company_city, company_state, company_country,
          total_funding, latest_funding, last_raised_at,
          source, batch_id
        ) values (
          %(company_domain)s, %(company_name)s, %(company_website)s, %(company_linkedin_url)s,
          %(industry)s, %(technologies)s, %(employee_count)s, %(revenue)s, %(year_founded)s,
          %(company_city)s, %(company_state)s, %(company_country)s,
          %(total_funding)s, %(latest_funding)s, %(last_raised_at)s,
          %(source)s, %(batch_id)s
        )
        on conflict (company_domain) do update set
          company_name = coalesce(company.company_name, excluded.company_name),
          company_website = coalesce(company.company_website, excluded.company_website),
          company_linkedin_url = coalesce(company.company_linkedin_url, excluded.company_linkedin_url),
          industry = coalesce(company.industry, excluded.industry),
          technologies = coalesce(company.technologies, excluded.technologies),
          employee_count = coalesce(company.employee_count, excluded.employee_count),
          revenue = coalesce(company.revenue, excluded.revenue),
          year_founded = coalesce(company.year_founded, excluded.year_founded),
          company_city = coalesce(company.company_city, excluded.company_city),
          company_state = coalesce(company.company_state, excluded.company_state),
          company_country = coalesce(company.company_country, excluded.company_country),
          total_funding = coalesce(company.total_funding, excluded.total_funding),
          latest_funding = coalesce(company.latest_funding, excluded.latest_funding),
          last_raised_at = coalesce(company.last_raised_at, excluded.last_raised_at),
          updated_at = now(),
          source = excluded.source,
          batch_id = excluded.batch_id;
      """, rows)
except Exception as e:
  print('UPSERT_ERROR', type(e), e)
  raise

print(f"upserted_company_rows={len(rows)}")

# Backfill leads (only when leads field is null)
with psycopg.connect(DSN) as conn:
  with conn.cursor() as cur:
    cur.execute("""
      update leads l
      set
        employee_count = coalesce(l.employee_count, c.employee_count),
        revenue = coalesce(l.revenue, c.revenue),
        year_founded = coalesce(l.year_founded, c.year_founded),
        industry = coalesce(l.industry, c.industry),
        company_city = coalesce(l.company_city, c.company_city),
        company_state = coalesce(l.company_state, c.company_state),
        company_country = coalesce(l.company_country, c.company_country),
        company_linkedin_url = coalesce(l.company_linkedin_url, c.company_linkedin_url),
        company_website = coalesce(l.company_website, c.company_website),
        updated_at = now(),
        last_updated_source = coalesce(l.last_updated_source, 'Apollo')
      from company c
      where l.company_domain is not null
        and lower(l.company_domain)=lower(c.company_domain)
        and (
          l.employee_count is null or l.revenue is null or l.year_founded is null or
          l.industry is null or l.company_country is null or l.company_state is null or l.company_city is null or
          l.company_linkedin_url is null or l.company_website is null
        );
    """)
    print(f"leads_backfill_updated={cur.rowcount}")
