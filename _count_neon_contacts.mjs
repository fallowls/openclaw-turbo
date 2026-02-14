import { Client } from 'pg';

const dsn = process.env.NEON_DSN;
if (!dsn) {
  console.error('Missing env NEON_DSN');
  process.exit(1);
}

const sql = `
with base as (
  select *
  from leads
  where (
          revenue >= 50000000
       or (revenue is null and employee_count > 100)
        )
    and (
         lower(title) like '%it manager%'
      or lower(title) like '%it operations manager%'
      or lower(title) like '%it service manager%'
      or lower(title) like '%it services manager%'
      or lower(title) like '%it project manager%'
      or lower(title) like '%it delivery manager%'
      or lower(title) like '%information technology manager%'
      or lower(title) like '%infrastructure manager%'
      or lower(title) like '%systems manager%'
      or lower(title) like '%network manager%'
      or lower(title) like '%service desk manager%'
      or lower(title) like '%helpdesk manager%'
      or lower(title) like '%application manager%'
      or lower(title) like '%it support manager%'
    )
    and (
      industry ilike '%information technology%'
      or industry ilike '%it & services%'
      or industry ilike '%software%'
      or industry ilike '%computer%'
      or industry ilike '%internet%'
      or industry ilike '%telecommunications%'
    )
    and (
      lower(coalesce(person_country,'')) in (
        'united kingdom','uk','great britain','england','scotland','wales','northern ireland'
      )
      or lower(coalesce(person_country,'')) like '%united kingdom%'
    )
)
select
  count(*)::int as contacts_total,
  count(*) filter (where email_primary is not null and email_primary <> '')::int as with_email,
  count(*) filter (where linkedin_person_url is not null and linkedin_person_url <> '')::int as with_linkedin,
  count(*) filter (where (phone_mobile is not null and phone_mobile <> '') or (phone_work is not null and phone_work <> '') or (phone_other is not null and phone_other <> ''))::int as with_any_phone,
  count(*) filter (where phone_mobile is not null and phone_mobile <> '')::int as with_mobile
from base;
`;

const client = new Client({ connectionString: dsn, ssl: { rejectUnauthorized: false } });
await client.connect();
try {
  const res = await client.query(sql);
  console.log(JSON.stringify(res.rows[0], null, 2));
} finally {
  await client.end();
}
