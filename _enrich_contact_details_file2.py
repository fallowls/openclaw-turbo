import csv
import os
import re
from urllib.parse import urlparse
import psycopg

DSN = os.environ.get(
    "NEON_DSN",
    "postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
)

IN_PATH = r"C:\Users\Administrator\.openclaw\media\inbound\13306903-7f8e-4252-904a-b8dde45e94e3.csv"
OUT_PATH = r"C:\Users\Administrator\.openclaw\workspace\qa_contacts_enriched_direct_mobile.csv"

JUNK = {"nan", "na", "n/a", "null", "none", "unavailable", ""}


def norm_email(s: str) -> str:
    if not s:
        return ""
    s = str(s).strip().lower()
    if s in JUNK:
        return ""
    return s


def norm_linkedin(url: str) -> str:
    if not url:
        return ""
    u = str(url).strip()
    if not u or u.strip().lower() in JUNK:
        return ""
    u = re.sub(r"\s+", "", u)
    if u.startswith("http://"):
        u = "https://" + u[len("http://"):]
    try:
        p = urlparse(u)
        if not p.netloc:
            return u.rstrip("/")
        clean = f"{p.scheme}://{p.netloc}{p.path}".rstrip("/")
        return clean
    except Exception:
        return u.rstrip("/")


def is_empty(v) -> bool:
    if v is None:
        return True
    s = str(v).strip()
    if s == "":
        return True
    return s.lower() in JUNK


def clean_cell(v):
    if v is None:
        return ""
    s = str(v)
    if s.strip().lower() in JUNK:
        return ""
    return v


def main():
    rows = []
    emails = set()
    li_urls = set()

    with open(IN_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for r in reader:
            # clean junk tokens in-place
            for k in list(r.keys()):
                r[k] = clean_cell(r[k])
            rows.append(r)
            e = norm_email(r.get("Email", ""))
            if e:
                emails.add(e)
            li = norm_linkedin(r.get("Person Linkedin Url", ""))
            if li:
                li_urls.add(li)

    # fetch neon phone fields
    cols = [
        "email_primary",
        "linkedin_person_url",
        "phone_mobile",
        "phone_work",
        "phone_other",
    ]
    email_map = {}
    li_map = {}

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            if emails:
                cur.execute(
                    f"SELECT {', '.join(cols)} FROM leads WHERE email_primary = ANY(%s)",
                    (list(emails),),
                )
                for rec in cur.fetchall():
                    d = dict(zip(cols, rec))
                    key = d.get("email_primary")
                    if key and key not in email_map:
                        email_map[key] = d

            if li_urls:
                cur.execute(
                    f"SELECT {', '.join(cols)} FROM leads WHERE linkedin_person_url = ANY(%s)",
                    (list(li_urls),),
                )
                for rec in cur.fetchall():
                    d = dict(zip(cols, rec))
                    key = d.get("linkedin_person_url")
                    if key and key not in li_map:
                        li_map[key] = d

    # ensure columns exist in same sheet
    for col in ["Work Direct Phone", "Mobile Phone"]:
        if col not in fieldnames:
            fieldnames.append(col)

    match_col = "neon_match_type"
    if match_col not in fieldnames:
        fieldnames.append(match_col)

    matched = 0
    for r in rows:
        e = norm_email(r.get("Email", ""))
        li = norm_linkedin(r.get("Person Linkedin Url", ""))
        hit = None
        mt = ""
        if e and e in email_map:
            hit = email_map[e]
            mt = "email"
        elif li and li in li_map:
            hit = li_map[li]
            mt = "linkedin"

        r[match_col] = mt

        if hit:
            matched += 1
            # Mobile
            if is_empty(r.get("Mobile Phone")) and not is_empty(hit.get("phone_mobile")):
                r["Mobile Phone"] = hit.get("phone_mobile")
            # Direct/Work (fallback to other)
            if is_empty(r.get("Work Direct Phone")):
                if not is_empty(hit.get("phone_work")):
                    r["Work Direct Phone"] = hit.get("phone_work")
                elif not is_empty(hit.get("phone_other")):
                    r["Work Direct Phone"] = hit.get("phone_other")

    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    filled_mobile = sum(1 for r in rows if not is_empty(r.get("Mobile Phone")))
    filled_work = sum(1 for r in rows if not is_empty(r.get("Work Direct Phone")))

    print(f"rows={len(rows)}")
    print(f"unique_emails={len(emails)} unique_linkedin={len(li_urls)}")
    print(f"email_hits={len(email_map)} linkedin_hits={len(li_map)}")
    print(f"matched_rows={matched}")
    print(f"filled_mobile={filled_mobile} filled_work_direct={filled_work}")
    print(f"out={OUT_PATH}")


if __name__ == "__main__":
    main()
