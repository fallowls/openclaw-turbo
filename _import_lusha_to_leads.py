import os, re
import pandas as pd
import psycopg


def parse_int(val):
    if pd.isna(val):
        return None
    s = str(val).strip().replace(",", "")
    if s == "":
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def parse_bool(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    if s in ["true", "yes", "1"]:
        return True
    if s in ["false", "no", "0"]:
        return False
    return None


def parse_list(val):
    if pd.isna(val) or str(val).strip() == "":
        return None
    parts = re.split(r"[;,]", str(val))
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else None


def parse_revenue(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower().replace(",", "")
    if not s:
        return None
    if "-" in s:
        s = s.split("-")[0]
    mult = 1
    if s.endswith("b"):
        mult = 1_000_000_000
        s = s[:-1]
    elif s.endswith("m"):
        mult = 1_000_000
        s = s[:-1]
    elif s.endswith("k"):
        mult = 1_000
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except Exception:
        return None


def parse_date(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s:
        return None
    if s.isdigit() and len(s) > 6:
        return None
    try:
        dt = pd.to_datetime(s, errors="coerce")
        if pd.isna(dt):
            return None
        return dt.date()
    except Exception:
        return None


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

rows = []
for _, r in df.iterrows():
    row = (
        r.get("First name"),
        r.get("Last name"),
        r.get("Job title"),
        r.get("Seniority"),
        parse_list(r.get("Departments")),
        r.get("Linkedin URL"),
        r.get("Work email"),
        r.get("Personal email"),
        parse_int(r.get("Email confidence")),
        parse_bool(r.get("Email verified")),
        r.get("Phone 1"),
        r.get("Phone 3"),
        r.get("Phone 2"),
        r.get("City"),
        r.get("State"),
        r.get("Country"),
        r.get("Company name"),
        None,
        extract_domain(r.get("Company website")),
        r.get("Company website"),
        r.get("Company Linkedin URL"),
        r.get("Industry"),
        r.get("Company description"),
        parse_list(r.get("Company keywords")),
        parse_list(r.get("Technologies")),
        parse_int(r.get("Company size")),
        parse_revenue(r.get("Company revenue")),
        parse_int(r.get("Company founded")),
        r.get("Company phone"),
        r.get("Company address"),
        r.get("Company city"),
        r.get("Company state"),
        r.get("Company country"),
        parse_revenue(r.get("Total funding")),
        parse_revenue(r.get("Latest funding")),
        parse_date(r.get("Last funding date")),
        None,
        None,
        "Lusha",
        r.get("Lusha Person ID"),
        r.get("Lusha Company ID"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    rows.append(row)

conn = psycopg.connect(os.environ["NEON_DSN"])
cols = [
    "first_name","last_name","title","seniority","departments",
    "linkedin_person_url","email_primary","email_secondary","email_confidence","email_verified",
    "phone_mobile","phone_work","phone_other",
    "person_city","person_state","person_country",
    "company_name","company_name_for_emails","company_domain","company_website","company_linkedin_url",
    "industry","company_description","keywords","technologies","employee_count","revenue","year_founded",
    "company_phone","company_address","company_city","company_state","company_country",
    "total_funding","latest_funding","last_raised_at","ipo_status","ipo_date",
    "source","source_person_id","source_company_id","stage","last_contacted",
    "email_sent","email_open","email_bounced","replied","demoed","lists"
]

with conn:
    with conn.cursor() as cur:
        batch = 300
        for i in range(0, len(rows), batch):
            chunk = rows[i:i+batch]
            args_str = b",".join([b"(" + b",".join([b"%s"]*len(cols)) + b")"]*len(chunk))
            flat = [item for row in chunk for item in row]
            cur.execute(
                "INSERT INTO leads (" + ",".join(cols) + ") VALUES " + args_str.decode(),
                flat
            )

print(f"Imported {len(rows)} rows into leads")
