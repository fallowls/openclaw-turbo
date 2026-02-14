import os, re
import pandas as pd
import psycopg

# Update existing leads with extra details from Lusha without overwriting existing values.
# Match priority: email_primary -> linkedin_person_url -> name+company.


def clean(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s == "" or s.lower() in ["nan", "na"]:
        return None
    return s


def parse_list(val):
    if pd.isna(val) or str(val).strip() == "":
        return None
    parts = re.split(r"[;,]", str(val))
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else None


def extract_domain(url):
    if pd.isna(url):
        return None
    s = str(url).strip().lower()
    if not s:
        return None
    s = re.sub(r"^https?://", "", s)
    s = s.split("/")[0]
    return s if s else None

path = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
df = pd.read_csv(path, dtype=str)

conn = psycopg.connect(os.environ["NEON_DSN"])

with conn:
    with conn.cursor() as cur:
        for _, r in df.iterrows():
            email = clean(r.get("Work email"))
            linkedin = clean(r.get("Linkedin URL"))
            first = clean(r.get("First name"))
            last = clean(r.get("Last name"))
            company = clean(r.get("Company name"))

            # find existing lead
            if email:
                cur.execute("select lead_id from leads where lower(email_primary)=lower(%s) limit 1", (email,))
            elif linkedin:
                cur.execute("select lead_id from leads where linkedin_person_url=%s limit 1", (linkedin,))
            elif first and last and company:
                cur.execute("select lead_id from leads where first_name=%s and last_name=%s and company_name=%s limit 1", (first, last, company))
            else:
                continue

            row = cur.fetchone()
            if not row:
                continue
            lead_id = row[0]

            cur.execute(
                """
                update leads set
                  title = coalesce(title, %s),
                  seniority = coalesce(seniority, %s),
                  departments = coalesce(departments, %s),
                  linkedin_person_url = coalesce(linkedin_person_url, %s),
                  email_primary = coalesce(email_primary, %s),
                  email_secondary = coalesce(email_secondary, %s),
                  phone_mobile = coalesce(phone_mobile, %s),
                  phone_work = coalesce(phone_work, %s),
                  phone_other = coalesce(phone_other, %s),
                  person_city = coalesce(person_city, %s),
                  person_state = coalesce(person_state, %s),
                  person_country = coalesce(person_country, %s),
                  company_name = coalesce(company_name, %s),
                  company_domain = coalesce(company_domain, %s),
                  company_website = coalesce(company_website, %s),
                  company_linkedin_url = coalesce(company_linkedin_url, %s),
                  industry = coalesce(industry, %s),
                  company_description = coalesce(company_description, %s),
                  keywords = coalesce(keywords, %s),
                  technologies = coalesce(technologies, %s),
                  employee_count = coalesce(employee_count, %s),
                  revenue = coalesce(revenue, %s),
                  year_founded = coalesce(year_founded, %s),
                  company_phone = coalesce(company_phone, %s),
                  company_address = coalesce(company_address, %s),
                  company_city = coalesce(company_city, %s),
                  company_state = coalesce(company_state, %s),
                  company_country = coalesce(company_country, %s),
                  updated_at = now()
                where lead_id = %s
                """,
                (
                    clean(r.get("Job title")),
                    clean(r.get("Seniority")),
                    parse_list(r.get("Departments")),
                    linkedin,
                    email,
                    clean(r.get("Personal email")),
                    clean(r.get("Phone 1")),
                    clean(r.get("Phone 3")),
                    clean(r.get("Phone 2")),
                    clean(r.get("City")),
                    clean(r.get("State")),
                    clean(r.get("Country")),
                    company,
                    extract_domain(r.get("Company website")),
                    clean(r.get("Company website")),
                    clean(r.get("Company Linkedin URL")),
                    clean(r.get("Industry")),
                    clean(r.get("Company description")),
                    parse_list(r.get("Company keywords")),
                    parse_list(r.get("Technologies")),
                    None,
                    None,
                    None,
                    clean(r.get("Company phone")),
                    clean(r.get("Company address")),
                    clean(r.get("Company city")),
                    clean(r.get("Company state")),
                    clean(r.get("Company country")),
                    lead_id,
                )
            )

print("Backfill update complete")
