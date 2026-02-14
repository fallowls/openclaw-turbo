# Automation (Phase 4)

## Suggested schedule
- Daily: import latest Apollo/Lusha exports
- Weekly: backfill missing fields from freshest dumps
- Monthly: full refresh, dedupe, and summary export

## Pipeline steps
1) Ingest new CSVs
2) Normalize + clean (NaN → NULL)
3) Upsert into leads table (no overwrite)
4) Update `batch_id` and `last_updated_source`
5) Export summary CSVs
