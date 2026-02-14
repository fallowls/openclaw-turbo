import pg from 'pg';
const { Client } = pg;
const dsn = 'postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require';

const sql = process.argv[2];
if (!sql) {
  console.error('Usage: node _tmp_neon_query.mjs "SQL"');
  process.exit(2);
}

const params = process.argv.slice(3);

const c = new Client({ connectionString: dsn });
await c.connect();
try {
  const r = await c.query(sql, params);
  console.log(JSON.stringify(r.rows, null, 2));
} finally {
  await c.end();
}
