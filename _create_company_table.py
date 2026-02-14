import os, psycopg

DDL = r"""
create extension if not exists pgcrypto;

create table if not exists company (
  company_id uuid primary key default gen_random_uuid(),

  company_domain text unique,
  company_name text,
  company_website text,
  company_linkedin_url text,

  industry text,
  sub_industry text,
  technologies text[],
  specialties text,

  employee_count int,
  revenue bigint,
  year_founded int,

  company_city text,
  company_state text,
  company_country text,

  total_funding bigint,
  latest_funding bigint,
  last_raised_at date,
  ipo_status boolean,
  ipo_date date,

  source text,
  batch_id text,
  created_at timestamp default now(),
  updated_at timestamp default now()
);

create index if not exists idx_company_name on company (company_name);
create index if not exists idx_company_country on company (company_country);
"""

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute(DDL)
print('company table ensured')
