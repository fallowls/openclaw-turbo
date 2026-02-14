import pandas as pd
import sys
path=sys.argv[1]
df=pd.read_csv(path, nrows=0)
for c in df.columns:
    print(c)
