import re
from pathlib import Path
import psycopg

ref = Path(r"C:\Users\Administrator\.openclaw\workspace\skills\lead-gen-db\references\neon-db.md").read_text(encoding="utf-8", errors="ignore")
m = re.search(r"postgresql://[^\s\"']+", ref)
if not m:
    raise SystemExit("NEON_DSN not found in neon-db.md")
dsn = m.group(0)

linkedin = "https://www.linkedin.com/in/sagar-khatri-cpa-cga-fcca-45284059/".rstrip("/")

queries = [
    (
        "by_linkedin_exact_or_like",
        """
        select first_name,last_name,title,company_name,company_domain,linkedin_person_url,email_primary,email_secondary
        from leads
        where linkedin_person_url is not null
          and (linkedin_person_url = %s or linkedin_person_url ilike %s)
        order by updated_at desc nulls last
        limit 10
        """,
        (linkedin, f"%{linkedin}%"),
    ),
    (
        "by_linkedin_contains_slug",
        """
        select first_name,last_name,title,company_name,company_domain,linkedin_person_url,email_primary,email_secondary
        from leads
        where linkedin_person_url ilike %s
        order by updated_at desc nulls last
        limit 10
        """,
        ("%sagar-khatri%",),
    ),
    (
        "by_name",
        """
        select first_name,last_name,title,company_name,company_domain,linkedin_person_url,email_primary,email_secondary
        from leads
        where lower(first_name) = 'sagar' and lower(last_name) = 'khatri'
        order by updated_at desc nulls last
        limit 10
        """,
        tuple(),
    ),
]

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        found = False
        for label, q, params in queries:
            cur.execute(q, params)
            rows = cur.fetchall()
            if rows:
                print(f"FOUND:{label}:{len(rows)}")
                for r in rows:
                    print("|".join([str(x) if x is not None else "" for x in r]))
                found = True
                break
        if not found:
            print("NOT_FOUND")
