import os, csv, psycopg

OUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'c_level_us_employee_gt2000.csv')

SQL = r"""
select
  first_name,
  last_name,
  title,
  seniority,
  email_primary,
  email_secondary,
  phone_mobile,
  phone_work,
  phone_other,
  linkedin_person_url,
  company_name,
  company_domain,
  industry,
  employee_count,
  company_city,
  company_state,
  company_country,
  person_city,
  person_state,
  person_country,
  source,
  batch_id,
  updated_at
from leads
where employee_count > 2000
  and coalesce(company_country, person_country) ilike 'United States'
  and (
    seniority ilike 'c%'
    or title ilike 'chief %'
    or title ~* '(^|\\m)(CEO|CFO|COO|CTO|CIO|CMO|CRO|CPO|CISO|CHRO|CCO|CDO)(\\M|$)'
  )
order by employee_count desc nulls last, company_name nulls last, last_name nulls last;
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

print(f"Exported {len(rows)} rows to {OUT}")
