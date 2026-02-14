#!/usr/bin/env node
/**
 * Credits manager for Explorium API keys stored in a Google Sheet.
 *
 * Data model (keys tab, default: Sheet1)
 * Required columns (header row):
 *   - Keys
 *   - Credits used/Month
 * Optional (created/maintained by script if present):
 *   - Credits Month (YYYY-MM)
 *   - Last Used (UTC ISO)
 *
 * Usage log tab (recommended): UsageLog
 * Header:
 *   timestamp_utc, month, api_key, action, credits_spent, credits_used_month, prospect_id, linkedin, correlation_id
 *
 * Commands:
 *   node credits_manager.mjs pick
 *   node credits_manager.mjs spend --api-key <key> --credits 5 [--action contacts_information] [--prospect-id ...] [--linkedin ...] [--correlation-id ...]
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';

function die(msg) {
  console.error(msg);
  process.exit(1);
}

function readConfig() {
  // workspace secrets file: ../../../secrets/explorium_credits_sheet.json
  try {
    const p = new URL('../../../secrets/explorium_credits_sheet.json', import.meta.url);
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    die('Missing secrets/explorium_credits_sheet.json with spreadsheetId');
  }
}

function gog(args) {
  const r = spawnSync('gog', args, { encoding: 'utf8' });
  if (r.error) throw new Error(`Failed to run gog: ${r.error.message}`);
  if (r.status !== 0) throw new Error(r.stderr || r.stdout || `gog failed (${r.status})`);
  return r.stdout;
}

function gogOrDie(args) {
  try {
    return gog(args);
  } catch (e) {
    die(e.message);
  }
}

function ymNow() {
  const d = new Date();
  return d.toISOString().slice(0, 7); // YYYY-MM in UTC
}

function utcNowIso() {
  return new Date().toISOString();
}

function parseSheetValues(jsonText) {
  const j = JSON.parse(jsonText);
  const values = j.values || [];
  return values;
}

function headerIndexMap(headerRow) {
  const m = new Map();
  headerRow.forEach((h, i) => m.set(String(h || '').trim(), i));
  return m;
}

function getAllKeys(cfg) {
  const range = `${cfg.keysTab}!A1:Z1000`;
  const out = gogOrDie(['sheets', 'get', cfg.spreadsheetId, range, '--json', '--no-input']);
  const values = parseSheetValues(out);
  if (!values.length) die('Keys sheet is empty');
  const header = values[0];
  const map = headerIndexMap(header);
  const idxKey = map.get('Keys');
  const idxCredits = map.get('Credits used/Month');
  const idxMonth = map.get('Credits Month (YYYY-MM)');
  const idxLast = map.get('Last Used (UTC ISO)');

  if (idxKey == null) die('Sheet1 header must include column: Keys');
  if (idxCredits == null) die('Sheet1 header must include column: Credits used/Month');

  const rows = [];
  for (let r = 1; r < values.length; r++) {
    const row = values[r];
    const apiKey = row[idxKey];
    if (!apiKey) continue;
    const creditsUsed = Number(row[idxCredits] || 0) || 0;
    const month = idxMonth != null ? (row[idxMonth] || '') : '';
    const lastUsed = idxLast != null ? (row[idxLast] || '') : '';
    rows.push({ rowNumber1: r + 1, apiKey: String(apiKey).trim(), creditsUsed, month: String(month).trim(), lastUsed: String(lastUsed).trim() });
  }

  return { header, map, rows };
}

function pickKey(cfg) {
  const { rows } = getAllKeys(cfg);
  const ym = ymNow();

  // Choose first key with credits < 100 for current month; if month column exists and differs, treat credits as 0.
  for (const r of rows) {
    const effectiveCredits = (r.month && r.month !== ym) ? 0 : r.creditsUsed;
    if (effectiveCredits < 100) {
      process.stdout.write(JSON.stringify({ api_key: r.apiKey, credits_used_month: effectiveCredits, month: ym }, null, 2));
      return;
    }
  }

  die('No available API key with credits < 100 for current month');
}

function findKeyRow(cfg, apiKey) {
  const { header, map, rows } = getAllKeys(cfg);
  const hit = rows.find(r => r.apiKey === apiKey);
  if (!hit) die('API key not found in sheet');
  return { header, map, hit };
}

function ensureExtraColumns(cfg, header, map) {
  // If month/last-used columns are missing, we do NOT auto-add (requires shifting columns).
  // We can still work with Credits used/Month only.
  return {
    idxCredits: map.get('Credits used/Month'),
    idxMonth: map.get('Credits Month (YYYY-MM)'),
    idxLast: map.get('Last Used (UTC ISO)')
  };
}

function colToA1(colIndex0) {
  let n = colIndex0 + 1;
  let s = '';
  while (n > 0) {
    const r = (n - 1) % 26;
    s = String.fromCharCode(65 + r) + s;
    n = Math.floor((n - 1) / 26);
  }
  return s;
}

function spend(cfg, apiKey, credits, meta) {
  const { header, map, hit } = findKeyRow(cfg, apiKey);
  const ym = ymNow();
  const cols = ensureExtraColumns(cfg, header, map);

  // Determine current credits used
  const currentCredits = (cols.idxMonth != null && hit.month && hit.month !== ym) ? 0 : hit.creditsUsed;
  const nextCredits = currentCredits + credits;

  // Update Credits used/Month cell
  const colCreditsA1 = colToA1(cols.idxCredits);
  const rangeCredits = `${cfg.keysTab}!${colCreditsA1}${hit.rowNumber1}`;
  gogOrDie(['sheets', 'update', cfg.spreadsheetId, rangeCredits, '--values-json', JSON.stringify([[String(nextCredits)]]), '--input', 'USER_ENTERED', '--json', '--no-input']);

  // If month column exists, keep it aligned
  if (cols.idxMonth != null) {
    const colMonthA1 = colToA1(cols.idxMonth);
    const rangeMonth = `${cfg.keysTab}!${colMonthA1}${hit.rowNumber1}`;
    gogOrDie(['sheets', 'update', cfg.spreadsheetId, rangeMonth, '--values-json', JSON.stringify([[ym]]), '--input', 'USER_ENTERED', '--json', '--no-input']);
  }

  // If last-used column exists, update it
  if (cols.idxLast != null) {
    const colLastA1 = colToA1(cols.idxLast);
    const rangeLast = `${cfg.keysTab}!${colLastA1}${hit.rowNumber1}`;
    gogOrDie(['sheets', 'update', cfg.spreadsheetId, rangeLast, '--values-json', JSON.stringify([[utcNowIso()]]), '--input', 'USER_ENTERED', '--json', '--no-input']);
  }

  // Append usage log if tab exists
  if (cfg.usageTab) {
    try {
      // Prefix month with apostrophe so Sheets keeps it as text (avoid date serial like 46054).
      const row = [
        utcNowIso(),
        `'${ym}`,
        apiKey,
        meta.action || 'spend',
        String(credits),
        String(nextCredits),
        meta.prospectId || '',
        meta.linkedin || '',
        meta.correlationId || ''
      ];
      gog(['sheets', 'append', cfg.spreadsheetId, `${cfg.usageTab}!A:I`, '--values-json', JSON.stringify([row]), '--insert', 'INSERT_ROWS', '--json', '--no-input']);
    } catch {
      // ignore
    }
  }

  process.stdout.write(JSON.stringify({ api_key: apiKey, month: ym, credits_used_month: nextCredits }, null, 2));
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) out._.push(a);
    else {
      const k = a.slice(2);
      const v = (i + 1 < argv.length && !argv[i + 1].startsWith('--')) ? argv[++i] : true;
      out[k] = v;
    }
  }
  return out;
}

const args = parseArgs(process.argv);
const cmd = args._[0];
const cfg = readConfig();

if (cmd === 'pick') {
  pickKey(cfg);
} else if (cmd === 'spend') {
  const apiKey = args['api-key'];
  const credits = Number(args['credits'] || 0);
  if (!apiKey) die('Missing --api-key');
  if (!credits) die('Missing/invalid --credits');
  spend(cfg, apiKey, credits, {
    action: args['action'],
    prospectId: args['prospect-id'],
    linkedin: args['linkedin'],
    correlationId: args['correlation-id']
  });
} else {
  die('Usage: node credits_manager.mjs pick | spend --api-key <key> --credits 5');
}
