#!/usr/bin/env node
/**
 * One-shot workflow (1 match + 1 enrichment) using a rotating API key from the credits sheet.
 *
 * Usage:
 *   node contact_details_from_linkedin.mjs --linkedin <url>
 */

import { spawnSync } from 'node:child_process';

function die(msg) {
  console.error(msg);
  process.exit(1);
}

function runNode(script, args, input) {
  const r = spawnSync('node', [script, ...args], { encoding: 'utf8', input });
  if (r.error) die(r.error.message);
  if (r.status !== 0) die(r.stderr || r.stdout || `Failed (${r.status})`);
  return r.stdout;
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
const linkedin = args.linkedin;
if (!linkedin) die('Missing --linkedin');

// 1) Pick key (no spend)
const pick = JSON.parse(runNode('scripts/credits_manager.mjs', ['pick']));
const apiKey = pick.api_key;

// 2) Match (cost 0)
const matchBody = JSON.stringify({ prospects_to_match: [{ linkedin }], request_context: null });
const matchJson = JSON.parse(runNode('scripts/match_prospects.mjs', ['--api-key', apiKey, '--stdin'], matchBody));

const prospectId = matchJson?.matched_prospects?.[0]?.prospect_id;
if (!prospectId) die('No prospect_id returned from match');

// 3) Enrich contact details (cost 5)
const enrichJson = JSON.parse(runNode('scripts/enrich_contacts_information.mjs', ['--api-key', apiKey, '--prospect-id', prospectId]));

// 4) Spend credits (5)
const correlationId = enrichJson?.response_context?.correlation_id || '';
runNode('scripts/credits_manager.mjs', ['spend', '--api-key', apiKey, '--credits', '5', '--action', 'contacts_information', '--prospect-id', prospectId, '--linkedin', linkedin, '--correlation-id', correlationId]);

process.stdout.write(JSON.stringify({ api_key: apiKey, prospect_id: prospectId, contacts_information: enrichJson.data || enrichJson }, null, 2));
