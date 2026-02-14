import fs from 'node:fs';
import path from 'node:path';

const base = path.join(process.env.LOCALAPPDATA || '', 'Google','Chrome','User Data');
const profiles = ['Default','Profile 1','Profile 2','Profile 3'];

function readJson(p){
  try { return JSON.parse(fs.readFileSync(p,'utf8')); } catch { return null; }
}

for (const prof of profiles) {
  const pref = path.join(base, prof, 'Preferences');
  const spref = path.join(base, prof, 'Secure Preferences');
  const prefs = readJson(pref) || {};
  const sprefs = readJson(spref) || {};
  const settings = sprefs?.extensions?.settings || prefs?.extensions?.settings || {};
  const ids = Object.keys(settings);
  console.log('\n===', prof, 'extensions:', ids.length, '===');
  let shown=0;
  for (const id of ids) {
    const s = settings[id];
    const m = s?.manifest || {};
    const name = s?.webstore_name || m?.name || '';
    const desc = m?.description || '';
    const upd = s?.update_url || '';
    const fromWebStore = typeof upd === 'string' && upd.includes('clients2.google.com/service/update2/crx');
    const blob = (String(name)+' '+String(desc)+' '+id).toLowerCase();
    const likely = ['openclaw','claw','relay','browser relay'].some(k=>blob.includes(k));
    if (likely || shown < 25) {
      console.log('---');
      console.log('name:', name);
      console.log('id:', id);
      console.log('fromWebStore:', fromWebStore);
      if (s?.path) console.log('path:', s.path);
      shown++;
    }
  }
}
