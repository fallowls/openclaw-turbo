import os, psycopg

dsn = os.environ.get('NEON_DSN')
if not dsn:
    raise SystemExit('NEON_DSN env var not set')

titles = [
  'Software Development Manager',
  'Senior QA automation lead',
  'Senior software Engineering Manager',
  'Senior QA Manager',
]

# employee range
emp = "employee_count between 50 and 2000"
# canada geo
# NOTE: psycopg uses % for placeholders; literal % in SQL must be doubled (%%)
geo = "(coalesce(person_country, company_country) ilike 'canada' or person_country ilike '%%canada%%' or company_country ilike '%%canada%%')"

# exclude industries
excl = [
  'IT Consulting',
  'Embedded Software',
  'Education',
  'Govt',
  'Government',
  'Non-Profit',
  'Nonprofit',
]

# build filters
excl_sql = " and not (" + " or ".join([f"industry ilike '%%{e.replace("'","''")}%%'" for e in excl]) + ")"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    # total matching any of the titles (contains)
    title_any = "(" + " or ".join(["title ilike %s" for _ in titles]) + ")"
    params = [f"%{t}%" for t in titles]
    q = f"select count(*) from leads where {emp} and {geo} and {title_any} {excl_sql}"
    cur.execute(q, params)
    total = cur.fetchone()[0]

    breakdown = []
    for t in titles:
      cur.execute(
        f"select count(*) from leads where {emp} and {geo} and title ilike %s {excl_sql}",
        [f"%{t}%"],
      )
      breakdown.append((t, cur.fetchone()[0]))

print('total_any_of_titles', total)
for t,c in breakdown:
  print(f"{t}: {c}")
