import os, psycopg

SQL = r"""
select count(*)
from leads
where employee_count > 2000
  and coalesce(company_country, person_country) ilike 'United States'
  and (
    seniority ilike 'c%' 
    or title ilike 'chief %'
    or title ~* '(^|\\m)(CEO|CFO|COO|CTO|CIO|CMO|CRO|CPO|CISO|CHRO|CCO|CDO)(\\M|$)'
  )
"""

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute(SQL)
        print(cur.fetchone()[0])
