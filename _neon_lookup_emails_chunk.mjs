import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
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

function escCsv(v) {
  if (v == null) return '';
  const s = String(v);
  if (/[\",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
  return s;
}

function toIso(v) {
  if (!v) return '';
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? '' : d.toISOString();
}

function normEmail(s) {
  return (s ?? '').toString().trim().toLowerCase().replace(/^mailto:/, '').replace(/^<|>$/g, '');
}

function getArg(name, def = null) {
  const i = process.argv.indexOf(name);
  if (i === -1) return def;
  return process.argv[i + 1] ?? def;
}

const inPath = getArg('--in');
const outPath = getArg('--out');
const startLine = Number.parseInt(getArg('--start-line', '1'), 10); // 1-indexed
const maxLines = Number.parseInt(getArg('--max-lines', '50000'), 10);
const batchSize = Number.parseInt(getArg('--batch-size', '500'), 10);

if (!inPath || !outPath) {
  console.error('Usage: node _neon_lookup_emails_chunk.mjs --in <emails.csv> --out <out.csv> [--start-line 1] [--max-lines 50000] [--batch-size 500]');
  process.exit(2);
}

const dsn = getNeonDsn();
const client = new Client({ connectionString: dsn });
await client.connect();

const out = fs.createWriteStream(outPath, { encoding: 'utf8' });
out.write([
  'input_email','found','lead_id','first_name','last_name','title','company_name',
  'email_primary','email_secondary','email_secondary_2',
  'phone_mobile','phone_work','phone_other','phone_mobile_secondary','phone_work_secondary','phone_other_secondary',
  'company_phone','linkedin_person_url','updated_at'
].join(',') + '\n');

let currentLine = 0;
let processed = 0;
let uniqInChunk = 0;
let foundCount = 0;

async function flushBatch(emails) {
  if (emails.length === 0) return;

  // Query any of the email columns.
  const res = await client.query(
    `select lead_id, first_name, last_name, title, company_name,
            email_primary, email_secondary, email_secondary_2,
            phone_mobile, phone_work, phone_other,
            phone_mobile_secondary, phone_work_secondary, phone_other_secondary,
            company_phone, linkedin_person_url, updated_at
       from leads
      where lower(email_primary) = any($1)
         or lower(email_secondary) = any($1)
         or lower(email_secondary_2) = any($1)
      order by updated_at desc nulls last`,
    [emails]
  );

  // Build map from each email to best matching row (first seen in ordered result set)
  const map = new Map();
  for (const row of res.rows) {
    const candidates = [row.email_primary, row.email_secondary, row.email_secondary_2]
      .filter(Boolean)
      .map((e) => e.toLowerCase());
    for (const e of candidates) {
      if (emailsSet.has(e) && !map.has(e)) map.set(e, row);
    }
  }

  for (const e of emails) {
    const row = map.get(e);
    if (!row) {
      out.write([escCsv(e),'false',...Array(17).fill('')].join(',') + '\n');
      continue;
    }
    foundCount++;
    out.write([
      escCsv(e),
      'true',
      escCsv(row.lead_id),
      escCsv(row.first_name),
      escCsv(row.last_name),
      escCsv(row.title),
      escCsv(row.company_name),
      escCsv(row.email_primary),
      escCsv(row.email_secondary),
      escCsv(row.email_secondary_2),
      escCsv(row.phone_mobile),
      escCsv(row.phone_work),
      escCsv(row.phone_other),
      escCsv(row.phone_mobile_secondary),
      escCsv(row.phone_work_secondary),
      escCsv(row.phone_other_secondary),
      escCsv(row.company_phone),
      escCsv(row.linkedin_person_url),
      escCsv(toIso(row.updated_at)),
    ].join(',') + '\n');
  }
}

const rl = readline.createInterface({
  input: fs.createReadStream(inPath, { encoding: 'utf8' }),
  crlfDelay: Infinity,
});

let batch = [];
let emailsSet = new Set();

for await (const line of rl) {
  currentLine++;
  if (currentLine < startLine) continue;
  if (processed >= maxLines) break;

  const email = normEmail(line);
  processed++;
  if (!email) continue;
  if (emailsSet.has(email)) continue;

  emailsSet.add(email);
  batch.push(email);

  if (batch.length >= batchSize) {
    uniqInChunk += batch.length;
    await flushBatch(batch);
    batch = [];
    emailsSet = new Set();
  }
}

if (batch.length) {
  uniqInChunk += batch.length;
  await flushBatch(batch);
}

out.end();
await client.end();

console.log(JSON.stringify({
  input: inPath,
  out: outPath,
  start_line: startLine,
  max_lines: maxLines,
  processed_lines: processed,
  unique_emails_written: uniqInChunk,
  found_rows: foundCount
}, null, 2));
