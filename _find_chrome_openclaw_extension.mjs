import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const localAppData = process.env.LOCALAPPDATA;
if (!localAppData) {
  console.error('LOCALAPPDATA not set');
  process.exit(1);
}
const base = path.join(localAppData, 'Google', 'Chrome', 'User Data', 'Default', 'Extensions');
console.log('BASE', base);

function* walk(dir) {
  let ents;
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of ents) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.isFile() && e.name === 'manifest.json') yield p;
  }
}

const hits = [];
for (const manifestPath of walk(base)) {
  try {
    const j = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    const name = String(j.name || '');
    const desc = String(j.description || '');
    const blob = (name + ' ' + desc).toLowerCase();
    if (blob.includes('openclaw') || blob.includes('claw') || blob.includes('relay')) {
      hits.push({ name, desc, manifestPath });
    }
  } catch {}
}

hits.sort((a,b) => a.name.localeCompare(b.name));
for (const h of hits) {
  console.log(h.name);
  console.log('  desc:', h.desc);
  console.log('  manifest:', h.manifestPath);
}

if (!hits.length) {
  console.log('No obvious OpenClaw/relay extensions found by name/description.');
  console.log('If you can share the Chrome extension ID, I can locate it directly.');
}
