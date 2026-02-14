import os, psycopg

dsn=os.environ['NEON_DSN']
emp="employee_count between 50 and 2000"
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    cur.execute(f"""
      select coalesce(title,'(null)') as title, count(*)
      from leads
      where {emp} and {geo} {excl_sql}
      group by 1
      order by 2 desc
      limit 30
    """)
    rows=cur.fetchall()

for t,c in rows:
  print(c, t)
