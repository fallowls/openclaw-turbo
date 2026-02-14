import os, csv, psycopg

dsn=os.environ['NEON_DSN']

# canada geo
geo="(person_country ilike 'canada' or person_country='CA' or company_country ilike 'canada' or company_country='CA')"

# exclude industries
excl = ['IT Consulting','Embedded Software','Education','Govt','Government','Non-Profit','Nonprofit']
excl_sql = "and not (" + " or ".join([f"industry ilike '%%{e}%%'" for e in excl]) + ")"

# broader title match (as requested roles; handles variations)
variant_sql = {
  'software_development_manager': "title ilike '%%software%%' and title ilike '%%development%%' and title ilike '%%manager%%'",
  'senior_qa_manager': "title ilike '%%senior%%' and title ilike '%%qa%%' and title ilike '%%manager%%'",
  'qa_automation_lead': "title ilike '%%qa%%' and title ilike '%%automation%%' and (title ilike '%%lead%%' or title ilike '%%manager%%' or title ilike '%%head%%')",
  'senior_software_engineering_manager': "title ilike '%%senior%%' and title ilike '%%software%%' and title ilike '%%engineering%%' and title ilike '%%manager%%'",
}

out_path=r"C:\Users\Administrator\.openclaw\workspace\canada_target_titles_no_emp.csv"

with psycopg.connect(dsn) as conn:
  with conn.cursor() as cur:
    base=f"from leads where {geo} {excl_sql}"
    cur.execute(f"select count(*) {base}")
    base_count=cur.fetchone()[0]

    breakdown_variant=[]
    for k,tsql in variant_sql.items():
      cur.execute(f"select count(*) {base} and ({tsql})")
      breakdown_variant.append((k, cur.fetchone()[0]))

    any_variant = " or ".join([f"({v})" for v in variant_sql.values()])
    cur.execute(f"select count(*) {base} and ({any_variant})")
    any_variant_count=cur.fetchone()[0]

    # export rows for variant matches
    cur.execute(f"""
      select
        first_name, last_name, title,
        email_primary, linkedin_person_url,
        company_name, company_domain, industry,
        employee_count,
        person_city, person_state, person_country,
        company_city, company_state, company_country,
        source
      {base} and ({any_variant})
      order by company_name nulls last, last_name nulls last
      limit 5000
    """)
    rows=cur.fetchall()
    cols=[d.name for d in cur.description]

with open(out_path,'w',newline='',encoding='utf-8') as f:
  w=csv.writer(f)
  w.writerow(cols)
  w.writerows(rows)

print('base_ca_excl_ind', base_count)
print('any_variant_count', any_variant_count)
for k,c in breakdown_variant:
  print(f"variant::{k}: {c}")
print('export_rows', len(rows))
print('out', out_path)
