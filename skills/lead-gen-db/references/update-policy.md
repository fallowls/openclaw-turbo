# Update Policy

- **Never delete** existing leads during enrichment.
- **Update only missing fields** (NULL/empty).
- If new data arrives for a filled field, store it in the **secondary_* columns**.
- Track provenance in `field_sources` (jsonb) and `last_updated_source`.
- Tag imports with a `batch_id` for audit.
