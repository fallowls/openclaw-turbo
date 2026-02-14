"""Create tables in Neon Postgres.
Requires: pip install psycopg[binary]
Uses NEON_DSN env var.
"""
import os
import psycopg

DDL = """
create table if not exists companies (
  company_id bigserial primary key,
  name text,
  website text,
  linkedin_url text,
  country text,
  state text,
  revenue text,
  source text,
  created_at timestamptz default now()
);

create table if not exists prospects (
  prospect_id bigserial primary key,
  first_name text,
  last_name text,
  title text,
  email text,
  mobile_phone text,
  other_phone text,
  corporate_phone text,
  person_linkedin_url text,
  company_linkedin_url text,
  website text,
  state text,
  country text,
  time_zone text,
  company_id bigint references companies(company_id),
  source text,
  created_at timestamptz default now()
);
create index if not exists idx_prospects_email on prospects (lower(email));
create index if not exists idx_prospects_linkedin on prospects (person_linkedin_url);

create table if not exists contact_activity (
  activity_id bigserial primary key,
  prospect_id bigint references prospects(prospect_id),
  activity_type text,
  activity_value text,
  activity_ts timestamptz default now()
);
"""

conn = psycopg.connect(os.environ["NEON_DSN"])
with conn:
    with conn.cursor() as cur:
        cur.execute(DDL)
print("Tables created/verified")
