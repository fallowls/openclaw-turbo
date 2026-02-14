import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute("select count(*) from staging_lusha where batch_id=%s", ('TEST_LUSHA2',))
        print('staging_rows', cur.fetchone()[0])
        cur.execute("select count(*) from leads where batch_id=%s", ('TEST_LUSHA2',))
        print('lead_rows_batch', cur.fetchone()[0])
