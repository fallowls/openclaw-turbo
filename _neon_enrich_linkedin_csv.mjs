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
      if (field.endsWith('\r')) field = field.slice(0, -1);
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
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

async function main() {
  const inPath = getArg('--in') || getArg('-i');
  const outPath = getArg('--out') || getArg('-o');
  if (!inPath || !outPath) {
    console.error('Usage: node _neon_enrich_linkedin_csv.mjs --in <input.csv> --out <output.csv>');
    process.exit(2);
  }

  const raw = fs.readFileSync(inPath, 'utf8');
  const rows = parseCsv(raw);
  if (rows.length < 2) throw new Error('CSV has no data rows');

  const header = rows[0];
  const idx = Object.fromEntries(header.map((h, i) => [h, i]));

  const colLinkedIn = 'Person Linkedin Url';
  if (!(colLinkedIn in idx)) throw new Error(`Missing expected column: ${colLinkedIn}`);

  const colWork = 'Work Direct Phone';
  const colMobile = 'Mobile Phone';
  const colOther = 'Other Phone';
  const colCompanyPhone = 'Company Phone';

  for (const c of [colWork, colMobile, colOther]) {
    if (!(c in idx)) throw new Error(`Missing expected column: ${c}`);
  }

  const hasCompanyPhone = colCompanyPhone in idx;

  const dsn = getNeonDsn();
  const client = new Client({ connectionString: dsn });
  await client.connect();

  let matched = 0;
  let filledWork = 0;
  let filledMobile = 0;
  let filledOther = 0;
  let filledCompanyPhone = 0;

  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    while (row.length < header.length) row.push('');

    const linkedin = (row[idx[colLinkedIn]] || '').trim();
    if (!linkedin) continue;

    const needsAny = [colWork, colMobile, colOther].some((c) => (row[idx[c]] || '').trim() === '');
    const needsCompany = hasCompanyPhone && (row[idx[colCompanyPhone]] || '').trim() === '';
    if (!needsAny && !needsCompany) continue;

    const variants = new Set();
    const li = linkedin;
    variants.add(li);
    variants.add(li.replace(/\/+$/,'') );
    variants.add(li.replace(/^https:\/\//,'http://'));
    variants.add(li.replace(/^http:\/\//,'https://'));
    variants.add(li.replace(/^https:\/\//,'http://').replace(/\/+$/,'') );
    variants.add(li.replace(/^http:\/\//,'https://').replace(/\/+$/,'') );

    const res = await client.query(
      `select phone_mobile, phone_work, phone_other, company_phone
       from leads
       where linkedin_person_url = any($1)
       order by updated_at desc nulls last
       limit 1`,
      [Array.from(variants)]
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

    if (needsCompany && lead.company_phone) {
      row[idx[colCompanyPhone]] = lead.company_phone;
      filledCompanyPhone++;
    }
  }

  await client.end();

  fs.writeFileSync(outPath, toCsv(rows), 'utf8');

  console.log(JSON.stringify({
    rows: rows.length - 1,
    matched,
    filled_work: filledWork,
    filled_mobile: filledMobile,
    filled_other: filledOther,
    filled_company_phone: filledCompanyPhone,
    out: outPath
  }, null, 2));
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
