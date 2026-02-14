import fs from 'node:fs';
const p = process.argv[2];
if (!p) { console.error('usage: node _clean_nan_csv.mjs <path>'); process.exit(1); }
let s = fs.readFileSync(p,'utf8');
// Replace ,NaN, or ,NaN\n (case-insensitive)
s = s.replace(/,NaN(?=,|\r?\n)/gi, ',');
fs.writeFileSync(p, s, 'utf8');
console.log('CLEANED', p);
