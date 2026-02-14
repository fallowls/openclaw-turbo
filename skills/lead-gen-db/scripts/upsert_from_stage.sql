-- Upsert from staging into leads (no overwrite).
-- Assumes leads table exists.
-- Strategy:
-- 1) Normalize NaN/NA/blank to NULL in staging via NULLIF.
-- 2) Match existing lead by email_primary OR linkedin_person_url.
-- 3) Insert net-new.
-- 4) Update only missing fields; store new values into secondary_* when primary already set.

-- NOTE: This is a template; run it per-source by replacing <STAGING_TABLE> and <SOURCE_NAME>.

-- Helper: treat blank/'nan'/'na' as NULL
-- We apply per column inline using nullif / lower.

-- Insert net-new
insert into leads (
  first_name,last_name,title,seniority,departments,linkedin_person_url,
  email_primary,email_secondary,email_confidence,email_verified,
  phone_mobile,phone_work,phone_other,
  person_city,person_state,person_country,
  company_name,company_name_for_emails,company_domain,company_website,company_linkedin_url,
  industry,company_description,keywords,technologies,employee_count,revenue,year_founded,
  company_phone,company_address,company_city,company_state,company_country,
  total_funding,latest_funding,last_raised_at,
  source,source_person_id,source_company_id,
  last_updated_source,batch_id,field_sources,
  stage,last_contacted,lists,created_at,updated_at
)
select
  nullif(first_name,'') , nullif(last_name,'') , nullif(title,'') , nullif(seniority,''),
  case when departments is null or departments='' then null else regexp_split_to_array(departments, '[;,]') end,
  nullif(linkedin_person_url,''),
  nullif(email_primary,''), nullif(email_secondary,''),
  nullif(regexp_replace(coalesce(email_confidence,''), '[^0-9]', '', 'g'),'')::int,
  case when lower(email_verified) in ('true','yes','1') then true when lower(email_verified) in ('false','no','0') then false else null end,
  nullif(phone_mobile,''), nullif(phone_work,''), nullif(phone_other,''),
  nullif(person_city,''), nullif(person_state,''), nullif(person_country,''),
  nullif(company_name,''), nullif(company_name_for_emails,''),
  nullif(regexp_replace(lower(company_website), '^https?://', ''),''),
  nullif(company_website,''), nullif(company_linkedin_url,''),
  nullif(industry,''), nullif(company_description,''),
  case when keywords is null or keywords='' then null else regexp_split_to_array(keywords, '[;,]') end,
  case when technologies is null or technologies='' then null else regexp_split_to_array(technologies, '[;,]') end,
  nullif(replace((regexp_match(coalesce(employee_count,''), '(\\d[\\d,]*)'))[1], ',', ''),'')::int,
  nullif(regexp_replace(coalesce(revenue,''), '[^0-9]', '', 'g'),'')::bigint,
  nullif(regexp_replace(coalesce(year_founded,''), '[^0-9]', '', 'g'),'')::int,
  nullif(company_phone,''), nullif(company_address,''), nullif(company_city,''), nullif(company_state,''), nullif(company_country,''),
  nullif(regexp_replace(coalesce(total_funding,''), '[^0-9]', '', 'g'),'')::bigint,
  nullif(regexp_replace(coalesce(latest_funding,''), '[^0-9]', '', 'g'),'')::bigint,
  nullif(last_raised_at,'')::date,
  '<SOURCE_NAME>'::text,
  nullif(source_person_id,''), nullif(source_company_id,''),
  '<SOURCE_NAME>'::text, batch_id,
  jsonb_build_object('<SOURCE_NAME>', true),
  nullif(stage,''), nullif(last_contacted,'')::date,
  case when lists is null or lists='' then null else regexp_split_to_array(lists, '[;,]') end,
  now(), now()
from <STAGING_TABLE> s
where s.batch_id is not null
  and not exists (
    select 1 from leads l
    where (l.email_primary is not null and s.email_primary is not null and lower(l.email_primary)=lower(s.email_primary))
       or (l.linkedin_person_url is not null and s.linkedin_person_url is not null and l.linkedin_person_url=s.linkedin_person_url)
  );

-- Update existing (fill NULL only, store alternates)
update leads l
set
  title = coalesce(l.title, nullif(s.title,'')),
  title_secondary = case when l.title is not null and nullif(s.title,'') is not null and l.title <> nullif(s.title,'') then coalesce(l.title_secondary, nullif(s.title,'')) else l.title_secondary end,

  phone_mobile = coalesce(l.phone_mobile, nullif(s.phone_mobile,'')),
  phone_mobile_secondary = case when l.phone_mobile is not null and nullif(s.phone_mobile,'') is not null and l.phone_mobile <> nullif(s.phone_mobile,'') then coalesce(l.phone_mobile_secondary, nullif(s.phone_mobile,'')) else l.phone_mobile_secondary end,

  phone_work = coalesce(l.phone_work, nullif(s.phone_work,'')),
  phone_work_secondary = case when l.phone_work is not null and nullif(s.phone_work,'') is not null and l.phone_work <> nullif(s.phone_work,'') then coalesce(l.phone_work_secondary, nullif(s.phone_work,'')) else l.phone_work_secondary end,

  phone_other = coalesce(l.phone_other, nullif(s.phone_other,'')),
  phone_other_secondary = case when l.phone_other is not null and nullif(s.phone_other,'') is not null and l.phone_other <> nullif(s.phone_other,'') then coalesce(l.phone_other_secondary, nullif(s.phone_other,'')) else l.phone_other_secondary end,

  email_secondary = coalesce(l.email_secondary, nullif(s.email_secondary,'')),
  email_secondary_2 = case when l.email_secondary is not null and nullif(s.email_secondary,'') is not null and l.email_secondary <> nullif(s.email_secondary,'') then coalesce(l.email_secondary_2, nullif(s.email_secondary,'')) else l.email_secondary_2 end,

  company_name = coalesce(l.company_name, nullif(s.company_name,'')),
  company_website = coalesce(l.company_website, nullif(s.company_website,'')),
  company_linkedin_url = coalesce(l.company_linkedin_url, nullif(s.company_linkedin_url,'')),

  last_updated_source = '<SOURCE_NAME>'::text,
  batch_id = coalesce(l.batch_id, s.batch_id),
  field_sources = coalesce(l.field_sources, '{}'::jsonb) || jsonb_build_object('<SOURCE_NAME>', true),
  updated_at = now()
from <STAGING_TABLE> s
where s.batch_id is not null
  and (
    (l.email_primary is not null and s.email_primary is not null and lower(l.email_primary)=lower(s.email_primary))
     or (l.linkedin_person_url is not null and s.linkedin_person_url is not null and l.linkedin_person_url=s.linkedin_person_url)
  );
