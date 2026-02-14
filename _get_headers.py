import pandas as pd

paths = {
    'LTI_Tal': r"C:\Users\Administrator\Downloads\LTI\LTI Tal.csv",
    'Lusha_Merged': r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv",
    'Apollo_Filtered': r"C:\Users\Administrator\.openclaw\workspace\bunny_apollo\combined_apollo_filtered.csv",
}

for name, path in paths.items():
    df = pd.read_csv(path, dtype=str, nrows=5)
    print(f"--- {name} ---")
    for c in df.columns:
        print(c)
    print()
