import pandas as pd

apollo_path = r"C:\Users\Administrator\Downloads\LTI\apollo_it_manager_mexico.csv"
lusha_path = r"C:\Users\Administrator\Downloads\LTI\lusha_it_manager_mexico.csv"
out_path = r"C:\Users\Administrator\Downloads\LTI\it_manager_mexico_merged.csv"

apollo = pd.read_csv(apollo_path, dtype=str)
lusha = pd.read_csv(lusha_path, dtype=str)

# Normalize column names
apollo_cols = {c.lower(): c for c in apollo.columns}
lusha_cols = {c.lower(): c for c in lusha.columns}

# Helper to get column value safely

def get_col(df, cols, key):
    col = cols.get(key.lower())
    return df[col] if col else pd.Series([None] * len(df))

# Build Apollo output
apollo_out = pd.DataFrame({
    "First Name": get_col(apollo, apollo_cols, "First Name"),
    "Last Name": get_col(apollo, apollo_cols, "Last Name"),
    "Title": get_col(apollo, apollo_cols, "Title"),
    "Company": get_col(apollo, apollo_cols, "Company Name"),
    "Email": get_col(apollo, apollo_cols, "Email"),
    "Mobile Phone": get_col(apollo, apollo_cols, "Mobile Phone"),
    "Other Phone": get_col(apollo, apollo_cols, "Other Phone"),
    "Corporate Phone": get_col(apollo, apollo_cols, "Corporate Phone"),
    "Person Linkedin Url": get_col(apollo, apollo_cols, "Person Linkedin Url"),
    "Company Linkedin Url": get_col(apollo, apollo_cols, "Company Linkedin Url"),
    "Website": get_col(apollo, apollo_cols, "Website"),
    "State": get_col(apollo, apollo_cols, "State"),
    "Country": get_col(apollo, apollo_cols, "Country"),
    "Time Zone": None,
})

# Build Lusha output
lusha_out = pd.DataFrame({
    "First Name": get_col(lusha, lusha_cols, "First name"),
    "Last Name": get_col(lusha, lusha_cols, "Last name"),
    "Title": get_col(lusha, lusha_cols, "Job title"),
    "Company": get_col(lusha, lusha_cols, "Company name"),
    "Email": get_col(lusha, lusha_cols, "Work email"),
    "Mobile Phone": get_col(lusha, lusha_cols, "Phone 1"),
    "Other Phone": get_col(lusha, lusha_cols, "Phone 2"),
    "Corporate Phone": None,
    "Person Linkedin Url": get_col(lusha, lusha_cols, "Linkedin URL"),
    "Company Linkedin Url": get_col(lusha, lusha_cols, "Company Linkedin URL"),
    "Website": get_col(lusha, lusha_cols, "Company website"),
    "State": get_col(lusha, lusha_cols, "State"),
    "Country": get_col(lusha, lusha_cols, "Country"),
    "Time Zone": None,
})

merged = pd.concat([apollo_out, lusha_out], ignore_index=True)
merged.to_csv(out_path, index=False)
print(out_path, 'rows', len(merged))
