"""Add advanced columns for enrichment without overwriting.
Requires: pip install psycopg[binary]
Uses NEON_DSN env var.
"""
import os
import psycopg

DDL = """
alter table leads add column if not exists last_updated_source text;
alter table leads add column if not exists batch_id text;
alter table leads add column if not exists field_sources jsonb;

alter table leads add column if not exists title_secondary text;
alter table leads add column if not exists phone_mobile_secondary text;
alter table leads add column if not exists phone_work_secondary text;
alter table leads add column if not exists phone_other_secondary text;
alter table leads add column if not exists email_secondary_2 text;
"""

conn = psycopg.connect(os.environ["NEON_DSN"])
with conn:
    with conn.cursor() as cur:
        cur.execute(DDL)
print("Columns added/verified")
