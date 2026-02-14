"""Run an end-to-end import pipeline for a single CSV.

This is the automation entrypoint.

Requires: pip install psycopg[binary]
Env: NEON_DSN

Usage:
  python run_pipeline.py apollo <csv_path> <batch_id>
  python run_pipeline.py lusha  <csv_path> <batch_id>

Expectations:
- csv_path should be a *normalized staging CSV* with headers matching stage_load.py columns.
  (We will add normalizers per source later; for now this automates the DB part.)

Steps:
1) stage_load.py
2) add_leads_columns.py (safe idempotent)
3) upsert_from_stage.sql template applied per source
"""

import os
import sys
import subprocess
from pathlib import Path
import psycopg

HERE = Path(__file__).resolve().parent

if len(sys.argv) < 4:
    print('Usage: python run_pipeline.py apollo|lusha <csv_path> <batch_id>')
    raise SystemExit(1)

source = sys.argv[1].lower()
csv_path = sys.argv[2]
batch_id = sys.argv[3]

py = sys.executable

subprocess.check_call([py, str(HERE / 'add_leads_columns.py')])
subprocess.check_call([py, str(HERE / 'stage_load.py'), source, csv_path, batch_id])

staging = 'staging_apollo' if source == 'apollo' else 'staging_lusha'
source_name = 'Apollo' if source == 'apollo' else 'Lusha'

sql_template = (HERE / 'upsert_from_stage.sql').read_text(encoding='utf-8')
sql_text = sql_template.replace('<STAGING_TABLE>', staging).replace('<SOURCE_NAME>', source_name)

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute(sql_text)

print('Pipeline complete:', source, batch_id)
