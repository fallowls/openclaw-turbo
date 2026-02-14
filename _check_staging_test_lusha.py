import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute("select batch_id, count(*) from staging_lusha group by batch_id order by count(*) desc limit 5")
    print(cur.fetchall())
