import os, csv, psycopg

OUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'companies_missing_employee_revenue_year.csv')

SQL = r"""
with base as (
  select
    coalesce(nullif(trim(company_domain),''), nullif(trim(company_name),'')) as company_key,
    nullif(trim(company_name), '') as company_name,
    nullif(trim(company_domain), '') as company_domain,
    employee_count,
    revenue,
    year_founded
  from leads
), agg as (
  select
    company_key,
    min(company_name) as company_name,
    min(company_domain) as company_domain,
    count(*) as lead_rows
  from base
  where company_key is not null
    and employee_count is null
    and revenue is null
    and year_founded is null
  group by company_key
)
select company_name, company_domain, lead_rows
from agg
where lead_rows >= 3
order by lead_rows desc, company_name nulls last;
"""

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute(SQL)
    cols = [d.name for d in cur.description]
    rows = cur.fetchall()

with open(OUT, 'w', newline='', encoding='utf-8') as f:
  w = csv.writer(f)
  w.writerow(cols)
  w.writerows(rows)

print(f"Exported {len(rows)} companies to {OUT}")
