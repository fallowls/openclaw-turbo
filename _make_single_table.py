import pandas as pd
from pathlib import Path

xlsx = Path(r"C:\Users\Administrator\.openclaw\workspace\Stonewater_Karjat_Quote.xlsx")

rows = []

# Accommodation
acc = pd.read_excel(xlsx, sheet_name="Accommodation")
for _, r in acc.iterrows():
    rows.append({"Section": "Accommodation", "Item": r["Field"], "Details": r["Value"], "Timeframe/Notes": ""})

# Pricing
pricing = pd.read_excel(xlsx, sheet_name="Pricing")
for _, r in pricing.iterrows():
    rows.append({"Section": "Pricing", "Item": r["Room Category"], "Details": f"Rooms: {r['No. of Rooms']} | {r['Room Tariff (Per Room Per Night)']}", "Timeframe/Notes": ""})

# Optional Charges
optional = pd.read_excel(xlsx, sheet_name="Optional Charges")
for _, r in optional.iterrows():
    rows.append({"Section": "Optional Charges", "Item": r["Add On Services"], "Details": r["Charges"], "Timeframe/Notes": r.get("Timeframe", "")})

# Venue Rental
venue = pd.read_excel(xlsx, sheet_name="Venue Rental")
for _, r in venue.iterrows():
    rows.append({"Section": "Venue Rental", "Item": r["Venue"], "Details": r["Charges"], "Timeframe/Notes": r["Timeframe"]})

# Inclusions
inclusions = pd.read_excel(xlsx, sheet_name="Inclusions")
for _, r in inclusions.iterrows():
    rows.append({"Section": "Inclusions", "Item": r["Inclusions"], "Details": "", "Timeframe/Notes": ""})

all_df = pd.DataFrame(rows, columns=["Section", "Item", "Details", "Timeframe/Notes"])

# Write to new sheet
with pd.ExcelWriter(xlsx, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    all_df.to_excel(writer, sheet_name="All_In_One", index=False)

print("OK")
