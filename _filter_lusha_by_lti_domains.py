import pandas as pd
import re
from urllib.parse import urlparse

lti_path = r"C:\Users\Administrator\Downloads\LTI\LTI Tal.csv"
lusha_path = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
out_path = r"C:\Users\Administrator\Downloads\LTI\lusha_filtered_LTI_Tal.csv"

lti = pd.read_csv(lti_path, dtype=str)
lusha = pd.read_csv(lusha_path, dtype=str)

# find website/domain columns
lti_cols = list(lti.columns)
website_col = None
for c in lti_cols:
    if c.lower() in ["website", "company website", "domain"]:
        website_col = c
        break
if website_col is None:
    for c in lti_cols:
        if 'website' in c.lower():
            website_col = c
            break

if website_col is None:
    raise SystemExit("No website/domain column found in LTI Tal")


def get_domain(x):
    if pd.isna(x) or not str(x).strip():
        return None
    x = str(x).strip()
    if not re.match(r"https?://", x):
        x = "http://" + x
    try:
        netloc = urlparse(x).netloc
    except Exception:
        return None
    netloc = netloc.lower()
    netloc = netloc.split('@')[-1]
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    return netloc if netloc else None

lti_domains = set(filter(None, (get_domain(v) for v in lti[website_col].tolist())))

# find domain/website or email column in lusha
lusha_cols = list(lusha.columns)

lusha_website_col = None
for c in lusha_cols:
    if c.lower() in ["website", "company website", "domain", "company domain"]:
        lusha_website_col = c
        break

email_col = None
for c in lusha_cols:
    if c.lower() in ["email", "email address", "work email", "personal email"]:
        email_col = c
        break

if lusha_website_col:
    lusha_domains = lusha[lusha_website_col].map(get_domain)
else:
    def email_domain(x):
        if pd.isna(x) or not str(x).strip():
            return None
        x = str(x).strip()
        if '@' in x:
            return x.split('@')[-1].lower()
        return None
    if email_col is None:
        raise SystemExit("No website/domain or email column found in Lusha")
    lusha_domains = lusha[email_col].map(email_domain)

lusha['__domain'] = lusha_domains
filtered = lusha[lusha['__domain'].isin(lti_domains)].copy()
filtered.to_csv(out_path, index=False)

print("LTI domains", len(lti_domains))
print("Filtered rows", len(filtered))
print(out_path)
