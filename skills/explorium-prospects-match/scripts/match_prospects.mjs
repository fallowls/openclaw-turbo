#!/usr/bin/env node
/**
 * Explorium: POST /v1/prospects/match
 *
 * Usage:
 *   node match_prospects.mjs --api-key "..." --in body.json [--tenant "..."]
 *   type body.json | node match_prospects.mjs --api-key "..." --stdin
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

async function readStdin() {
  return await new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => (data += chunk));
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

function usageAndExit(msg) {
  if (msg) console.error(msg);
  console.error('Usage: node match_prospects.mjs --api-key <key> (--in <file.json> | --stdin) [--tenant <tenant>]');
  process.exit(2);
}

const args = parseArgs(process.argv);
let apiKey = args['api-key'] || process.env.EXPLORIUM_API_KEY;
const inPath = args['in'];
const useStdin = !!args['stdin'];
const tenant = args['tenant'];

// Fallback: workspace secrets file (optional)
if (!apiKey) {
  try {
    const p = new URL('../../../secrets/explorium.json', import.meta.url);
    const raw = fs.readFileSync(p, 'utf8');
    const j = JSON.parse(raw);
    if (j && typeof j.api_key === 'string') apiKey = j.api_key;
  } catch {}
}

if (!apiKey) usageAndExit('Missing --api-key (or set EXPLORIUM_API_KEY, or create secrets/explorium.json)');
if ((!inPath && !useStdin) || (inPath && useStdin)) usageAndExit('Provide exactly one of --in or --stdin');

let bodyText;
if (useStdin) bodyText = await readStdin();
else bodyText = fs.readFileSync(inPath, 'utf8');

let body;
try {
  body = JSON.parse(bodyText);
} catch (e) {
  usageAndExit('Invalid JSON body');
}

const url = 'https://api.explorium.ai/v1/prospects/match';

const headers = {
  'Content-Type': 'application/json',
  'api_key': apiKey,
};
if (tenant) headers['tenant'] = tenant;

const res = await fetch(url, {
  method: 'POST',
  headers,
  body: JSON.stringify(body),
});

const text = await res.text();
let json;
try {
  json = JSON.parse(text);
} catch {
  // Non-JSON error
  console.error(text);
  process.exit(res.ok ? 0 : 1);
}

if (!res.ok) {
  console.error(JSON.stringify({ http_status: res.status, error: json }, null, 2));
  process.exit(1);
}

process.stdout.write(JSON.stringify(json, null, 2));
