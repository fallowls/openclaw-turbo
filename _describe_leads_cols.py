import psycopg

dsn='postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute("select column_name from information_schema.columns where table_schema='public' and table_name='leads' order by ordinal_position")
        cols=[r[0] for r in cur.fetchall()]
print('cols',len(cols))
for c in cols:
    print(c)
