import fs from 'node:fs';
import path from 'node:path';
import xlsx from 'xlsx';
import pgPkg from 'pg';
const { Client } = pgPkg;

function getNeonDsn() {
  if (process.env.NEON_DSN) return process.env.NEON_DSN;
  const mdPath = path.resolve('skills/lead-gen-db/references/neon-db.md');
  const md = fs.readFileSync(mdPath, 'utf8');
  const m = md.match(/postgresql:\/\/[^\s"']+/);
  if (!m) throw new Error(`Could not find DSN in ${mdPath}`);
  return m[0];
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

function normEmail(v) {
  const s = (v ?? '').toString().trim().toLowerCase();
  if (!s) return '';
  // remove surrounding <> and mailto:
  return s.replace(/^<|>$/g, '').replace(/^mailto:/, '');
}

const inPath = process.argv[2];
const outPath = process.argv[3] || path.resolve(process.cwd(), 'neon_lookup_results.csv');
const sheetNameArg = process.argv.find(a => a.startsWith('--sheet='))?.split('=')[1];
const emailColArg = process.argv.find(a => a.startsWith('--email-col='))?.split('=')[1];

if (!inPath) {
  console.error('Usage: node _lookup_neon_by_email_from_xlsx.mjs <input.xlsx> [output.csv] [--sheet=Sheet1] [--email-col=Email]');
  process.exit(2);
}

const wb = xlsx.readFile(inPath, { cellDates: true });
const sheetName = sheetNameArg || wb.SheetNames[0];
const ws = wb.Sheets[sheetName];
if (!ws) throw new Error(`Sheet not found: ${sheetName}`);

const json = xlsx.utils.sheet_to_json(ws, { defval: '' });
if (json.length === 0) throw new Error('Sheet has no rows');

// pick email column
const headers = Object.keys(json[0]);
const emailCol = emailColArg || (headers.find(h => h.toLowerCase().includes('email')) ?? headers[0]);

const emails = json
  .map(r => normEmail(r[emailCol]))
  .filter(Boolean);

const uniq = Array.from(new Set(emails));

const dsn = getNeonDsn();
const client = new Client({ connectionString: dsn });
await client.connect();

const outRows = [[
  'input_email',
  'found',
  'lead_id',
  'first_name',
  'last_name',
  'title',
  'company_name',
  'email_primary',
  'email_secondary',
  'email_secondary_2',
  'phone_mobile',
  'phone_work',
  'phone_other',
  'phone_mobile_secondary',
  'phone_work_secondary',
  'phone_other_secondary',
  'company_phone',
  'linkedin_person_url',
  'updated_at'
]];

let found = 0;

for (const email of uniq) {
  const res = await client.query(
    `select lead_id, first_name, last_name, title, company_name,
            email_primary, email_secondary, email_secondary_2,
            phone_mobile, phone_work, phone_other,
            phone_mobile_secondary, phone_work_secondary, phone_other_secondary,
            company_phone, linkedin_person_url, updated_at
       from leads
      where lower(email_primary) = $1
         or lower(email_secondary) = $1
         or lower(email_secondary_2) = $1
      order by updated_at desc nulls last
      limit 1`,
    [email]
  );

  if (res.rows.length === 0) {
    outRows.push([email, 'false', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']);
    continue;
  }

  found++;
  const r = res.rows[0];
  outRows.push([
    email,
    'true',
    r.lead_id ?? '',
    r.first_name ?? '',
    r.last_name ?? '',
    r.title ?? '',
    r.company_name ?? '',
    r.email_primary ?? '',
    r.email_secondary ?? '',
    r.email_secondary_2 ?? '',
    r.phone_mobile ?? '',
    r.phone_work ?? '',
    r.phone_other ?? '',
    r.phone_mobile_secondary ?? '',
    r.phone_work_secondary ?? '',
    r.phone_other_secondary ?? '',
    r.company_phone ?? '',
    r.linkedin_person_url ?? '',
    r.updated_at ? new Date(r.updated_at).toISOString() : ''
  ]);
}

await client.end();

fs.writeFileSync(outPath, toCsv(outRows), 'utf8');
console.log(JSON.stringify({ sheet: sheetName, email_col: emailCol, input_rows: json.length, unique_emails: uniq.length, found, out: outPath }, null, 2));
