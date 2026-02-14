import psycopg

dsn='postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

TOKENS = ["nan", "na", "n/a", "null", "none", "unavailable", ""]

def main():
    with psycopg.connect(dsn) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            # text-like columns only
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema='public'
                  AND table_name='leads'
                  AND data_type IN ('character varying','text','character')
                ORDER BY ordinal_position
                """
            )
            cols = [r[0] for r in cur.fetchall()]

            total_updates = 0
            for col in cols:
                # Build a safe statement using identifier quoting
                # Normalize whitespace then compare lower(value)
                stmt = f"""
                UPDATE leads
                SET {psycopg.sql.Identifier(col).as_string(conn)} = NULL
                WHERE {psycopg.sql.Identifier(col).as_string(conn)} IS NOT NULL
                  AND lower(btrim({psycopg.sql.Identifier(col).as_string(conn)})) = ANY(%s)
                """
                cur.execute(stmt, (TOKENS,))
                updated = cur.rowcount if cur.rowcount is not None else 0
                if updated:
                    total_updates += updated
                    print(f"{col}: {updated}")

            print(f"TOTAL_UPDATED={total_updates}")

if __name__ == '__main__':
    main()
