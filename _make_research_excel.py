import pandas as pd
from datetime import datetime

# Data extracted from research
data = [
    {
        "Company Name": "Airbus",
        "Industry": "Aerospace & Defence",
        "Investment/Expansion Details": "Deepening presence in manufacturing, engineering, training. Plan to source $2B components by 2030.",
        "Locations": "India-wide (Supply Chain); C295 manufacturing with Tata",
        "Key Context": "Aligning with 'Make in India'; C295 military transport aircraft production.",
        "Source Link": "https://www.investindia.gov.in/team-india-blogs/10-global-corporations-expanding-operations-india-2025"
    },
    {
        "Company Name": "Microsoft",
        "Industry": "Technology / Cloud / AI",
        "Investment/Expansion Details": "$3 Billion investment over next 2 years.",
        "Locations": "India-wide (Data Centers)",
        "Key Context": "Expanding cloud and AI infrastructure; supporting data center capacity growth.",
        "Source Link": "https://news.microsoft.com/en-in/microsoft-announces-us-3bn-investment-over-two-years-in-india-cloud-and-ai-infrastructure-to-accelerate-adoption-of-ai-skilling-and-innovation/"
    },
    {
        "Company Name": "Apple Inc.",
        "Industry": "Consumer Electronics",
        "Investment/Expansion Details": "Recorded $22 Billion assembling in April 2025 alone.",
        "Locations": "Various (Manufacturing units)",
        "Key Context": "Diversifying from China; 60% rise in production; 300+ manufacturing units ecosystem.",
        "Source Link": "https://economictimes.indiatimes.com/industry/cons-products/electronics/apple-india-produces-22-billion-of-iphones-in-shift-from-china/articleshow/120245833.cms"
    },
    {
        "Company Name": "Foxconn",
        "Industry": "Electronics Manufacturing",
        "Investment/Expansion Details": "$1.48 Billion investment; 3 new plants.",
        "Locations": "Chennai, Bengaluru, Hyderabad; Semiconductor unit in Uttar Pradesh",
        "Key Context": "Supporting Apple production; JV with HCL for semiconductors.",
        "Source Link": "https://timesofindia.indiatimes.com/business/india-business/apple-vendor-foxconn-pumps-1-48-billion-into-tamil-nadu-unit/articleshow/121274001.cms"
    },
    {
        "Company Name": "Amazon (AWS)",
        "Industry": "Cloud Computing / E-commerce",
        "Investment/Expansion Details": "$8.2 Billion in AWS (Maharashtra); $233 Million for Operations (2025).",
        "Locations": "Maharashtra (AWS); India-wide (Operations)",
        "Key Context": "Data storage demand due to AI; enhancing fulfilment network and safety.",
        "Source Link": "https://www.reuters.com/technology/amazons-cloud-business-invest-82-billion-indian-state-coming-years-2025-03-03/"
    },
    {
        "Company Name": "Samsung",
        "Industry": "Consumer Electronics",
        "Investment/Expansion Details": "Enhancing manufacturing capabilities; diversifying from Vietnam.",
        "Locations": "Noida, Chennai",
        "Key Context": "World's largest mobile factory; producing flagship phones.",
        "Source Link": "https://news.samsung.com/in/samsung-inaugurates-worlds-largest-mobile-factory-in-india"
    },
    {
        "Company Name": "NTT Data",
        "Industry": "IT Services / Infrastructure",
        "Investment/Expansion Details": "Biggest data center campus (500 MW capacity); MIST submarine cable.",
        "Locations": "Mumbai (Data Centers)",
        "Key Context": "IOWN technology deployment; MIST cable connecting Malaysia, India, Singapore, Thailand.",
        "Source Link": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2132817"
    },
    {
        "Company Name": "VinFast",
        "Industry": "Automotive (EV)",
        "Investment/Expansion Details": "$2 Billion for EV plant; considering further expansion.",
        "Locations": "Thoothukudi (Tamil Nadu); considering Andhra Pradesh",
        "Key Context": "Operations expected by late 2025; targeting Tier 2/3 cities for affordable EVs.",
        "Source Link": "https://economictimes.indiatimes.com/industry/renewables/vietnams-vinfast-plots-deeper-india-push-after-2-bn-tamil-nadu-bet-eyes-andhra-and-telangana/articleshow/121546283.cms"
    },
    {
        "Company Name": "Nissan / Renault",
        "Industry": "Automotive",
        "Investment/Expansion Details": "₹5,300 Crores investment by FY27.",
        "Locations": "Chennai (Manufacturing base)",
        "Key Context": "Introducing new models; enhancing manufacturing for export and local market.",
        "Source Link": "https://www.nissan.in/latest-news/renault-and-nissan-renew-commitment-to-indian-operations-through-new-investment-and-vehicles.html"
    },
    {
        "Company Name": "Nestlé",
        "Industry": "FMCG",
        "Investment/Expansion Details": "₹4,200 Crore for new plant.",
        "Locations": "Odisha",
        "Key Context": "Strengthening supply chain; acquired stake in pet food firm Drools.",
        "Source Link": "https://www.investindia.gov.in/team-india-blogs/10-global-corporations-expanding-operations-india-2025"
    },
    {
        "Company Name": "AISIN Corporation",
        "Industry": "Automotive Components",
        "Investment/Expansion Details": "32 Billion Yen investment.",
        "Locations": "Maharashtra",
        "Key Context": "New plant for eAxles starting 2025.",
        "Source Link": "https://www.aisin.com/en/news/2026/010482.html"
    },
    {
        "Company Name": "Marriott International",
        "Industry": "Hospitality",
        "Investment/Expansion Details": "Rapid expansion into smaller towns.",
        "Locations": "Tier-2 and Tier-3 cities",
        "Key Context": "Capitalizing on high revenue growth in India.",
        "Source Link": "https://www.google.com/search?q=Marriott+International+India+expansion"
    },
    {
        "Company Name": "Mahindra & Mahindra",
        "Industry": "Automotive",
        "Investment/Expansion Details": "$1.65 Billion over 10 years.",
        "Locations": "Western India",
        "Key Context": "Expanding manufacturing footprint.",
        "Source Link": "https://www.reuters.com/world/india/indian-automaker-mahindra-invest-165-billion-over-decade-expand-manufacturing-2026-02-06/"
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# File path
file_path = "India_Expansion_Research_2025.xlsx"

# Write to Excel
df.to_excel(file_path, index=False)

print(f"Excel file created at: {file_path}")
