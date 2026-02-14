import fs from 'node:fs';
import { Client } from 'pg';

const md = fs.readFileSync('skills/lead-gen-db/references/neon-db.md','utf8');
const m = md.match(/postgresql:\/\/[^\s"']+/);
if (!m) throw new Error('DSN not found');
const dsn = process.env.NEON_DSN || m[0];

const client = new Client({ connectionString: dsn });
await client.connect();
const r = await client.query("select column_name from information_schema.columns where table_name='leads' order by ordinal_position");
const cols = r.rows.map(x => x.column_name);
const want = cols.filter(n => n.includes('secondary') || n.startsWith('title_') || n.startsWith('phone_') && n.includes('secondary'));
console.log(JSON.stringify({ count: cols.length, secondary_like: want }, null, 2));
await client.end();
