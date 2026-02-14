import fs from 'node:fs';
import path from 'node:path';

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

function getArg(name, def = null) {
  const i = process.argv.indexOf(name);
  if (i === -1) return def;
  return process.argv[i + 1] ?? def;
}

const outPath = getArg('--out', path.resolve('34b04286_neon_lookup_found_merged.csv'));
const partsArg = getArg('--parts');
const parts = partsArg
  ? partsArg.split(',').map(s => s.trim()).filter(Boolean)
  : Array.from({ length: 8 }, (_, i) => path.resolve(`34b04286_neon_lookup_part${i + 1}.csv`));

let header = null;
let idx = null;
const keepRows = [];

for (const p of parts) {
  if (!fs.existsSync(p)) throw new Error(`Missing file: ${p}`);
  const rows = parseCsv(fs.readFileSync(p, 'utf8'));
  if (rows.length === 0) continue;
  if (!header) {
    header = rows[0];
    idx = Object.fromEntries(header.map((h, i) => [h, i]));
    if (!('found' in idx) || !('input_email' in idx)) throw new Error('Unexpected header (need found,input_email)');
  }
  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    if (!row || row.length === 0) continue;
    const found = (row[idx.found] ?? '').toString().trim().toLowerCase();
    if (found === 'true') keepRows.push(row);
  }
}

// Deduplicate: prefer by lead_id if present, else by input_email
const leadIdIdx = idx.lead_id;
const emailIdx = idx.input_email;
const seenLead = new Set();
const seenEmail = new Set();
const dedup = [];

for (const row of keepRows) {
  const leadId = (row[leadIdIdx] ?? '').toString().trim();
  const email = (row[emailIdx] ?? '').toString().trim().toLowerCase();

  if (leadId) {
    if (seenLead.has(leadId)) continue;
    seenLead.add(leadId);
    dedup.push(row);
    continue;
  }

  if (email) {
    if (seenEmail.has(email)) continue;
    seenEmail.add(email);
    dedup.push(row);
  }
}

const outRows = [header, ...dedup];
fs.writeFileSync(outPath, toCsv(outRows), 'utf8');

console.log(JSON.stringify({
  parts: parts.length,
  total_rows_in_parts_found_only: keepRows.length,
  dedup_rows: dedup.length,
  out: outPath
}, null, 2));
