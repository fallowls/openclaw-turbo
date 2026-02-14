#!/usr/bin/env node
/**
 * Explorium: POST /v1/prospects/contacts_information/enrich
 *
 * Usage:
 *   node enrich_contacts_information.mjs --prospect-id <id> [--api-key <key>] [--tenant <tenant>]
 *
 * API key resolution (same as match script):
 *   1) --api-key
 *   2) EXPLORIUM_API_KEY env var
 *   3) workspace secrets/explorium.json {"api_key":"..."}
 */

import fs from 'node:fs';

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

function usageAndExit(msg) {
  if (msg) console.error(msg);
  console.error('Usage: node enrich_contacts_information.mjs --prospect-id <id> [--api-key <key>] [--tenant <tenant>]');
  process.exit(2);
}

const args = parseArgs(process.argv);
const prospectId = args['prospect-id'];
let apiKey = args['api-key'] || process.env.EXPLORIUM_API_KEY;
const tenant = args['tenant'];

if (!prospectId) usageAndExit('Missing --prospect-id');

if (!apiKey) {
  try {
    const p = new URL('../../../secrets/explorium.json', import.meta.url);
    const raw = fs.readFileSync(p, 'utf8');
    const j = JSON.parse(raw);
    if (j && typeof j.api_key === 'string') apiKey = j.api_key;
  } catch {}
}

if (!apiKey) usageAndExit('Missing api key (use --api-key, EXPLORIUM_API_KEY, or secrets/explorium.json)');

const url = 'https://api.explorium.ai/v1/prospects/contacts_information/enrich';

// Docs for this endpoint expect header `API_KEY` (case-sensitive in practice).
const headers = {
  'Content-Type': 'application/json',
  'API_KEY': apiKey,
};
if (tenant) headers['tenant'] = tenant;

const res = await fetch(url, {
  method: 'POST',
  headers,
  body: JSON.stringify({ prospect_id: prospectId }),
});

const text = await res.text();
let json;
try { json = JSON.parse(text); } catch {
  console.error(text);
  process.exit(res.ok ? 0 : 1);
}

if (!res.ok) {
  console.error(JSON.stringify({ http_status: res.status, error: json }, null, 2));
  process.exit(1);
}

process.stdout.write(JSON.stringify(json, null, 2));
