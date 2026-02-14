import os, psycopg

dsn=os.environ['NEON_DSN']
emp="employee_count between 50 and 2000"
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    base=f"from leads where {emp} and {geo} {excl_sql}"
    cur.execute(f"select count(*) {base}")
    print('base', cur.fetchone()[0])

    cur.execute(f"select count(*) {base} and title ilike '%%qa%%'")
    print('any_QA_in_title', cur.fetchone()[0])

    cur.execute(f"select count(*) {base} and title ilike '%%software engineering%%' and (title ilike '%%director%%' or title ilike '%%manager%%' or title ilike '%%head%%' or title ilike '%%lead%%')")
    print('software_engineering_leadership', cur.fetchone()[0])

    cur.execute(f"select count(*) {base} and title ilike '%%quality assurance%%' and (title ilike '%%director%%' or title ilike '%%manager%%' or title ilike '%%lead%%')")
    print('quality_assurance_leadership', cur.fetchone()[0])

    cur.execute(f"select count(*) {base} and title ilike '%%qa%%' and (title ilike '%%director%%' or title ilike '%%manager%%' or title ilike '%%lead%%')")
    print('qa_leadership', cur.fetchone()[0])
