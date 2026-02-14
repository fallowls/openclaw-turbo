import os, psycopg
conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute("select count(*) from leads")
        total = cur.fetchone()[0]
        cur.execute("select source, count(*) from leads group by source order by count(*) desc")
        by_source = cur.fetchall()
        cur.execute("""
            select
              sum(case when email_primary is null or email_primary='' then 1 else 0 end) as missing_email,
              sum(case when linkedin_person_url is null or linkedin_person_url='' then 1 else 0 end) as missing_linkedin,
              sum(case when phone_mobile is null and phone_work is null and phone_other is null then 1 else 0 end) as missing_phone,
              sum(case when company_name is null or company_name='' then 1 else 0 end) as missing_company,
              sum(case when person_country is null or person_country='' then 1 else 0 end) as missing_country
            from leads
        """)
        quality = cur.fetchone()
        cur.execute("select first_name,last_name,title,email_primary,company_name,source from leads limit 5")
        sample = cur.fetchall()

print('total', total)
print('by_source', by_source)
print('missing_email, missing_linkedin, missing_phone, missing_company, missing_country', quality)
print('sample_rows', sample)
