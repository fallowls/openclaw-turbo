---
name: lead-gen-db
description: Lead generation data processing and database management for Apollo/Lusha/Bunny CSVs. Use when cleaning, normalizing, filtering, deduplicating, merging lead data, or loading/querying the Neon Postgres lead database. Includes standard schemas, dedupe rules, and CSV import/export workflows.
---

# Lead Gen DB Skill

Follow this workflow to process lead data and maintain the Neon database.

## Workflow

1) **Choose input sources**
- Apollo CSV exports
- Lusha CSV exports
- Bunny Storage CSV batches

2) **Normalize + clean**
- Standardize headers to the canonical schema
- Normalize domains and LinkedIn URLs
- Map phone fields to Mobile/Other/Corporate
- Remove obvious junk (e.g., empty names + no contact info)
- Normalize NaN/NA/blank → NULL

3) **Filter** (optional)
- Titles, geo, revenue, domains

4) **Deduplicate / Update**
- Match order: email → LinkedIn URL → name + company
- **Update existing rows with new details** without overwriting populated fields
- If new data exists for a filled field, store in **secondary_* columns** (do not delete old data)
- Track **field_sources** + **last_updated_source** + **batch_id**

5) **Load or export**
- Load into Neon (leads table)
- Export filtered CSV or query results

6) **Search & Retrieval (Phase 3)**
- Use prebuilt queries (titles, geo, revenue, missing fields)
- Export to CSV for delivery

7) **Automation (Phase 4)**
- Schedule imports from Bunny Storage / Apollo / Lusha
- Auto-normalize + dedupe + upsert
- Export summaries after each run

8) **Intelligence Layer (Phase 5)**
- Tag companies by expansion signals
- Score leads by intent
- Track new India‑office signals

## References
- **Schema + DDL**: `references/schema.md`
- **Dedupe rules**: `references/dedupe-rules.md`
- **Update policy**: `references/update-policy.md`
- **Phone/header mapping**: `references/phone-mapping.md`
- **Queries (Phase 3)**: `references/queries.md`
- **Automation (Phase 4)**: `references/automation.md`
- **Intelligence (Phase 5)**: `references/intelligence.md`
- **Neon connection + usage**: `references/neon-db.md`

## Scripts
- `scripts/create_tables.py` (create schema)
- `scripts/add_leads_columns.py` (add advanced columns)
- `scripts/import_csv.py` (load CSV to Neon)
- `scripts/export_query.py` (export query results)
- `scripts/export_prebuilt.py` (Phase 3 exports)
- `scripts/normalize_nan.sql` (clean NaN/NA values)

Use the scripts when deterministic behavior is required. If Python deps are missing, install with pip as noted in the script headers.

## Automation entrypoint
- `scripts/run_pipeline.py` runs: add columns → stage load (COPY) → set-based upsert (no overwrite).
