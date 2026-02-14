import os, psycopg
sql = """
create extension if not exists pgcrypto;
create table if not exists leads (
    lead_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name TEXT,
    last_name TEXT,
    title TEXT,
    seniority TEXT,
    departments TEXT[],
    linkedin_person_url TEXT,
    email_primary TEXT,
    email_secondary TEXT,
    email_confidence INTEGER,
    email_verified BOOLEAN,
    phone_mobile TEXT,
    phone_work TEXT,
    phone_other TEXT,
    person_city TEXT,
    person_state TEXT,
    person_country TEXT,
    company_name TEXT,
    company_name_for_emails TEXT,
    company_domain TEXT,
    company_website TEXT,
    company_linkedin_url TEXT,
    industry TEXT,
    company_description TEXT,
    keywords TEXT[],
    technologies TEXT[],
    employee_count INTEGER,
    revenue BIGINT,
    year_founded INTEGER,
    company_phone TEXT,
    company_address TEXT,
    company_city TEXT,
    company_state TEXT,
    company_country TEXT,
    total_funding BIGINT,
    latest_funding BIGINT,
    last_raised_at DATE,
    ipo_status BOOLEAN,
    ipo_date DATE,
    source TEXT CHECK (source IN ('LTI', 'Lusha', 'Apollo')),
    source_person_id TEXT,
    source_company_id TEXT,
    stage TEXT,
    last_contacted DATE,
    email_sent BOOLEAN,
    email_open BOOLEAN,
    email_bounced BOOLEAN,
    replied BOOLEAN,
    demoed BOOLEAN,
    lists TEXT[],
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
"""
conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute(sql)
print('leads table created')
