import fs from 'node:fs';
import path from 'node:path';
import { Client } from 'pg';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else field += c;
      continue;
    }
    if (c === '"') { inQuotes = true; continue; }
    if (c === ',') { row.push(field); field = ''; continue; }
    if (c === '\n') {
      if (field.endsWith('\r')) field = field.slice(0, -1);
      row.push(field);
      rows.push(row);
      row = []; field = '';
      continue;
    }
    field += c;
  }
  if (field.length || row.length) {
    if (field.endsWith('\r')) field = field.slice(0, -1);
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function idxMap(header) {
  return Object.fromEntries(header.map((h, i) => [h, i]));
}

function cell(row, idx, col) {
  const i = idx[col];
  if (i == null) return '';
  return (row[i] ?? '').toString().trim();
}

function nullIfBlank(v) {
  const s = (v ?? '').toString().trim();
  return s === '' ? null : s;
}

function boolOrNull(v) {
  const s = (v ?? '').toString().trim().toLowerCase();
  if (!s) return null;
  if (['true','t','1','yes','y'].includes(s)) return true;
  if (['false','f','0','no','n'].includes(s)) return false;
  return null;
}

function intOrNull(v) {
  const s = (v ?? '').toString().replace(/[,$]/g, '').trim();
  if (!s) return null;
  const n = Number.parseInt(s, 10);
  return Number.isFinite(n) ? n : null;
}

function bigIntOrNull(v) {
  const s = (v ?? '').toString().replace(/[,$]/g, '').trim();
  if (!s) return null;
  const n = Number.parseFloat(s);
  if (!Number.isFinite(n)) return null;
  return BigInt(Math.trunc(n));
}

function dateOrNull(v) {
  const s = (v ?? '').toString().trim();
  if (!s) return null;
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) return null;
  return d.toISOString().slice(0, 10);
}

function splitList(v) {
  const s = (v ?? '').toString().trim();
  if (!s) return null;
  const parts = s.split(',').map(x => x.trim()).filter(Boolean);
  return parts.length ? parts : null;
}

function normalizeLinkedin(url) {
  const s = (url ?? '').toString().trim();
  if (!s) return null;
  return s.replace(/\/+$/, '');
}

function getNeonDsn() {
  if (process.env.NEON_DSN) return process.env.NEON_DSN;
  const mdPath = path.resolve('skills/lead-gen-db/references/neon-db.md');
  const md = fs.readFileSync(mdPath, 'utf8');
  const m = md.match(/postgresql:\/\/[^\s"']+/);
  if (!m) throw new Error(`Could not find DSN in ${mdPath}`);
  return m[0];
}

async function main() {
  const inPath = process.argv[2];
  if (!inPath) {
    console.error('Usage: node _import_5986_to_neon.mjs <input.csv>');
    process.exit(2);
  }

  const raw = fs.readFileSync(inPath, 'utf8');
  const rows = parseCsv(raw);
  if (rows.length < 2) throw new Error('CSV has no data rows');

  const header = rows[0];
  const idx = idxMap(header);

  const dsn = getNeonDsn();
  const client = new Client({ connectionString: dsn });
  await client.connect();

  let inserted = 0;
  let updated = 0;
  let skipped = 0;

  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    while (row.length < header.length) row.push('');

    const first_name = nullIfBlank(cell(row, idx, 'First Name'));
    const last_name = nullIfBlank(cell(row, idx, 'Last Name'));
    const title = nullIfBlank(cell(row, idx, 'Title'));
    const company_name = nullIfBlank(cell(row, idx, 'Company Name'));
    const company_name_for_emails = nullIfBlank(cell(row, idx, 'Company Name for Emails'));

    const email_primary = nullIfBlank(cell(row, idx, 'Email'))?.toLowerCase() ?? null;

    const linkedin_person_url = normalizeLinkedin(cell(row, idx, 'Person Linkedin Url'));

    const phone_mobile = nullIfBlank(cell(row, idx, 'Mobile Phone'));
    const phone_other = nullIfBlank(cell(row, idx, 'Other Phone'));
    const corporate_phone = nullIfBlank(cell(row, idx, 'Corporate Phone'));

    const employee_count = intOrNull(cell(row, idx, '# Employees'));
    const industry = nullIfBlank(cell(row, idx, 'Industry'));

    const keywords = splitList(cell(row, idx, 'Keywords'));
    const technologies = splitList(cell(row, idx, 'Technologies'));

    const person_city = nullIfBlank(cell(row, idx, 'City'));
    const person_state = nullIfBlank(cell(row, idx, 'State'));
    const person_country = nullIfBlank(cell(row, idx, 'Country'));

    const company_address = nullIfBlank(cell(row, idx, 'Company Address'));
    const company_city = nullIfBlank(cell(row, idx, 'Company City'));
    const company_state = nullIfBlank(cell(row, idx, 'Company State'));
    const company_country = nullIfBlank(cell(row, idx, 'Company Country'));
    const company_phone = nullIfBlank(cell(row, idx, 'Company Phone')) || corporate_phone;

    const revenue = bigIntOrNull(cell(row, idx, 'Annual Revenue'));
    const total_funding = bigIntOrNull(cell(row, idx, 'Total Funding'));
    const latest_funding = bigIntOrNull(cell(row, idx, 'Latest Funding Amount'));
    const last_raised_at = dateOrNull(cell(row, idx, 'Last Raised At'));

    const stage = nullIfBlank(cell(row, idx, 'Stage'));
    const lists = splitList(cell(row, idx, 'Lists'));
    const last_contacted = dateOrNull(cell(row, idx, 'Last Contacted'));

    const email_sent = boolOrNull(cell(row, idx, 'Email Sent'));
    const email_open = boolOrNull(cell(row, idx, 'Email Open'));
    const email_bounced = boolOrNull(cell(row, idx, 'Email Bounced'));
    const replied = boolOrNull(cell(row, idx, 'Replied'));
    const demoed = boolOrNull(cell(row, idx, 'Demoed'));

    const source_person_id = nullIfBlank(cell(row, idx, 'Apollo Contact Id'));
    const source_company_id = nullIfBlank(cell(row, idx, 'Apollo Account Id'));

    const hasKey = !!email_primary || !!linkedin_person_url || (!!first_name && !!last_name && !!company_name);
    if (!hasKey) {
      skipped++;
      continue;
    }

    // find existing lead (email → linkedin → name+company)
    const find = await client.query(
      `select lead_id from leads
       where ($1::text is not null and lower(email_primary) = lower($1))
          or ($2::text is not null and replace(linkedin_person_url,'/','') = replace($2,'/',''))
          or ($3::text is not null and $4::text is not null and $5::text is not null and lower(first_name)=lower($3) and lower(last_name)=lower($4) and lower(company_name)=lower($5))
       order by updated_at desc nulls last
       limit 1`,
      [email_primary, linkedin_person_url, first_name, last_name, company_name]
    );

    if (find.rows.length === 0) {
      await client.query(
        `insert into leads (
          first_name, last_name, title, seniority, departments, linkedin_person_url,
          email_primary, email_secondary,
          phone_mobile, phone_work, phone_other,
          person_city, person_state, person_country,
          company_name, company_name_for_emails, company_website, company_linkedin_url,
          industry, employee_count, keywords, technologies,
          company_phone, company_address, company_city, company_state, company_country,
          revenue, total_funding, latest_funding, last_raised_at,
          stage, last_contacted, email_sent, email_open, email_bounced, replied, demoed, lists,
          source, source_person_id, source_company_id,
          last_updated_source, updated_at
        ) values (
          $1,$2,$3,null,null,$4,
          $5,null,
          $6,null,$7,
          $8,$9,$10,
          $11,$12,$13,$14,
          $15,$16,$17,$18,
          $19,$20,$21,$22,$23,
          $24,$25,$26,$27,
          $28,$29,$30,$31,$32,$33,$34,$35,
          'Apollo',$36,$37,
          'Apollo', now()
        )`,
        [
          first_name, last_name, title, linkedin_person_url,
          email_primary,
          phone_mobile, phone_other,
          person_city, person_state, person_country,
          company_name, company_name_for_emails, nullIfBlank(cell(row, idx, 'Website')), nullIfBlank(cell(row, idx, 'Company Linkedin Url')),
          industry, employee_count, keywords, technologies,
          company_phone, company_address, company_city, company_state, company_country,
          revenue, total_funding, latest_funding, last_raised_at,
          stage, last_contacted, email_sent, email_open, email_bounced, replied, demoed, lists,
          source_person_id, source_company_id,
        ]
      );
      inserted++;
      continue;
    }

    const leadId = find.rows[0].lead_id;

    // Update with: fill blanks; if different store in secondary columns (only if secondary empty)
    await client.query(
      `update leads set
        first_name = coalesce(nullif(first_name,''), $2),
        last_name = coalesce(nullif(last_name,''), $3),

        title = case when nullif(title,'') is null then $4 else title end,
        title_secondary = case
          when $4 is null then title_secondary
          when nullif(title,'') is not null and title <> $4 and nullif(title_secondary,'') is null then $4
          else title_secondary
        end,

        linkedin_person_url = coalesce(nullif(linkedin_person_url,''), $5),

        email_primary = case when nullif(email_primary,'') is null then $6 else email_primary end,
        email_secondary = case
          when $6 is null then email_secondary
          when nullif(email_primary,'') is not null and lower(email_primary) <> lower($6) and nullif(email_secondary,'') is null then $6
          else email_secondary
        end,
        email_secondary_2 = case
          when $6 is null then email_secondary_2
          when nullif(email_primary,'') is not null and lower(email_primary) <> lower($6)
               and nullif(email_secondary,'') is not null and lower(email_secondary) <> lower($6)
               and nullif(email_secondary_2,'') is null
            then $6
          else email_secondary_2
        end,

        phone_mobile = case when nullif(phone_mobile,'') is null then $7 else phone_mobile end,
        phone_mobile_secondary = case
          when $7 is null then phone_mobile_secondary
          when nullif(phone_mobile,'') is not null and phone_mobile <> $7 and nullif(phone_mobile_secondary,'') is null then $7
          else phone_mobile_secondary
        end,

        phone_other = case when nullif(phone_other,'') is null then $8 else phone_other end,
        phone_other_secondary = case
          when $8 is null then phone_other_secondary
          when nullif(phone_other,'') is not null and phone_other <> $8 and nullif(phone_other_secondary,'') is null then $8
          else phone_other_secondary
        end,

        company_name = coalesce(nullif(company_name,''), $9),
        company_name_for_emails = coalesce(nullif(company_name_for_emails,''), $10),
        company_website = coalesce(nullif(company_website,''), $11),
        company_linkedin_url = coalesce(nullif(company_linkedin_url,''), $12),
        industry = coalesce(nullif(industry,''), $13),
        employee_count = coalesce(employee_count, $14),
        keywords = coalesce(keywords, $15),
        technologies = coalesce(technologies, $16),

        person_city = coalesce(nullif(person_city,''), $17),
        person_state = coalesce(nullif(person_state,''), $18),
        person_country = coalesce(nullif(person_country,''), $19),

        company_address = coalesce(nullif(company_address,''), $20),
        company_city = coalesce(nullif(company_city,''), $21),
        company_state = coalesce(nullif(company_state,''), $22),
        company_country = coalesce(nullif(company_country,''), $23),

        company_phone = coalesce(nullif(company_phone,''), $24),

        revenue = coalesce(revenue, $25),
        total_funding = coalesce(total_funding, $26),
        latest_funding = coalesce(latest_funding, $27),
        last_raised_at = coalesce(last_raised_at, $28),

        stage = coalesce(nullif(stage,''), $29),
        last_contacted = coalesce(last_contacted, $30),
        email_sent = coalesce(email_sent, $31),
        email_open = coalesce(email_open, $32),
        email_bounced = coalesce(email_bounced, $33),
        replied = coalesce(replied, $34),
        demoed = coalesce(demoed, $35),
        lists = coalesce(lists, $36),

        source_person_id = coalesce(nullif(source_person_id,''), $37),
        source_company_id = coalesce(nullif(source_company_id,''), $38),
        last_updated_source = 'Apollo',
        updated_at = now()
      where lead_id = $1`,
      [
        leadId,
        first_name, last_name, title, linkedin_person_url,
        email_primary,
        phone_mobile, phone_other,
        company_name, company_name_for_emails, nullIfBlank(cell(row, idx, 'Website')), nullIfBlank(cell(row, idx, 'Company Linkedin Url')),
        industry, employee_count, keywords, technologies,
        person_city, person_state, person_country,
        company_address, company_city, company_state, company_country,
        company_phone,
        revenue, total_funding, latest_funding, last_raised_at,
        stage, last_contacted, email_sent, email_open, email_bounced, replied, demoed, lists,
        source_person_id, source_company_id,
      ]
    );

    updated++;
  }

  await client.end();
  console.log(JSON.stringify({ input: inPath, rows: rows.length - 1, inserted, updated, skipped }, null, 2));
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
