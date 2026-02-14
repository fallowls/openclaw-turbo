import fs from 'node:fs';
import path from 'node:path';
import { Client } from 'pg';

function parseCsv(text) {
  // RFC4180-ish parser (handles quotes + commas + CRLF)
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const c = text[i];

    if (inQuotes) {
      if (c === '"') {
        const next = text[i + 1];
        if (next === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
      continue;
    }

    if (c === '"') {
      inQuotes = true;
      continue;
    }

    if (c === ',') {
      row.push(field);
      field = '';
      continue;
    }

    if (c === '\n') {
      // finish field (strip trailing \r)
      if (field.endsWith('\r')) field = field.slice(0, -1);
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
      continue;
    }

    field += c;
  }

  // last field
  if (field.length || row.length) {
    if (field.endsWith('\r')) field = field.slice(0, -1);
    row.push(field);
    rows.push(row);
  }

  return rows;
}

function toCsv(rows) {
  const esc = (v) => {
    if (v == null) return '';
    const s = String(v);
    if (/[\",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
    return s;
  };
  return rows.map((r) => r.map(esc).join(',')).join('\n') + '\n';
}

function getArg(name) {
  const i = process.argv.indexOf(name);
  if (i === -1) return null;
  return process.argv[i + 1] ?? null;
}

function getNeonDsn() {
  if (process.env.NEON_DSN) return process.env.NEON_DSN;
  const mdPath = path.resolve('skills/lead-gen-db/references/neon-db.md');
  const md = fs.readFileSync(mdPath, 'utf8');
  const m = md.match(/postgresql:\/\/[^\s"']+/);
  if (!m) throw new Error(`Could not find DSN in ${mdPath}`);
  return m[0];
}

function pickFirstNonEmpty(...vals) {
  for (const v of vals) {
    if (v != null && String(v).trim() !== '') return String(v);
  }
  return '';
}

async function main() {
  const inPath = getArg('--in') || getArg('-i');
  const outPath = getArg('--out') || getArg('-o');
  if (!inPath || !outPath) {
    console.error('Usage: node _neon_enrich_apollo_csv.mjs --in <input.csv> --out <output.csv>');
    process.exit(2);
  }

  const raw = fs.readFileSync(inPath, 'utf8');
  const rows = parseCsv(raw);
  if (rows.length < 2) throw new Error('CSV has no data rows');

  const header = rows[0];
  const idx = Object.fromEntries(header.map((h, i) => [h, i]));

  const colEmail = 'Email';
  const colLinkedIn = 'Person Linkedin Url';

  const colWork = 'Work Direct Phone';
  const colMobile = 'Mobile Phone';
  const colOther = 'Other Phone';
  const colCorp = 'Corporate Phone';
  const colCompanyPhone = 'Company Phone';

  for (const c of [colEmail, colLinkedIn, colWork, colMobile, colOther, colCorp, colCompanyPhone]) {
    if (!(c in idx)) throw new Error(`Missing expected column: ${c}`);
  }

  const dsn = getNeonDsn();
  const client = new Client({ connectionString: dsn });
  await client.connect();

  let filledWork = 0;
  let filledMobile = 0;
  let filledOther = 0;
  let filledCorp = 0;
  let filledCompanyPhone = 0;
  let matched = 0;

  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    // normalize row length
    while (row.length < header.length) row.push('');

    const email = (row[idx[colEmail]] || '').trim().toLowerCase();
    const linkedin = (row[idx[colLinkedIn]] || '').trim();

    const needsAny = [colWork, colMobile, colOther, colCorp, colCompanyPhone].some((c) => (row[idx[c]] || '').trim() === '');
    if (!needsAny) continue;

    if (!email && !linkedin) continue;

    const res = await client.query(
      `select phone_mobile, phone_work, phone_other, company_phone
       from leads
       where ($1 <> '' and lower(email_primary) = $1)
          or ($2 <> '' and linkedin_person_url = $2)
       order by updated_at desc nulls last
       limit 1`,
      [email || '', linkedin || '']
    );

    if (res.rows.length === 0) continue;
    matched++;
    const lead = res.rows[0];

    if ((row[idx[colWork]] || '').trim() === '' && lead.phone_work) {
      row[idx[colWork]] = lead.phone_work;
      filledWork++;
    }
    if ((row[idx[colMobile]] || '').trim() === '' && lead.phone_mobile) {
      row[idx[colMobile]] = lead.phone_mobile;
      filledMobile++;
    }
    if ((row[idx[colOther]] || '').trim() === '' && lead.phone_other) {
      row[idx[colOther]] = lead.phone_other;
      filledOther++;
    }

    const companyPhone = pickFirstNonEmpty(lead.company_phone);
    if ((row[idx[colCompanyPhone]] || '').trim() === '' && companyPhone) {
      row[idx[colCompanyPhone]] = companyPhone;
      filledCompanyPhone++;
    }
    if ((row[idx[colCorp]] || '').trim() === '' && companyPhone) {
      row[idx[colCorp]] = companyPhone;
      filledCorp++;
    }
  }

  await client.end();

  fs.writeFileSync(outPath, toCsv(rows), 'utf8');

  const summary = {
    rows: rows.length - 1,
    matched,
    filled_work: filledWork,
    filled_mobile: filledMobile,
    filled_other: filledOther,
    filled_corporate: filledCorp,
    filled_company_phone: filledCompanyPhone,
    out: outPath
  };
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
