import os, psycopg

dsn=os.environ['NEON_DSN']
with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    cur.execute("select count(*) from leads")
    total=cur.fetchone()[0]
    cur.execute("select count(*) from leads where employee_count is not null")
    with_emp=cur.fetchone()[0]

    cur.execute("""
      select count(*)
      from leads
      where employee_count between 50 and 2000
    """)
    emp_50_2000=cur.fetchone()[0]

    cur.execute("""
      select
        count(*) filter (where person_country ilike 'canada' or person_country='CA' or person_country ilike '%%can%%') as pc,
        count(*) filter (where company_country ilike 'canada' or company_country='CA' or company_country ilike '%%can%%') as cc,
        count(*) filter (where coalesce(person_country,company_country) ilike 'canada' or coalesce(person_country,company_country)='CA') as any_ca
      from leads
    """)
    pc,cc,any_ca=cur.fetchone()

    cur.execute("""
      select count(*)
      from leads
      where employee_count between 50 and 2000
        and (
          person_country ilike 'canada' or person_country='CA' or
          company_country ilike 'canada' or company_country='CA'
        )
    """)
    emp_ca=cur.fetchone()[0]

print('total', total)
print('with_employee_count', with_emp)
print('employee_50_2000', emp_50_2000)
print('person_country_ca_like', pc)
print('company_country_ca_like', cc)
print('coalesce_country_ca', any_ca)
print('employee_50_2000_and_ca', emp_ca)
