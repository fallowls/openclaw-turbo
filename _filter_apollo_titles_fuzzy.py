import pandas as pd
import re

data_path = r"C:\Users\Administrator\Downloads\LTI\apollo_filtered_LTI_Tal.csv"
out_path = r"C:\Users\Administrator\Downloads\LTI\apollo_filtered_LTI_Tal_titles.csv"

df = pd.read_csv(data_path, dtype=str)

# find title column
cols = list(df.columns)
title_col = None
for c in cols:
    if c.lower() in ["title", "job title", "jobtitle", "position"]:
        title_col = c
        break
if title_col is None:
    for c in cols:
        if 'title' in c.lower():
            title_col = c
            break
if title_col is None:
    raise SystemExit("No title column found")

# target titles list
raw_titles = [
"Director of Cloud Engineering",
"Director of Cloud Infrastructure",
"Head of Cloud Platforms",
"Vice President of Cloud and Infrastructure",
"Director of Information Technology Infrastructure",
"Head of Infrastructure Services",
"Vice President of Infrastructure and Operations",
"Director of Platform Engineering",
"Head of Hybrid Cloud",
"Chief Cloud Officer",
"Director of Information Technology Operations",
"Head of Information Technology Operations",
"Vice President of Information Technology Operations",
"Director of Enterprise Information Technology",
"Head of Global Information Technology",
"Director of Technology Operations",
"Vice President of Information Technology",
"Chief Information Officer",
"Deputy Chief Information Officer",
"Associate Chief Information Officer",
"Director of Enterprise Architecture",
"Head of Enterprise Architecture",
"Vice President of Enterprise Architecture",
"Chief Architect",
"Global Enterprise Architect",
"Director of Technology Architecture",
"Director of Enterprise Applications",
"Head of Enterprise Applications",
"Director of Enterprise Resource Planning",
"Head of Enterprise Resource Planning Systems",
"Vice President of Enterprise Applications",
"Director of JD Edwards Applications",
"JD Edwards Program Director",
"Director of Business Systems",
"Head of Digital Core Systems",
"Director of Supply Chain Systems",
"Head of Supply Chain Technology",
"Vice President of Supply Chain Technology",
"Director of Logistics Systems",
"Head of Global Supply Chain Information Technology",
"Director of Operations Technology",
"Vice President of Digital Supply Chain",
"Chief Supply Chain Technology Officer",
"Director of Industrial Internet of Things",
"Head of Smart Factory",
"Director of Digital Manufacturing",
"Vice President of Manufacturing Technology",
"Head of Operational Technology and Information Technology Integration",
"Director of Factory Automation Systems",
"Director of Industry Four Point Zero",
"Head of Connected Operations",
"Director of Artificial Intelligence Engineering",
"Head of Artificial Intelligence Platforms",
"Director of Machine Learning Engineering",
"Vice President of Artificial Intelligence and Advanced Analytics",
"Head of Model Operations",
"Director of Data Science and Artificial Intelligence",
"Chief Artificial Intelligence Officer",
"Director of Applied Artificial Intelligence",
]

# build a regex for fuzzy-like matching by keywords
keywords = []
for t in raw_titles:
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", "", t)
    keywords.append(t)

# match if any normalized title is contained in normalized job title

def norm(s):
    if pd.isna(s):
        return ""
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

norm_titles = df[title_col].map(norm)

mask = norm_titles.apply(lambda t: any(k in t for k in keywords))
filtered = df[mask].copy()
filtered.to_csv(out_path, index=False)

print("title_col", title_col)
print("filtered_rows", len(filtered))
print(out_path)
