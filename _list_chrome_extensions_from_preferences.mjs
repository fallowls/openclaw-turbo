import fs from 'node:fs';
import path from 'node:path';

const localAppData = process.env.LOCALAPPDATA;
const prefPath = path.join(localAppData, 'Google', 'Chrome', 'User Data', 'Default', 'Preferences');
console.log('PREFERENCES', prefPath);

const raw = fs.readFileSync(prefPath, 'utf8');
const prefs = JSON.parse(raw);

const settings = prefs?.extensions?.settings || {};
const keys = Object.keys(settings);
console.log('EXTENSIONS FOUND', keys.length);

function getName(id, s) {
  const m = s?.manifest || {};
  const n = m?.name;
  const webstoreName = s?.webstore_name;
  return webstoreName || n || '';
}

const rows = [];
for (const id of keys) {
  const s = settings[id];
  const name = getName(id, s);
  const updateUrl = s?.update_url || '';
  const fromWebStore = typeof updateUrl === 'string' && updateUrl.includes('clients2.google.com/service/update2/crx');
  const pathHint = s?.path || ''; // present for unpacked
  const enabled = s?.state === 1;
  rows.push({ id, name, enabled, fromWebStore, pathHint, updateUrl });
}

// Print likely matches first
const needles = ['openclaw','claw','relay','browser relay'];
function score(r) {
  const blob = (r.name + ' ' + r.id).toLowerCase();
  let sc = 0;
  for (const n of needles) if (blob.includes(n)) sc += 10;
  if (r.pathHint) sc += 3;
  if (!r.fromWebStore) sc += 1;
  return -sc;
}
rows.sort((a,b)=>score(a)-score(b) || a.name.localeCompare(b.name));

let shown = 0;
for (const r of rows) {
  const blob = (r.name || '').toLowerCase();
  const likely = needles.some(n=>blob.includes(n));
  if (likely || shown < 40) {
    console.log('---');
    console.log('name:', r.name);
    console.log('id:', r.id);
    console.log('enabled:', r.enabled);
    console.log('fromWebStore:', r.fromWebStore);
    if (r.pathHint) console.log('pathHint:', r.pathHint);
    if (r.updateUrl) console.log('updateUrl:', r.updateUrl);
    shown++;
  }
}

console.log('\nTip: If you want only one extension, send me the id from chrome://extensions and I can map it to the on-disk folder immediately.');
