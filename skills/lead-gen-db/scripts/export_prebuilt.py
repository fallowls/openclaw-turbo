"""Export prebuilt queries.
Usage: python export_prebuilt.py <query_name> <out_csv>
Query names: title_geo | revenue_range | missing_fields | newest_batch
"""
import os, sys
import pandas as pd
import psycopg

QUERY_MAP = {
    "title_geo": "select * from leads where lower(title) like '%it manager%' and lower(person_country)='mexico'",
    "revenue_range": "select * from leads where revenue >= 50000000 and revenue <= 200000000",
    "missing_fields": """
        select * from leads
        where email_primary is null
           or linkedin_person_url is null
           or (phone_mobile is null and phone_work is null and phone_other is null)
    """,
    "newest_batch": "select * from leads where batch_id = %s"
}

if len(sys.argv) < 3:
    print("Usage: python export_prebuilt.py <query_name> <out_csv> [batch_id]")
    sys.exit(1)

name = sys.argv[1]
out_csv = sys.argv[2]

conn = psycopg.connect(os.environ["NEON_DSN"])
with conn:
    if name == "newest_batch":
        batch_id = sys.argv[3] if len(sys.argv) > 3 else ""
        df = pd.read_sql(QUERY_MAP[name], conn, params=[batch_id])
    else:
        df = pd.read_sql(QUERY_MAP[name], conn)

df.to_csv(out_csv, index=False)
print(f"Exported {len(df)} rows to {out_csv}")
