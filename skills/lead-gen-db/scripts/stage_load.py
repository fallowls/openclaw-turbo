"""Load a source CSV into a staging table using COPY (fast).

Requires: pip install psycopg[binary]
Env: NEON_DSN

Usage:
  python stage_load.py <source> <csv_path> <batch_id>

Creates/uses tables:
- staging_apollo
- staging_lusha

Notes:
- Staging tables are wide text columns to avoid type issues.
- Upsert step is handled by upsert_from_stage.sql.
"""

import os
import sys
import psycopg

if len(sys.argv) < 4:
    print("Usage: python stage_load.py <source> <csv_path> <batch_id>")
    raise SystemExit(1)

source = sys.argv[1].lower()
csv_path = sys.argv[2]
batch_id = sys.argv[3]

if source not in ("apollo", "lusha"):
    raise SystemExit("source must be apollo|lusha")

# Minimal canonical staging columns (all text). Keep extra_json for future expansion.
DDL = {
    "apollo": """
      create table if not exists staging_apollo (
        batch_id text,
        first_name text,
        last_name text,
        title text,
        seniority text,
        departments text,
        linkedin_person_url text,
        email_primary text,
        email_secondary text,
        email_confidence text,
        email_verified text,
        phone_mobile text,
        phone_work text,
        phone_other text,
        person_city text,
        person_state text,
        person_country text,
        company_name text,
        company_name_for_emails text,
        company_website text,
        company_linkedin_url text,
        industry text,
        company_description text,
        keywords text,
        technologies text,
        employee_count text,
        revenue text,
        year_founded text,
        company_phone text,
        company_address text,
        company_city text,
        company_state text,
        company_country text,
        total_funding text,
        latest_funding text,
        last_raised_at text,
        source_person_id text,
        source_company_id text,
        stage text,
        last_contacted text,
        lists text,
        extra_json jsonb
      );
    """,
    "lusha": """
      create table if not exists staging_lusha (
        batch_id text,
        first_name text,
        last_name text,
        title text,
        seniority text,
        departments text,
        linkedin_person_url text,
        email_primary text,
        email_secondary text,
        email_confidence text,
        email_verified text,
        phone_mobile text,
        phone_work text,
        phone_other text,
        person_city text,
        person_state text,
        person_country text,
        company_name text,
        company_name_for_emails text,
        company_website text,
        company_linkedin_url text,
        industry text,
        company_description text,
        keywords text,
        technologies text,
        employee_count text,
        revenue text,
        year_founded text,
        company_phone text,
        company_address text,
        company_city text,
        company_state text,
        company_country text,
        total_funding text,
        latest_funding text,
        last_raised_at text,
        source_person_id text,
        source_company_id text,
        stage text,
        last_contacted text,
        lists text,
        extra_json jsonb
      );
    """,
}

table = "staging_apollo" if source == "apollo" else "staging_lusha"

conn = psycopg.connect(os.environ["NEON_DSN"])
with conn:
    with conn.cursor() as cur:
        cur.execute(DDL[source])
        # Clear batch for idempotency
        cur.execute(f"delete from {table} where batch_id = %s", (batch_id,))
        # Use server-side COPY; expect caller to provide already-normalized CSV with matching header names.
        copy_sql = f"copy {table} from stdin with (format csv, header true)"
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            with cur.copy(copy_sql) as cp:
                # stream file
                for line in f:
                    cp.write(line)

print(f"Loaded {source} staging for batch {batch_id}")
