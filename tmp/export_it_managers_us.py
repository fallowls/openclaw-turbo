import re
import csv
from pathlib import Path
import psycopg

ref = Path(r"C:\Users\Administrator\.openclaw\workspace\skills\lead-gen-db\references\neon-db.md").read_text(encoding="utf-8", errors="ignore")
m = re.search(r"postgresql://[^\s\"']+", ref)
if not m:
    raise SystemExit("NEON_DSN not found")
dsn = m.group(0)

out_path = Path(r"C:\Users\Administrator\.openclaw\workspace\tmp\it_manager_100.csv")

patterns = [
    '%IT Manager%',
    '%Information Technology Manager%',
    '%IT Operations Manager%',
    '%Infrastructure Manager%',
    '%Systems Manager%',
    '%Network Manager%',
]

q = """
select
  first_name,
  last_name,
  title,
  company_name,
  company_domain,
  linkedin_person_url,
  email_primary,
  person_city,
  person_state,
  person_country
from leads
where
  email_primary is not null
  and (
    title ilike any(%s)
  )
order by updated_at desc nulls last
limit 100;
"""

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute(q, (patterns,))
        rows = cur.fetchall()

headers = [
    'first_name','last_name','title','company_name','company_domain',
    'linkedin_person_url','email_primary','person_city','person_state','person_country'
]

with out_path.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for r in rows:
        w.writerow(r)

print(str(out_path))
print(f"rows={len(rows)}")
