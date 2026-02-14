import os, psycopg
conn=psycopg.connect(os.environ['NEON_DSN'])
with conn:
  with conn.cursor() as cur:
    cur.execute("""
      select column_name, data_type
      from information_schema.columns
      where table_name='companies'
      order by ordinal_position
    """)
    rows=cur.fetchall()
    print(rows)
