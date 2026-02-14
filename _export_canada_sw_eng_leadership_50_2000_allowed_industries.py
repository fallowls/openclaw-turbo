import os, csv, psycopg

dsn=os.environ['NEON_DSN']

emp="employee_count between 50 and 2000"
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"
role = "title ilike '%%software engineering%%' and (title ilike '%%director%%' or title ilike '%%manager%%' or title ilike '%%head%%' or title ilike '%%lead%%')"

q=f"""
select
  first_name, last_name, title,
  email_primary, linkedin_person_url,
  company_name, company_domain, industry,
  employee_count,
  person_city, person_state, person_country,
  company_city, company_state, company_country,
  source
from leads
where {emp} and {geo} {excl_sql} and ({role})
order by company_name nulls last, last_name nulls last
"""

out_path=r"C:\Users\Administrator\.openclaw\workspace\canada_sw_eng_leadership_50_2000.csv"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    cur.execute(q)
    rows=cur.fetchall()
    cols=[d.name for d in cur.description]

with open(out_path,'w',newline='',encoding='utf-8') as f:
  w=csv.writer(f)
  w.writerow(cols)
  w.writerows(rows)

print('rows', len(rows))
print('out', out_path)
