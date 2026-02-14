import pandas as pd
import re

def parse_revenue(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    if not s:
        return None
    # remove currency symbols and commas
    s = re.sub(r"[^0-9\.a-z]", "", s)
    # handle ranges like 50m-100m
    if '-' in s:
        s = s.split('-')[0]
    mult = 1
    if s.endswith('b'):
        mult = 1_000_000_000
        s = s[:-1]
    elif s.endswith('m'):
        mult = 1_000_000
        s = s[:-1]
    elif s.endswith('k'):
        mult = 1_000
        s = s[:-1]
    try:
        return float(s) * mult
    except Exception:
        return None

# Apollo
apollo_path = r"C:\Users\Administrator\.openclaw\workspace\bunny_apollo\combined_apollo_filtered.csv"
apollo_out = r"C:\Users\Administrator\Downloads\LTI\apollo_it_manager_mexico_50m.csv"
apollo = pd.read_csv(apollo_path, dtype=str)

# columns
apollo_title_col = next((c for c in apollo.columns if c.lower() == 'title'), None)
apollo_country_col = next((c for c in apollo.columns if c.lower() in ['country','company country']), None)
apollo_rev_col = next((c for c in apollo.columns if c.lower() in ['annual revenue','revenue','company revenue']), None)

if apollo_title_col and apollo_country_col and apollo_rev_col:
    apollo['__rev'] = apollo[apollo_rev_col].map(parse_revenue)
    apollo_mask = (
        apollo[apollo_title_col].fillna('').str.lower().str.contains('it manager') &
        apollo[apollo_country_col].fillna('').str.lower().eq('mexico') &
        (apollo['__rev'].fillna(0) >= 50_000_000)
    )
    apollo_filtered = apollo[apollo_mask].copy()
    apollo_filtered.to_csv(apollo_out, index=False)
    print('apollo_rows', len(apollo_filtered))
else:
    print('apollo_missing_cols', apollo_title_col, apollo_country_col, apollo_rev_col)

# Lusha
lusha_path = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
lusha_out = r"C:\Users\Administrator\Downloads\LTI\lusha_it_manager_mexico_50m.csv"
lusha = pd.read_csv(lusha_path, dtype=str)

lusha_title_col = next((c for c in lusha.columns if c.lower() in ['job title','title']), None)
lusha_country_col = next((c for c in lusha.columns if c.lower() in ['country','company country']), None)
lusha_rev_col = next((c for c in lusha.columns if c.lower() in ['company revenue','revenue']), None)

if lusha_title_col and lusha_country_col and lusha_rev_col:
    lusha['__rev'] = lusha[lusha_rev_col].map(parse_revenue)
    lusha_mask = (
        lusha[lusha_title_col].fillna('').str.lower().str.contains('it manager') &
        lusha[lusha_country_col].fillna('').str.lower().eq('mexico') &
        (lusha['__rev'].fillna(0) >= 50_000_000)
    )
    lusha_filtered = lusha[lusha_mask].copy()
    lusha_filtered.to_csv(lusha_out, index=False)
    print('lusha_rows', len(lusha_filtered))
else:
    print('lusha_missing_cols', lusha_title_col, lusha_country_col, lusha_rev_col)
