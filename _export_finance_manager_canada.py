import csv
import psycopg

dsn='postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

OUT_PATH = r"C:\Users\Administrator\.openclaw\workspace\finance_manager_canada.csv"

QUERY = """
SELECT
  lead_id,
  first_name,
  last_name,
  title,
  seniority,
  departments,
  linkedin_person_url,
  email_primary,
  email_secondary,
  phone_mobile,
  phone_work,
  phone_other,
  person_city,
  person_state,
  person_country,
  company_name,
  company_domain,
  company_website,
  company_linkedin_url,
  industry,
  employee_count,
  revenue,
  total_funding,
  latest_funding,
  last_raised_at,
  source,
  batch_id,
  updated_at
FROM leads
WHERE
  title IS NOT NULL
  AND lower(title) LIKE '%%finance manager%%'
  AND (
    person_country ILIKE 'canada'
    OR company_country ILIKE 'canada'
  )
ORDER BY updated_at DESC NULLS LAST
LIMIT 20000;
"""


def main():
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY)
            cols = [d.name for d in cur.description]
            rows = cur.fetchall()

    with open(OUT_PATH, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)

    print(f"rows={len(rows)}")
    print(f"out={OUT_PATH}")


if __name__ == '__main__':
    main()
