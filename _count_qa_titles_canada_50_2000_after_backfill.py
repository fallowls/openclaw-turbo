import os, psycopg
SQL = r"""
select
  count(*) as rows,
  count(distinct company_domain) as companies
from leads
where employee_count between 50 and 2000
  and coalesce(company_country, person_country) ilike 'Canada'
  and (
    title ~* '(^|\\m)(QA|Quality Assurance)(\\M|$)'
    or title ~* 'Quality\\s+(Engineering|Engineer|Test|Testing)'
  );
"""
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute(SQL)
    print(cur.fetchone())
