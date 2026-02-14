import os, psycopg
conn = psycopg.connect(os.environ['NEON_DSN'])
with conn:
    with conn.cursor() as cur:
        cur.execute("update leads set title=null where title ilike 'nan' or title ilike 'na' or title=''")
        cur.execute("select count(*) from leads where title is null")
        print('null_titles', cur.fetchone()[0])
