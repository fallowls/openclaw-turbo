import os
import pandas as pd
import psycopg

out_csv = r"C:\Users\Administrator\Downloads\finance_directors_intent.csv"

sql = """
select
  first_name,
  last_name,
  title,
  seniority,
  email_primary,
  phone_mobile,
  phone_work,
  phone_other,
  linkedin_person_url,
  company_name,
  company_website,
  company_domain,
  company_linkedin_url,
  industry,
  employee_count,
  revenue,
  total_funding,
  latest_funding,
  last_raised_at,
  person_country,
  person_state,
  company_country,
  source
from leads
where title is not null
  and lower(title) like '%finance director%'
  and email_primary is not null
  and (phone_mobile is not null or phone_work is not null or phone_other is not null)
order by
  (case when last_raised_at is null then 1 else 0 end),
  last_raised_at desc nulls last,
  latest_funding desc nulls last
limit 2000;
"""

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    df = pd.read_sql(sql, conn)

df.to_csv(out_csv, index=False)
print(out_csv, len(df))
