import os, psycopg

dsn=os.environ['NEON_DSN']

emp="employee_count between 50 and 2000"
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"

# keyword buckets
bucket_sql = {
  'software_development_manager': "title ilike '%%software development manager%%'",
  'senior_qa_manager': "title ilike '%%senior%%' and title ilike '%%qa%%' and title ilike '%%manager%%'",
  'qa_automation_lead': "title ilike '%%qa%%' and title ilike '%%automation%%' and (title ilike '%%lead%%' or title ilike '%%manager%%')",
  'senior_software_engineering_manager': "title ilike '%%senior%%' and title ilike '%%software%%' and title ilike '%%engineering%%' and title ilike '%%manager%%'",
  'engineering_manager': "title ilike '%%engineering manager%%'",
}

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    base=f"from leads where {emp} and {geo} {excl_sql}"
    cur.execute(f"select count(*) {base}")
    base_count=cur.fetchone()[0]
    print('base_50_2000_ca_excl_ind', base_count)

    for k,tsql in bucket_sql.items():
      cur.execute(f"select count(*) {base} and ({tsql})")
      print(k, cur.fetchone()[0])

    # any of buckets
    any_sql = " or ".join([f"({v})" for v in bucket_sql.values()])
    cur.execute(f"select count(*) {base} and ({any_sql})")
    print('any_bucket', cur.fetchone()[0])
