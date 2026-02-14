#!/usr/bin/env node
/**
 * Sync real Explorium credits (GET /v1/credits) into the Google Sheet.
 *
 * For each API key in the keys tab:
 * - call https://api.explorium.ai/v1/credits with header API_KEY
 * - compute used = allocated_credits - remaining_credits
 * - write used into column `Credits used/Month`
 *
 * Usage:
 *   node sync_credits_from_explorium.mjs
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';

function die(msg) {
  console.error(msg);
  process.exit(1);
}

function readConfig() {
  try {
    const p = new URL('../../../secrets/explorium_credits_sheet.json', import.meta.url);
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    die('Missing secrets/explorium_credits_sheet.json');
  }
}

function gogOrDie(args) {
  const r = spawnSync('gog', args, { encoding: 'utf8' });
  if (r.error) die(`Failed to run gog: ${r.error.message}`);
  if (r.status !== 0) die(r.stderr || r.stdout || `gog failed (${r.status})`);
  return r.stdout;
}

function parseSheetValues(jsonText) {
  const j = JSON.parse(jsonText);
  return j.values || [];
}

function headerIndexMap(headerRow) {
  const m = new Map();
  headerRow.forEach((h, i) => m.set(String(h || '').trim(), i));
  return m;
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

async function fetchCredits(apiKey) {
  const res = await fetch('https://api.explorium.ai/v1/credits', {
    headers: {
      'API_KEY': apiKey
    }
  });
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${JSON.stringify(json)}`);
  }
  const allocated = Number(json.allocated_credits ?? 0);
  const remaining = Number(json.remaining_credits ?? 0);
  return { allocated_credits: allocated, remaining_credits: remaining, used_credits: allocated - remaining, correlation_id: json?.response_context?.correlation_id };
}

const cfg = readConfig();
const range = `${cfg.keysTab}!A1:Z1000`;
const out = gogOrDie(['sheets', 'get', cfg.spreadsheetId, range, '--json', '--no-input']);
const values = parseSheetValues(out);
if (!values.length) die('Keys sheet is empty');

const header = values[0];
const map = headerIndexMap(header);
const idxKey = map.get('Keys');
const idxCredits = map.get('Credits used/Month');
if (idxKey == null) die('Missing header: Keys');
if (idxCredits == null) die('Missing header: Credits used/Month');

const colCreditsA1 = colToA1(idxCredits);

let ok = 0, fail = 0;
for (let r = 1; r < values.length; r++) {
  const row = values[r];
  const apiKey = row[idxKey];
  if (!apiKey) continue;

  const key = String(apiKey).trim();
  try {
    const c = await fetchCredits(key);
    const target = `${cfg.keysTab}!${colCreditsA1}${r + 1}`;
    // Use gog sheets update with inline values (pipe-separated cells). Single cell update.
    gogOrDie(['sheets', 'update', cfg.spreadsheetId, target, String(c.used_credits), '--input', 'USER_ENTERED', '--json', '--no-input']);
    ok++;
  } catch (e) {
    fail++;
    console.error(`Key row ${r + 1} failed: ${e.message}`);
  }
}

process.stdout.write(JSON.stringify({ synced: ok, failed: fail }, null, 2));
