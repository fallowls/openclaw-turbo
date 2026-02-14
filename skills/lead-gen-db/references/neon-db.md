# Neon DB Connection

Use the provided Neon connection string via env var:

```
setx NEON_DSN "postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

Access from Python using `psycopg` or `psycopg2`.

Example:
```python
import os
import psycopg

conn = psycopg.connect(os.environ["NEON_DSN"])
```
