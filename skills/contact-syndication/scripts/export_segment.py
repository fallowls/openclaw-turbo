"""Export an arbitrary SQL segment to CSV.

Requires: pip install psycopg[binary] pandas
Env: NEON_DSN

Usage:
  python export_segment.py "<sql>" <out_csv>

Notes:
- Use LIMIT during testing.
- Keep SQL deterministic (include ORDER BY) when exports must be stable.
"""

import os
import sys
import pandas as pd
import psycopg

if len(sys.argv) < 3:
    print('Usage: python export_segment.py "<sql>" <out_csv>')
    sys.exit(1)

sql = sys.argv[1]
out_csv = sys.argv[2]

conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    df = pd.read_sql(sql, conn)

df.to_csv(out_csv, index=False)
print(f"Exported {len(df)} rows -> {out_csv}")
