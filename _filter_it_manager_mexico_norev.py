import pandas as pd

# Apollo
apollo_path = r"C:\Users\Administrator\.openclaw\workspace\bunny_apollo\combined_apollo_filtered.csv"
apollo_out = r"C:\Users\Administrator\Downloads\LTI\apollo_it_manager_mexico.csv"
apollo = pd.read_csv(apollo_path, dtype=str)

apollo_title_col = next((c for c in apollo.columns if c.lower() == 'title'), None)
apollo_country_col = next((c for c in apollo.columns if c.lower() in ['country','company country']), None)

if apollo_title_col and apollo_country_col:
    apollo_mask = (
        apollo[apollo_title_col].fillna('').str.lower().str.contains('it manager') &
        apollo[apollo_country_col].fillna('').str.lower().eq('mexico')
    )
    apollo_filtered = apollo[apollo_mask].copy()
    apollo_filtered.to_csv(apollo_out, index=False)
    print('apollo_rows', len(apollo_filtered))
else:
    print('apollo_missing_cols', apollo_title_col, apollo_country_col)

# Lusha
lusha_path = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
lusha_out = r"C:\Users\Administrator\Downloads\LTI\lusha_it_manager_mexico.csv"
lusha = pd.read_csv(lusha_path, dtype=str)

lusha_title_col = next((c for c in lusha.columns if c.lower() in ['job title','title']), None)
lusha_country_col = next((c for c in lusha.columns if c.lower() in ['country','company country']), None)

if lusha_title_col and lusha_country_col:
    lusha_mask = (
        lusha[lusha_title_col].fillna('').str.lower().str.contains('it manager') &
        lusha[lusha_country_col].fillna('').str.lower().eq('mexico')
    )
    lusha_filtered = lusha[lusha_mask].copy()
    lusha_filtered.to_csv(lusha_out, index=False)
    print('lusha_rows', len(lusha_filtered))
else:
    print('lusha_missing_cols', lusha_title_col, lusha_country_col)
