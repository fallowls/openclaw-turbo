import os
import pandas as pd

folder = r"C:\Users\Administrator\Downloads\LTI\lusha\lusha"
files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.csv','.xlsx','.xls')) and not f.lower().startswith('.~lock')]
print('files', len(files))

frames = []
for f in files:
    try:
        if f.lower().endswith('.csv'):
            df = pd.read_csv(f, dtype=str)
        else:
            df = pd.read_excel(f, dtype=str)
        df['__source_file'] = os.path.basename(f)
        frames.append(df)
    except Exception as e:
        print('skip', f, e)

if frames:
    combined = pd.concat(frames, ignore_index=True)
    out_path = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
    combined.to_csv(out_path, index=False)
    print('saved', out_path, 'rows', len(combined))
else:
    print('no files merged')
