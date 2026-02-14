import os, psycopg

dsn=os.environ['NEON_DSN']
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    cur.execute(f"""
      select title, count(*)
      from leads
      where {geo} {excl_sql}
        and title is not null
        and (
          title ilike '%%qa%%' or
          title ilike '%%quality%%' or
          title ilike '%%test%%' or
          title ilike '%%sdet%%' or
          title ilike '%%software development%%'
        )
      group by 1
      order by 2 desc
      limit 50
    """)
    rows=cur.fetchall()

for t,c in rows:
  print(c, t)
