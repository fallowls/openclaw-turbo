import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute("select count(*) from leads where batch_id like %s", ('zip6f4c8265%',))
    print(cur.fetchone()[0])
