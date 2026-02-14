import pandas as pd
from pathlib import Path

xlsx = Path(r"C:\Users\Administrator\.openclaw\workspace\Stonewater_Karjat_Quote.xlsx")

opt = pd.read_excel(xlsx, sheet_name="Optional Charges")
opt = opt[opt["Add On Services"].str.strip().str.lower() != "dj with sound & light".lower()]

with pd.ExcelWriter(xlsx, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    opt.to_excel(writer, sheet_name="Optional Charges", index=False)

rows = []
acc = pd.read_excel(xlsx, sheet_name="Accommodation")
for _, r in acc.iterrows():
    rows.append({"Section": "Accommodation", "Item": r["Field"], "Details": r["Value"], "Timeframe/Notes": ""})

pricing = pd.read_excel(xlsx, sheet_name="Pricing")
for _, r in pricing.iterrows():
    rows.append({
        "Section": "Pricing",
        "Item": r["Room Category"],
        "Details": f"Rooms: {r['No. of Rooms']} | {r['Room Tariff (Per Room Per Night)']}",
        "Timeframe/Notes": ""
    })

optional = pd.read_excel(xlsx, sheet_name="Optional Charges")
for _, r in optional.iterrows():
    rows.append({"Section": "Optional Charges", "Item": r["Add On Services"], "Details": r["Charges"], "Timeframe/Notes": r.get("Timeframe", "")})

venue = pd.read_excel(xlsx, sheet_name="Venue Rental")
for _, r in venue.iterrows():
    rows.append({"Section": "Venue Rental", "Item": r["Venue"], "Details": r["Charges"], "Timeframe/Notes": r["Timeframe"]})

inclusions = pd.read_excel(xlsx, sheet_name="Inclusions")
for _, r in inclusions.iterrows():
    rows.append({"Section": "Inclusions", "Item": r["Inclusions"], "Details": "", "Timeframe/Notes": ""})

all_df = pd.DataFrame(rows, columns=["Section", "Item", "Details", "Timeframe/Notes"])
with pd.ExcelWriter(xlsx, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    all_df.to_excel(writer, sheet_name="All_In_One", index=False)

print("OK")
