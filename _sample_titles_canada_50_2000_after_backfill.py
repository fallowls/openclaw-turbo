import os, psycopg
SQL = r"""
select title, count(*) as c
from leads
where employee_count between 50 and 2000
  and coalesce(company_country, person_country) ilike 'Canada'
  and title is not null
group by title
order by c desc
limit 50;
"""
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute(SQL)
    for row in cur.fetchall():
      print(row)
