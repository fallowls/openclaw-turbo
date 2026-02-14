# Logging

Optional table to track syndication runs.

```sql
create table if not exists syndication_runs (
  run_id bigserial primary key,
  segment_name text not null,
  sql_text text not null,
  sql_hash text,
  row_count int,
  output_path text,
  destinations text[],
  batch_id text,
  created_at timestamptz default now()
);
```
