import csv
path = r"C:\Users\Administrator\.openclaw\workspace\bunny_apollo\combined_apollo_filtered.csv"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    headers = next(reader)
print(headers)
