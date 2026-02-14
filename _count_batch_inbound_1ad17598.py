import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute("select count(*) from leads where batch_id=%s", ('inbound_1ad17598_20260210',))
    print(cur.fetchone()[0])
