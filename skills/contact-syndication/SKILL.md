---
name: contact-syndication
description: Syndicate contacts/leads from the Neon Postgres lead database to external destinations (CSV exports, Google Drive/Sheets, email delivery, Bunny Storage, messaging). Use when pushing curated lead lists to channels, keeping downstream lists in sync, scheduling exports, or producing repeatable audience segments from the leads table.
---

# Contact Syndication

Use this skill to **publish** and **sync** lead lists out of the database.

## Core idea
- Treat Neon `leads` as the source of truth.
- For each audience/segment, generate a deterministic export.
- Deliver to one or more destinations.
- Track each run with `batch_id` and (optional) `syndication_runs` log.

## Workflow

1) **Pick a segment**
- Example: Finance Director + US + has email + any phone
- Example: IT Manager + Mexico + revenue >= 50M

2) **Export from Neon**
- Prefer SQL that is reproducible and includes ordering.
- Save as CSV with stable headers.

3) **Deliver**
- WhatsApp file (small exports)
- Google Drive upload/share (large exports)
- Google Sheets (append or overwrite tab)
- Bunny Storage upload (archive or downstream pipeline)
- Email attachment / link (optional)

4) **Log** (recommended)
- Write a record of: segment_name, sql_hash, row_count, output_path, destination(s), ts.

## References
- `references/segments.md` (standard segment recipes)
- `references/destinations.md` (delivery rules + size limits)
- `references/logging.md` (recommended syndication_runs table)
- `references/enterprise-plan.md` (enterprise research + acquisition + enrichment plan)

## Scripts
- `scripts/export_segment.py` (SQL → CSV)
- `scripts/deliver_drive.py` (upload + share)
- `scripts/deliver_bunny.py` (upload to Bunny Storage; requires creds)
- `scripts/log_run.py` (optional logging)

Notes:
- Do not automate actions that violate provider ToS (e.g., bulk scraping gated sites).
- Prefer Drive for files >25MB.
