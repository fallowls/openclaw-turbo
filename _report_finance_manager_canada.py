import csv
from collections import Counter, defaultdict

IN_PATH = r"C:\Users\Administrator\.openclaw\workspace\finance_manager_canada.csv"
OUT_TXT = r"C:\Users\Administrator\.openclaw\workspace\finance_manager_canada_report.txt"


def norm(s):
    if s is None:
        return ""
    s = str(s).strip()
    if s.lower() in {"", "nan", "na", "n/a", "null", "none", "unavailable"}:
        return ""
    return s


def hasval(s):
    return norm(s) != ""


def top(counter, n=15):
    return counter.most_common(n)


def pct(x, total):
    return 0.0 if total == 0 else (100.0 * x / total)


def main():
    with open(IN_PATH, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)

    total = len(rows)

    # coverage
    cov = {
        "email_primary": sum(1 for x in rows if hasval(x.get("email_primary"))),
        "linkedin_person_url": sum(1 for x in rows if hasval(x.get("linkedin_person_url"))),
        "phone_mobile": sum(1 for x in rows if hasval(x.get("phone_mobile"))),
        "phone_work": sum(1 for x in rows if hasval(x.get("phone_work"))),
        "phone_other": sum(1 for x in rows if hasval(x.get("phone_other"))),
        "any_phone": sum(1 for x in rows if hasval(x.get("phone_mobile")) or hasval(x.get("phone_work")) or hasval(x.get("phone_other"))),
        "company_domain": sum(1 for x in rows if hasval(x.get("company_domain"))),
        "company_linkedin_url": sum(1 for x in rows if hasval(x.get("company_linkedin_url"))),
    }

    # breakdowns
    by_state = Counter(norm(x.get("person_state")) or "(blank)" for x in rows)
    by_city = Counter(norm(x.get("person_city")) or "(blank)" for x in rows)
    by_industry = Counter(norm(x.get("industry")) or "(blank)" for x in rows)
    by_seniority = Counter(norm(x.get("seniority")) or "(blank)" for x in rows)
    by_employees_bucket = Counter()

    def emp_bucket(v):
        v = norm(v)
        if not v:
            return "(blank)"
        try:
            n = int(float(v))
        except Exception:
            return "(non-numeric)"
        if n < 11:
            return "1-10"
        if n < 51:
            return "11-50"
        if n < 201:
            return "51-200"
        if n < 501:
            return "201-500"
        if n < 1001:
            return "501-1000"
        if n < 5001:
            return "1001-5000"
        return "5000+"

    for x in rows:
        by_employees_bucket[emp_bucket(x.get("employee_count"))] += 1

    # email domain distribution (top)
    email_domains = Counter()
    for x in rows:
        e = norm(x.get("email_primary"))
        if e and "@" in e:
            email_domains[e.split("@", 1)[1].lower()] += 1

    # duplicates (by email)
    email_counts = Counter(norm(x.get("email_primary")).lower() for x in rows if hasval(x.get("email_primary")))
    dup_emails = sum(1 for k, c in email_counts.items() if c > 1)

    # rows missing key things
    missing_both_email_li = sum(1 for x in rows if not hasval(x.get("email_primary")) and not hasval(x.get("linkedin_person_url")))

    lines = []
    lines.append("FINANCE MANAGER — CANADA (Neon export report)")
    lines.append("=")
    lines.append(f"Total contacts: {total}")
    lines.append("")

    lines.append("Data coverage")
    for k in ["email_primary", "linkedin_person_url", "any_phone", "phone_mobile", "phone_work", "phone_other", "company_domain", "company_linkedin_url"]:
        lines.append(f"- {k}: {cov[k]} ({pct(cov[k], total):.1f}%)")
    lines.append(f"- Missing BOTH email + LinkedIn: {missing_both_email_li} ({pct(missing_both_email_li, total):.1f}%)")
    lines.append(f"- Duplicate primary emails (unique email values that repeat): {dup_emails}")
    lines.append("")

    lines.append("Top provinces/states (person_state)")
    for name, c in top(by_state, 20):
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")
    lines.append("")

    lines.append("Top cities (person_city)")
    for name, c in top(by_city, 20):
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")
    lines.append("")

    lines.append("Top industries")
    for name, c in top(by_industry, 20):
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")
    lines.append("")

    lines.append("Seniority breakdown")
    for name, c in by_seniority.most_common():
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")
    lines.append("")

    lines.append("Employee count buckets")
    for name, c in by_employees_bucket.most_common():
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")
    lines.append("")

    lines.append("Top email domains")
    for name, c in top(email_domains, 25):
        lines.append(f"- {name}: {c} ({pct(c, total):.1f}%)")

    text = "\n".join(lines) + "\n"

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"wrote={OUT_TXT}")


if __name__ == "__main__":
    main()
