import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    for t in ['staging_lusha','staging_apollo']:
      cur.execute(f"select count(*) from {t}")
      print(t, cur.fetchone()[0])
