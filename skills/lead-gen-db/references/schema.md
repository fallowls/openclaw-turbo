# Lead Gen DB Schema (Neon Postgres)

## leads (primary)
```sql
create extension if not exists pgcrypto;
create table if not exists leads (
  lead_id UUID primary key default gen_random_uuid(),

  -- person
  first_name text,
  last_name text,
  title text,
  seniority text,
  departments text[],
  linkedin_person_url text,
  email_primary text,
  email_secondary text,
  email_confidence int,
  email_verified boolean,
  phone_mobile text,
  phone_work text,
  phone_other text,
  person_city text,
  person_state text,
  person_country text,

  -- company
  company_name text,
  company_name_for_emails text,
  company_domain text,
  company_website text,
  company_linkedin_url text,
  industry text,
  company_description text,
  keywords text[],
  technologies text[],
  employee_count int,
  revenue bigint,
  year_founded int,
  company_phone text,
  company_address text,
  company_city text,
  company_state text,
  company_country text,

  -- funding
  total_funding bigint,
  latest_funding bigint,
  last_raised_at date,
  ipo_status boolean,
  ipo_date date,

  -- source/meta
  source text check (source in ('LTI','Lusha','Apollo')),
  source_person_id text,
  source_company_id text,
  last_updated_source text,
  batch_id text,
  field_sources jsonb,

  -- outreach
  stage text,
  last_contacted date,
  email_sent boolean,
  email_open boolean,
  email_bounced boolean,
  replied boolean,
  demoed boolean,
  lists text[],

  -- system
  created_at timestamp default now(),
  updated_at timestamp default now()
);
```

## Optional: add secondary fields (store extra details without overwriting)
```sql
alter table leads add column if not exists title_secondary text;
alter table leads add column if not exists phone_mobile_secondary text;
alter table leads add column if not exists phone_work_secondary text;
alter table leads add column if not exists phone_other_secondary text;
alter table leads add column if not exists email_secondary_2 text;
```
