"""Import a canonical CSV into Neon Postgres prospects table.
Requires: pip install psycopg[binary] pandas
Usage: python import_csv.py <path_to_csv> <source>
"""
import os
import sys
import pandas as pd
import psycopg

if len(sys.argv) < 3:
    print("Usage: python import_csv.py <path_to_csv> <source>")
    sys.exit(1)

csv_path = sys.argv[1]
source = sys.argv[2]

df = pd.read_csv(csv_path, dtype=str)

# Expect canonical columns from phone-mapping.md
cols = [
    "First Name","Last Name","Title","Company","Email",
    "Mobile Phone","Other Phone","Corporate Phone",
    "Person Linkedin Url","Company Linkedin Url","Website",
    "State","Country","Time Zone"
]

for c in cols:
    if c not in df.columns:
        df[c] = None

conn = psycopg.connect(os.environ["NEON_DSN"])
with conn:
    with conn.cursor() as cur:
        for _, r in df.iterrows():
            cur.execute(
                """
                insert into prospects (
                  first_name,last_name,title,email,mobile_phone,other_phone,corporate_phone,
                  person_linkedin_url,company_linkedin_url,website,state,country,time_zone,source
                ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    r["First Name"], r["Last Name"], r["Title"], r["Email"],
                    r["Mobile Phone"], r["Other Phone"], r["Corporate Phone"],
                    r["Person Linkedin Url"], r["Company Linkedin Url"], r["Website"],
                    r["State"], r["Country"], r["Time Zone"], source
                )
            )
print("Import complete")
