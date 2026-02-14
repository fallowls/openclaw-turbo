import pandas as pd
import glob, os
base=r"C:\Users\Administrator\.openclaw\workspace\inbound_merge"
paths=sorted(glob.glob(os.path.join(base,'*.csv')))
print('files:', paths)
dfs=[]
for p in paths:
    df=pd.read_csv(p, dtype=str, keep_default_na=False)
    df['_source_file']=os.path.basename(p)
    dfs.append(df)
all_df=pd.concat(dfs, ignore_index=True, sort=False)
print('rows:', len(all_df), 'cols:', len(all_df.columns))
out=r"C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts.csv"
all_df.to_csv(out, index=False)
print('wrote:', out)
