import fs from 'node:fs';

const inPath = process.argv[2];
const outPath = process.argv[3];
if (!inPath || !outPath) {
  console.error('Usage: node _patch_two_explorium_results.mjs <in.csv> <out.csv>');
  process.exit(2);
}

const fixes = new Map([
  ['http://www.linkedin.com/in/robbie-bressler-cpa-ca-11327641', { mobile: '+14162073307' }],
  ['http://www.linkedin.com/in/mehmetshah', { mobile: '+16473857698', other: '+15123279200' }],
]);

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

function toCsv(rows) {
  const esc = (v) => {
    if (v == null) return '';
    const s = String(v);
    if (/[\",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
    return s;
  };
  return rows.map(r => r.map(esc).join(',')).join('\n') + '\n';
}

const raw = fs.readFileSync(inPath, 'utf8');
const rows = parseCsv(raw);
const header = rows[0];
const idx = Object.fromEntries(header.map((h, i) => [h, i]));

for (const col of ['Person Linkedin Url','Mobile Phone','Other Phone']) {
  if (!(col in idx)) throw new Error('Missing column: ' + col);
}

let patched = 0;
for (let r = 1; r < rows.length; r++) {
  const row = rows[r];
  while (row.length < header.length) row.push('');
  const li = (row[idx['Person Linkedin Url']] || '').trim();
  const fix = fixes.get(li);
  if (!fix) continue;

  if (!row[idx['Mobile Phone']].trim() && fix.mobile) row[idx['Mobile Phone']] = fix.mobile;
  if (!row[idx['Other Phone']].trim() && fix.other) row[idx['Other Phone']] = fix.other;
  patched++;
}

fs.writeFileSync(outPath, toCsv(rows), 'utf8');
console.log(JSON.stringify({ patched, out: outPath }, null, 2));
