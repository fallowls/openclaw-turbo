import os, psycopg

dsn = os.environ.get('NEON_DSN')
if not dsn:
    raise SystemExit('NEON_DSN env var not set')

TITLE_BASE = "title is not null and title <> '' and title ilike '%procurement%'"
ROLE_MANAGER = "title ilike '%manager%'"
ROLE_DIRECTOR = "title ilike '%director%'"
EMP = "employee_count between 200 and 500"

IND_CONSTRUCTION = "industry ilike '%construction%'"
IND_MANUFACTURING = "industry ilike '%manufactur%'"  # catches manufacturing/manufacturer
IND_BOTH = f"({IND_CONSTRUCTION} or {IND_MANUFACTURING})"

queries = {
    'total_procurement_mgr_or_dir_200_500_both_industries': f"select count(*) from leads where {EMP} and {IND_BOTH} and {TITLE_BASE} and ({ROLE_MANAGER} or {ROLE_DIRECTOR})",

    'construction_procurement_manager_200_500': f"select count(*) from leads where {EMP} and {IND_CONSTRUCTION} and {TITLE_BASE} and {ROLE_MANAGER}",
    'construction_procurement_director_200_500': f"select count(*) from leads where {EMP} and {IND_CONSTRUCTION} and {TITLE_BASE} and {ROLE_DIRECTOR}",

    'manufacturing_procurement_manager_200_500': f"select count(*) from leads where {EMP} and {IND_MANUFACTURING} and {TITLE_BASE} and {ROLE_MANAGER}",
    'manufacturing_procurement_director_200_500': f"select count(*) from leads where {EMP} and {IND_MANUFACTURING} and {TITLE_BASE} and {ROLE_DIRECTOR}",

    'both_industries_procurement_manager_200_500': f"select count(*) from leads where {EMP} and {IND_BOTH} and {TITLE_BASE} and {ROLE_MANAGER}",
    'both_industries_procurement_director_200_500': f"select count(*) from leads where {EMP} and {IND_BOTH} and {TITLE_BASE} and {ROLE_DIRECTOR}",

    'industry_breakdown_mgr_or_dir': f"""
      select
        case
          when {IND_CONSTRUCTION} then 'Construction'
          when {IND_MANUFACTURING} then 'Manufacturing'
          else 'Other'
        end as bucket,
        count(*)
      from leads
      where {EMP} and {IND_BOTH} and {TITLE_BASE} and ({ROLE_MANAGER} or {ROLE_DIRECTOR})
      group by 1
      order by 2 desc
    """,
}

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        out = {}
        for k, q in queries.items():
            cur.execute(q)
            rows = cur.fetchall()
            out[k] = rows

# Pretty print
for k, rows in out.items():
    if len(rows) == 1 and len(rows[0]) == 1:
        print(f"{k}: {rows[0][0]}")
    else:
        print(f"\n{k}:")
        for r in rows:
            print('  ', r)
