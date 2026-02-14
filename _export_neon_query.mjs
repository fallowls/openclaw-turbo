import { Client } from 'pg';
import fs from 'node:fs';

function csvEscape(v) {
  if (v === null || v === undefined) return '';
  let s = String(v);
  // Arrays/objects
  if (typeof v === 'object') {
    try { s = JSON.stringify(v); } catch { s = String(v); }
  }
  if (s.includes('"') || s.includes(',') || s.includes('\n') || s.includes('\r')) {
    s = '"' + s.replaceAll('"', '""') + '"';
  }
  return s;
}

const outPath = process.argv[2];
if (!outPath) {
  console.error('Usage: node _export_neon_query.mjs <out_csv_path>');
  process.exit(1);
}

const sql = process.env.EXPORT_SQL;
if (!sql) {
  console.error('Missing env EXPORT_SQL');
  process.exit(1);
}

const dsn = process.env.NEON_DSN;
if (!dsn) {
  console.error('Missing env NEON_DSN');
  process.exit(1);
}

const client = new Client({ connectionString: dsn, ssl: { rejectUnauthorized: false } });
await client.connect();

try {
  const res = await client.query(sql);
  const cols = res.fields.map(f => f.name);
  const lines = [];
  lines.push(cols.map(csvEscape).join(','));
  for (const row of res.rows) {
    lines.push(cols.map(c => csvEscape(row[c])).join(','));
  }
  fs.writeFileSync(outPath, lines.join('\n'), 'utf8');
  console.log(JSON.stringify({ exported: res.rowCount, outPath }, null, 2));
} finally {
  await client.end();
}
