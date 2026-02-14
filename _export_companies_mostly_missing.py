import os, csv, psycopg

OUT = os.path.join(os.path.expanduser('~'), 'Downloads', 'companies_most_data_missing.csv')

# Heuristic: company is "mostly missing" if >=60% of key fields are null/blank
# across its rows (averaged), and at least 5 leads exist for that company.
# Key fields considered: employee_count, revenue, industry, company_country, company_state,
# company_city, year_founded, company_linkedin_url, company_website
SQL = r"""
with base as (
  select
    nullif(trim(company_domain), '') as company_domain,
    nullif(trim(company_name), '') as company_name,
    employee_count,
    revenue,
    nullif(trim(industry), '') as industry,
    nullif(trim(company_country), '') as company_country,
    nullif(trim(company_state), '') as company_state,
    nullif(trim(company_city), '') as company_city,
    year_founded,
    nullif(trim(company_linkedin_url), '') as company_linkedin_url,
    nullif(trim(company_website), '') as company_website
  from leads
  where (company_domain is not null and trim(company_domain) <> '')
     or (company_name is not null and trim(company_name) <> '')
), scored as (
  select
    coalesce(company_domain, company_name) as company_key,
    min(company_name) as company_name,
    min(company_domain) as company_domain,
    count(*) as lead_rows,

    avg((employee_count is null)::int) as miss_employee_count,
    avg((revenue is null)::int) as miss_revenue,
    avg((industry is null)::int) as miss_industry,
    avg((company_country is null)::int) as miss_country,
    avg((company_state is null)::int) as miss_state,
    avg((company_city is null)::int) as miss_city,
    avg((year_founded is null)::int) as miss_year_founded,
    avg((company_linkedin_url is null)::int) as miss_company_linkedin,
    avg((company_website is null)::int) as miss_company_website,

    (
      avg((employee_count is null)::int) +
      avg((revenue is null)::int) +
      avg((industry is null)::int) +
      avg((company_country is null)::int) +
      avg((company_state is null)::int) +
      avg((company_city is null)::int) +
      avg((year_founded is null)::int) +
      avg((company_linkedin_url is null)::int) +
      avg((company_website is null)::int)
    ) / 9.0 as missing_ratio
  from base
  group by coalesce(company_domain, company_name)
)
select
  company_name,
  company_domain,
  lead_rows,
  round(missing_ratio::numeric, 3) as missing_ratio,
  round(miss_employee_count::numeric, 3) as miss_employee_count,
  round(miss_revenue::numeric, 3) as miss_revenue,
  round(miss_industry::numeric, 3) as miss_industry,
  round(miss_country::numeric, 3) as miss_company_country,
  round(miss_state::numeric, 3) as miss_company_state,
  round(miss_city::numeric, 3) as miss_company_city,
  round(miss_year_founded::numeric, 3) as miss_year_founded,
  round(miss_company_linkedin::numeric, 3) as miss_company_linkedin_url,
  round(miss_company_website::numeric, 3) as miss_company_website
from scored
where lead_rows >= 1
  and missing_ratio >= 0.70
order by missing_ratio desc, lead_rows desc, company_name nulls last;
"""

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute(SQL)
    cols = [d.name for d in cur.description]
    rows = cur.fetchall()

with open(OUT, 'w', newline='', encoding='utf-8') as f:
  w = csv.writer(f)
  w.writerow(cols)
  w.writerows(rows)

print(f"Exported {len(rows)} companies to {OUT}")
