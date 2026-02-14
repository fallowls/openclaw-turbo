import pandas as pd
from pathlib import Path

base = Path(r"C:\Users\Administrator\.openclaw\workspace")
file_path = base / "Stonewater_Karjat_Quote.xlsx"

accommodation = pd.DataFrame([
    {"Field": "Check-in Date", "Value": "18 Feb 2026"},
    {"Field": "Check-out Date", "Value": "19 Feb 2026"},
    {"Field": "Room type", "Value": "Mix categories"},
    {"Field": "Number of Guests", "Value": "75 pax"},
    {"Field": "Number of Rooms", "Value": "TBA"},
    {"Field": "Occupancy Type", "Value": "TBA"},
])

pricing = pd.DataFrame([
    {"Room Category": "The Cedar Room", "No. of Rooms": 48, "Room Tariff (Per Room Per Night)": "INR 17,500 + 18% taxes per double occupancy room per night."},
    {"Room Category": "Whispering Brook", "No. of Rooms": 15, "Room Tariff (Per Room Per Night)": "INR 18,500 + 18% taxes per double occupancy room per night."},
    {"Room Category": "Whispering Brook Riverview", "No. of Rooms": 15, "Room Tariff (Per Room Per Night)": "INR 19,500 + 18% taxes per double occupancy room per night."},
    {"Room Category": "Silver Spring Pool Access Room", "No. of Rooms": 18, "Room Tariff (Per Room Per Night)": "INR 20,500 + 18% taxes per double occupancy room per night."},
    {"Room Category": "Cascade Private Pool Cottage", "No. of Rooms": 8, "Room Tariff (Per Room Per Night)": "INR 30,000 + 18% taxes per double occupancy room per night."},
    {"Room Category": "Twin Leaf Pool Cottage", "No. of Rooms": 11, "Room Tariff (Per Room Per Night)": "INR 41,000 + 18% taxes per quadruple occupancy room per night."},
    {"Room Category": "Extra Person/Bed", "No. of Rooms": "TBA", "Room Tariff (Per Room Per Night)": "INR 6000 + 18% taxes per person/ per night."},
    {"Room Category": "Child Charges (06-11 YRS)", "No. of Rooms": "TBA", "Room Tariff (Per Room Per Night)": "INR 4000 + 18% taxes per kid/ per night."},
])

optional = pd.DataFrame([
    {"Add On Services": "DJ With Sound & Light", "Charges": "INR 40,000 + taxes", "Timeframe": "03 HRS"},
    {"Add On Services": "Karaoke Charges", "Charges": "INR 25,000 + Taxes", "Timeframe": "03 HRS"},
    {"Add On Services": "Bonfire Charges", "Charges": "INR 5000 + taxes", "Timeframe": "01 Time Set up"},
    {"Add On Services": "PA System, Projector & Screen", "Charges": "INR 20,000 + taxes", "Timeframe": "Per Day"},
    {"Add On Services": "2 HRS Unlimited Starters (02 Veg & 02 Non-Veg)", "Charges": "INR 1200 + taxes", "Timeframe": "Per Person"},
    {"Add On Services": "Additional Lunch OR Dinner", "Charges": "INR 1750 + taxes", "Timeframe": "Per Person"},
    {"Add On Services": "Evening High Tea", "Charges": "INR 1000 + taxes", "Timeframe": "Per Person"},
    {"Add On Services": "Non-Residential Guests Charges", "Charges": "On Request", "Timeframe": ""},
])

venue = pd.DataFrame([
    {"Venue": "Amara Banquet", "Charges": "INR 75,000 + Taxes", "Timeframe": "8 HRS"},
    {"Venue": "Ivory Ballroom", "Charges": "INR 2,00,000 + Taxes", "Timeframe": "8 HRS"},
    {"Venue": "Brookside Lawn (Riverside)", "Charges": "INR 1,50,000 + Taxes", "Timeframe": "12 HRS"},
    {"Venue": "The Marina Lawn (Poolside)", "Charges": "INR 2,00,000 + Taxes", "Timeframe": "12 HRS"},
])

inclusions = pd.DataFrame({
    "Inclusions": [
        "Welcome drink (Non-alcoholic) on arrival.",
        "Accommodation in a well-appointed airconditioned room with LED television.",
        "02 bottles of Mineral Water & Tea-Coffee Maker (replenished every day).",
        "Buffet Lunch, Dinner & Breakfast – 01 Cycle for per night booked.",
        "Complimentary Wi-Fi.",
        "Mini Refrigerator and Toiletries.",
        "Indoor Games & Outdoor Games (Not operational)",
        "Use of swimming pool, (swimming costumes are mandatory), as per resort timings.",
        "Parking facilities.",
    ]
})

with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    accommodation.to_excel(writer, sheet_name="Accommodation", index=False)
    pricing.to_excel(writer, sheet_name="Pricing", index=False)
    optional.to_excel(writer, sheet_name="Optional Charges", index=False)
    venue.to_excel(writer, sheet_name="Venue Rental", index=False)
    inclusions.to_excel(writer, sheet_name="Inclusions", index=False)

print(str(file_path))
