import psycopg

dsn='postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute("select pg_size_pretty(pg_database_size(current_database()))")
        print('db_size', cur.fetchone()[0])

        cur.execute(
            """
            select relname,
                   pg_size_pretty(pg_total_relation_size(c.oid)) as total,
                   pg_total_relation_size(c.oid) as total_bytes
            from pg_class c
            join pg_namespace n on n.oid = c.relnamespace
            where n.nspname='public' and c.relkind in ('r','m')
            order by total_bytes desc
            limit 30
            """
        )
        print('\nTop tables:')
        for name, total, _ in cur.fetchall():
            print(f"{name}\t{total}")
