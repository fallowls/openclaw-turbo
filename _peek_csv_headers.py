import sys, csv
path=sys.argv[1]
with open(path, 'r', encoding='utf-8-sig', newline='') as f:
    r=csv.reader(f)
    headers=next(r)
print('columns', len(headers))
print('\n'.join(headers))
