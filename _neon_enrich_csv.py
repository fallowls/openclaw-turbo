import os
import pandas as pd
import psycopg

def norm_email(x: str) -> str:
    x = (x or '').strip().lower()
    return x

def norm_linkedin(x: str) -> str:
    x = (x or '').strip()
    if not x:
        return ''
    # normalize by removing trailing slash
    if x.endswith('/'):
        x = x[:-1]
    return x

inp = r"C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts.csv"
out = r"C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts_neon_enriched.csv"
needs_expl = r"C:\Users\Administrator\.openclaw\workspace\needs_explorium.csv"

df = pd.read_csv(inp, dtype=str, keep_default_na=False)

email_col = 'Email' if 'Email' in df.columns else None
li_col = 'Person Linkedin Url' if 'Person Linkedin Url' in df.columns else None

emails = sorted({norm_email(v) for v in (df[email_col].tolist() if email_col else []) if norm_email(v)})
links = sorted({norm_linkedin(v) for v in (df[li_col].tolist() if li_col else []) if norm_linkedin(v)})

print(f'input_rows={len(df)} unique_emails={len(emails)} unique_linkedins={len(links)}')

neon_dsn = os.environ.get('NEON_DSN')
if not neon_dsn:
    raise SystemExit('Missing NEON_DSN env var')

rows = []
with psycopg.connect(neon_dsn) as conn:
    with conn.cursor() as cur:
        # query in chunks to avoid huge parameter lists
        def chunk(lst, n=2000):
            for i in range(0, len(lst), n):
                yield lst[i:i+n]

        for e_chunk in chunk(emails, 2000):
            cur.execute(
                """
                select email_primary, linkedin_person_url, phone_mobile, phone_work, phone_other
                from leads
                where email_primary = any(%s)
                """,
                (e_chunk,),
            )
            rows.extend(cur.fetchall())

        # linkedin lookup for rows without email match
        for l_chunk in chunk(links, 2000):
            cur.execute(
                """
                select email_primary, linkedin_person_url, phone_mobile, phone_work, phone_other
                from leads
                where linkedin_person_url = any(%s)
                """,
                (l_chunk,),
            )
            rows.extend(cur.fetchall())

# Build lookup maps (prefer rows with phones)
by_email = {}
by_li = {}
for (email, li, m, w, o) in rows:
    em = norm_email(email)
    ln = norm_linkedin(li)
    rec = {
        'email': em,
        'linkedin_person_url': ln,
        'phone_mobile': (m or '').strip(),
        'phone_work': (w or '').strip(),
        'phone_other': (o or '').strip(),
    }
    if em and (em not in by_email or sum(bool(rec[k]) for k in ['phone_mobile','phone_work','phone_other']) > sum(bool(by_email[em][k]) for k in ['phone_mobile','phone_work','phone_other'])):
        by_email[em] = rec
    if ln and (ln not in by_li or sum(bool(rec[k]) for k in ['phone_mobile','phone_work','phone_other']) > sum(bool(by_li[ln][k]) for k in ['phone_mobile','phone_work','phone_other'])):
        by_li[ln] = rec

filled_mobile = filled_work = filled_other = 0

for idx, r in df.iterrows():
    em = norm_email(r[email_col]) if email_col else ''
    ln = norm_linkedin(r[li_col]) if li_col else ''
    rec = by_email.get(em) or by_li.get(ln)
    if not rec:
        continue

    # Only fill blanks; do not overwrite
    if 'Mobile Phone' in df.columns and not (r.get('Mobile Phone') or '').strip() and rec['phone_mobile']:
        df.at[idx, 'Mobile Phone'] = rec['phone_mobile']
        filled_mobile += 1
    if 'Work Direct Phone' in df.columns and not (r.get('Work Direct Phone') or '').strip() and rec['phone_work']:
        df.at[idx, 'Work Direct Phone'] = rec['phone_work']
        filled_work += 1
    if 'Other Phone' in df.columns and not (r.get('Other Phone') or '').strip() and rec['phone_other']:
        df.at[idx, 'Other Phone'] = rec['phone_other']
        filled_other += 1

# Save output
df.to_csv(out, index=False)

# Determine which still need Explorium (no phones at all, but has linkedin)
phone_cols = [c for c in ['Work Direct Phone','Mobile Phone','Corporate Phone','Other Phone'] if c in df.columns]
mask_no_phones = df[phone_cols].apply(lambda s: s.astype(str).str.strip().eq('')).all(axis=1) if phone_cols else pd.Series([True]*len(df))
mask_has_li = df[li_col].astype(str).str.strip().ne('') if li_col else pd.Series([False]*len(df))
needs = df[mask_no_phones & mask_has_li].copy()
needs.to_csv(needs_expl, index=False)

print(f'wrote={out}')
print(f'filled_mobile={filled_mobile} filled_work={filled_work} filled_other={filled_other}')
print(f'needs_explorium_rows={len(needs)} wrote_needs_explorium={needs_expl}')
