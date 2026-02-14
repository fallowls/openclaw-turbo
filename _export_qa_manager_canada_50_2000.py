import os, csv, psycopg

OUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'canada_qa_manager_50_2000.csv')

SQL = r"""
select
  first_name,
  last_name,
  title,
  seniority,
  departments,
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
  source,
  batch_id,
  updated_at
from leads
where employee_count between 50 and 2000
  and coalesce(company_country, person_country) ilike 'Canada'
  and title ilike '%quality assurance%'
  and title ilike '%manager%'
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
