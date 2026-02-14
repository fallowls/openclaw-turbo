"""Log a syndication run (optional).

Requires: pip install psycopg[binary]
Env: NEON_DSN

Usage:
  python log_run.py <segment_name> <row_count> <output_path> <destinations_csv> [batch_id]

Example:
  python log_run.py finance_directors 782 C:\\out.csv drive,whatsapp BATCH_20260210
"""

import os
import sys
import psycopg

if len(sys.argv) < 5:
    print('Usage: python log_run.py <segment_name> <row_count> <output_path> <destinations_csv> [batch_id]')
    raise SystemExit(1)

segment = sys.argv[1]
row_count = int(sys.argv[2])
out_path = sys.argv[3]
dests = [d.strip() for d in sys.argv[4].split(',') if d.strip()]
batch_id = sys.argv[5] if len(sys.argv) > 5 else None

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            create table if not exists syndication_runs (
              run_id bigserial primary key,
              segment_name text not null,
              sql_text text not null default '',
              sql_hash text,
              row_count int,
              output_path text,
              destinations text[],
              batch_id text,
              created_at timestamptz default now()
            );
            """
        )
        cur.execute(
            """
            insert into syndication_runs(segment_name,row_count,output_path,destinations,batch_id)
            values (%s,%s,%s,%s,%s)
            """,
            (segment, row_count, out_path, dests, batch_id)
        )

print('Logged run')
