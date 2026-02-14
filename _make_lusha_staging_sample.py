import pandas as pd
import re

src = r"C:\Users\Administrator\Downloads\LTI\lusha_merged.csv"
out = r"C:\Users\Administrator\Downloads\LTI\lusha_staging_sample.csv"

def join_list(x):
    if pd.isna(x) or str(x).strip()=="":
        return ""
    return str(x)

# Load small sample
chunk = pd.read_csv(src, dtype=str, nrows=200)

st = pd.DataFrame({
    'batch_id': ['TEST_LUSHA']*len(chunk),
    'first_name': chunk.get('First name',''),
    'last_name': chunk.get('Last name',''),
    'title': chunk.get('Job title',''),
    'seniority': chunk.get('Seniority',''),
    'departments': chunk.get('Departments',''),
    'linkedin_person_url': chunk.get('Linkedin URL',''),
    'email_primary': chunk.get('Work email',''),
    'email_secondary': chunk.get('Personal email',''),
    'email_confidence': chunk.get('Email confidence',''),
    'email_verified': chunk.get('Email verified',''),
    'phone_mobile': chunk.get('Phone 1',''),
    'phone_work': chunk.get('Phone 3',''),
    'phone_other': chunk.get('Phone 2',''),
    'person_city': chunk.get('City',''),
    'person_state': chunk.get('State',''),
    'person_country': chunk.get('Country',''),
    'company_name': chunk.get('Company name',''),
    'company_name_for_emails': ['']*len(chunk),
    'company_website': chunk.get('Company website',''),
    'company_linkedin_url': chunk.get('Company Linkedin URL',''),
    'industry': chunk.get('Industry',''),
    'company_description': chunk.get('Company description',''),
    'keywords': chunk.get('Company keywords',''),
    'technologies': chunk.get('Technologies',''),
    'employee_count': chunk.get('Company size',''),
    'revenue': chunk.get('Company revenue',''),
    'year_founded': chunk.get('Company founded',''),
    'company_phone': chunk.get('Company phone',''),
    'company_address': chunk.get('Company address',''),
    'company_city': chunk.get('Company city',''),
    'company_state': chunk.get('Company state',''),
    'company_country': chunk.get('Company country',''),
    'total_funding': chunk.get('Total funding',''),
    'latest_funding': chunk.get('Latest funding',''),
    'last_raised_at': chunk.get('Last funding date',''),
    'source_person_id': chunk.get('Lusha Person ID',''),
    'source_company_id': chunk.get('Lusha Company ID',''),
    'stage': ['']*len(chunk),
    'last_contacted': ['']*len(chunk),
    'lists': ['']*len(chunk),
    'extra_json': ['{}']*len(chunk),
})

st.to_csv(out, index=False)
print(out, len(st))
