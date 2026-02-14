---
name: explorium-prospects-match
description: Call Explorium AgentSource Prospects API to match prospect attributes (email, phone_number, linkedin, or full_name+company_name, optionally business_id) into Prospect IDs using POST https://api.explorium.ai/v1/prospects/match. Use when you need to dedupe/resolve lead identities to Explorium prospect_id or validate lead inputs against Explorium.
---

## What this skill does

Use Explorium’s **Match prospects** endpoint to turn a list of prospect “fetchers” (identifiers) into stable **prospect_id** values, preserving input order.

## Required inputs

- `api_key` (Explorium)
- `prospects_to_match` array (1–50 items)
- Optional: `tenant` header (if your Explorium account uses it)

## Request schema (per prospect item)

Each item can include any of:

- `email` (string)
- `phone_number` (string)
- `linkedin` (string URL)
- `full_name` + `company_name` (must be provided together)
- `business_id` (optional string; filter match to a specific company)

## Preferred workflow (scripted)

1) Prepare a JSON body like:

```json
{
  "prospects_to_match": [
    { "email": "[email protected]" },
    { "linkedin": "https://www.linkedin.com/in/someone" },
    { "full_name": "Richard Branson", "company_name": "Virgin" }
  ],
  "request_context": null
}
```

2) Run the bundled script (outputs the API JSON response).

You can provide the key in one of three ways:
- `--api-key "..."`
- environment variable `EXPLORIUM_API_KEY`
- workspace file `secrets/explorium.json` with `{ "api_key": "..." }`

```powershell
node scripts/match_prospects.mjs --in body.json
```

Optional tenant header:

```powershell
node scripts/match_prospects.mjs --tenant "YOUR_TENANT" --in body.json
```

## Notes / gotchas

- The API returns `matched_prospects` **in the same length and order** as your input list.
- `prospects_to_match` supports **1–50** elements.
- Handle partial matches: some items may be unmatched or returned as an error variant.

## Reference

If you need the exact endpoint/headers/response fields, read:
- `references/match_prospects_api.md`

## Credits-aware key rotation (Google Sheet)

You asked for this policy:
- Every API key has **100 credits/month**.
- `prospects/match` costs **0**.
- `prospects/contacts_information/enrich` costs **5**.
- Track usage in the Google Sheet column **Credits used/Month**.
- When a key hits **100**, use the **next** key in the sheet.
- Credits refresh monthly. (To avoid accidental extra charges, do **not** retry failed calls automatically.)

This skill includes scripts to:
- pick an API key from the sheet
- spend credits and log usage

Prereq (Sheet setup)
- SpreadsheetId is stored in `secrets/explorium_credits_sheet.json`.
- Keys live in tab `Sheet1` with headers:
  - `Keys`
  - `Credits used/Month`
- A usage-log tab will be created in the sheet (currently created as **Sheet2**). Header row:
  - `timestamp_utc | month | api_key | action | credits_spent | credits_used_month | prospect_id | linkedin | correlation_id`

### Sync credits from Explorium (real-time)

To overwrite the Sheet credit counters with the **real** usage from `GET /v1/credits` for every key:

```powershell
node scripts/sync_credits_from_explorium.mjs
```

### One-shot: LinkedIn → contact details (1 match + 1 enrich + update credits)

```powershell
node scripts/contact_details_from_linkedin.mjs --linkedin "http://www.linkedin.com/in/vincent-kong-aa174a8b"
```

## Direct contacts information enrichment

To fetch emails/phone for a resolved `prospect_id`:

```powershell
node scripts/enrich_contacts_information.mjs --prospect-id "<prospect_id>"
```

(Uses `API_KEY` header; key can come from `--api-key`, `EXPLORIUM_API_KEY`, or `secrets/explorium.json`.)
