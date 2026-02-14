import csv
import os
import re
from urllib.parse import urlparse
import psycopg

DSN = os.environ.get(
    "NEON_DSN",
    "postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
)

IN_PATH = r"C:\Users\Administrator\.openclaw\media\inbound\6c2f3a81-d668-45fa-af51-0477c93110b0.csv"
OUT_PATH = r"C:\Users\Administrator\.openclaw\workspace\prospects_enriched_with_neon_phones.csv"


def norm_email(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    if s in {"na", "n/a", "null", "none", "unavailable", ""}:
        return ""
    return s


def norm_linkedin(url: str) -> str:
    if not url:
        return ""
    u = url.strip()
    if not u:
        return ""
    u = re.sub(r"\s+", "", u)
    # common cleanup
    if u.startswith("http://"):
        u = "https://" + u[len("http://"):]
    # strip tracking params
    try:
        p = urlparse(u)
        if not p.netloc:
            return u
        clean = f"{p.scheme}://{p.netloc}{p.path}"
        clean = clean.rstrip("/")
        return clean
    except Exception:
        return u


def main():
    rows = []
    emails = set()
    li_urls = set()

    with open(IN_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
            e = norm_email(r.get("Email", ""))
            if e:
                emails.add(e)
            li = norm_linkedin(r.get("Person Linkedin Url", ""))
            if li:
                li_urls.add(li)

    email_map = {}
    li_map = {}

    # Neon leads table canonical columns (see _leads_cols.txt)
    cols = [
        "email_primary",
        "linkedin_person_url",
        "phone_mobile",
        "phone_work",
        "phone_other",
        "company_name",
        "company_domain",
        "first_name",
        "last_name",
        "title",
    ]

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            if emails:
                cur.execute(
                    f"""
                    SELECT {', '.join(cols)}
                    FROM leads
                    WHERE email_primary = ANY(%s)
                    """,
                    (list(emails),),
                )
                for rec in cur.fetchall():
                    d = dict(zip(cols, rec))
                    if d.get("email_primary") and d["email_primary"] not in email_map:
                        email_map[d["email_primary"]] = d

            if li_urls:
                cur.execute(
                    f"""
                    SELECT {', '.join(cols)}
                    FROM leads
                    WHERE linkedin_person_url = ANY(%s)
                    """,
                    (list(li_urls),),
                )
                for rec in cur.fetchall():
                    d = dict(zip(cols, rec))
                    if d.get("linkedin_person_url") and d["linkedin_person_url"] not in li_map:
                        li_map[d["linkedin_person_url"]] = d

    # write enriched file
    extra_fields = [
        "neon_match_type",
        "neon_email_primary",
        "neon_linkedin_person_url",
        "neon_phone_mobile",
        "neon_phone_work",
        "neon_phone_other",
        "neon_company_name",
        "neon_company_domain",
        "neon_title",
    ]

    fieldnames = list(rows[0].keys()) + [f for f in extra_fields if f not in rows[0]] if rows else extra_fields

    def pick(r):
        e = norm_email(r.get("Email", ""))
        li = norm_linkedin(r.get("Person Linkedin Url", ""))

        hit = None
        match_type = ""
        if e and e in email_map:
            hit = email_map[e]
            match_type = "email"
        elif li and li in li_map:
            hit = li_map[li]
            match_type = "linkedin"

        out = dict(r)
        out["neon_match_type"] = match_type

        if hit:
            out["neon_email_primary"] = hit.get("email_primary") or ""
            out["neon_linkedin_person_url"] = hit.get("linkedin_person_url") or ""
            out["neon_phone_mobile"] = hit.get("phone_mobile") or ""
            out["neon_phone_work"] = hit.get("phone_work") or ""
            out["neon_phone_other"] = hit.get("phone_other") or ""
            out["neon_company_name"] = hit.get("company_name") or ""
            out["neon_company_domain"] = hit.get("company_domain") or ""
            out["neon_title"] = hit.get("title") or ""
        else:
            for k in extra_fields:
                out.setdefault(k, "")

        return out

    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(pick(r))

    total = len(rows)
    matched = sum(1 for r in rows if norm_email(r.get("Email", "")) in email_map or norm_linkedin(r.get("Person Linkedin Url", "")) in li_map)

    print(f"in_rows={total}")
    print(f"unique_emails={len(emails)} unique_linkedin_urls={len(li_urls)}")
    print(f"email_hits={len(email_map)} linkedin_hits={len(li_map)}")
    print(f"matched_rows={matched}")
    print(f"out={OUT_PATH}")


if __name__ == "__main__":
    main()
