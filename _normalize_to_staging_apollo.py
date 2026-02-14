import csv, json, re, sys
from pathlib import Path

STAGING_HEADERS = [
    'batch_id','first_name','last_name','title','seniority','departments','linkedin_person_url',
    'email_primary','email_secondary','email_confidence','email_verified',
    'phone_mobile','phone_work','phone_other',
    'person_city','person_state','person_country',
    'company_name','company_name_for_emails','company_website','company_linkedin_url','industry',
    'company_description','keywords','technologies','employee_count','revenue','year_founded',
    'company_phone','company_address','company_city','company_state','company_country',
    'total_funding','latest_funding','last_raised_at','source_person_id','source_company_id',
    'stage','last_contacted','lists','extra_json'
]


def norm(s: str | None) -> str:
    if s is None:
        return ''
    s = str(s).strip()
    if s.lower() in {'nan','na','n/a','null','none',''}:
        return ''
    return s


def pick(*vals):
    for v in vals:
        v = norm(v)
        if v:
            return v
    return ''


def map_phones(row: dict, pairs: list[tuple[str,str]]):
    mobile = work = other = ''
    for num_key, type_key in pairs:
        num = norm(row.get(num_key))
        if not num:
            continue
        typ = norm(row.get(type_key)).lower()
        if any(k in typ for k in ['mobile','cell']):
            if not mobile:
                mobile = num
            else:
                other = other or num
        elif any(k in typ for k in ['work','direct']):
            if not work:
                work = num
            else:
                other = other or num
        else:
            other = other or num
    return mobile, work, other


def detect_format(headers: list[str]) -> str:
    hs = {h.strip().lower() for h in headers}
    if 'job title' in hs and 'company number of employees' in hs and 'work email' in hs:
        return 'apollo_export_contacts'
    if 'apollo contact id' in hs and '# employees' in hs and 'person linkedin url' in hs:
        return 'apollo_mexico_like'
    # fallback
    return 'unknown'


def main():
    if len(sys.argv) < 4:
        print('Usage: python _normalize_to_staging_apollo.py <input_csv> <output_csv> <batch_id>')
        raise SystemExit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    batch_id = sys.argv[3]

    with in_path.open('r', encoding='utf-8-sig', errors='ignore', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit('No headers detected')
        fmt = detect_format(reader.fieldnames)

        with out_path.open('w', encoding='utf-8', newline='') as out_f:
            w = csv.DictWriter(out_f, fieldnames=STAGING_HEADERS)
            w.writeheader()

            n = 0
            for row in reader:
                out = {h: '' for h in STAGING_HEADERS}
                out['batch_id'] = batch_id

                if fmt == 'apollo_export_contacts':
                    out['first_name'] = norm(row.get('First Name'))
                    out['last_name'] = norm(row.get('Last Name'))
                    out['title'] = norm(row.get('Job Title'))
                    out['seniority'] = norm(row.get('Seniority'))
                    out['departments'] = norm(row.get('Departments'))
                    out['linkedin_person_url'] = norm(row.get('LinkedIn URL'))

                    work_email = norm(row.get('Work Email'))
                    direct_email = norm(row.get('Direct Email'))
                    out['email_primary'] = pick(work_email, direct_email)
                    if direct_email and direct_email != out['email_primary']:
                        out['email_secondary'] = direct_email
                    out['email_confidence'] = pick(row.get('Work Email Confidence'), row.get('Direct Email Confidence'))

                    m, wk, ot = map_phones(row, [('Phone 1','Phone 1 Type'), ('Phone 2','Phone 2 Type')])
                    out['phone_mobile'] = m
                    out['phone_work'] = wk
                    out['phone_other'] = ot

                    out['person_city'] = norm(row.get('City'))
                    out['person_state'] = norm(row.get('State'))
                    out['person_country'] = norm(row.get('Country'))

                    out['company_name'] = norm(row.get('Company Name'))
                    out['company_website'] = norm(row.get('Company Website'))
                    out['company_linkedin_url'] = norm(row.get('Company linkedin URL'))
                    out['industry'] = pick(row.get('Company Main Industry'), row.get('Company Sub Industry'))
                    out['company_description'] = norm(row.get('Company Description'))
                    out['technologies'] = norm(row.get('Company Technologies'))
                    out['employee_count'] = norm(row.get('Company Number of Employees'))
                    out['revenue'] = norm(row.get('Company Revenue'))
                    out['year_founded'] = norm(row.get('Company Year Founded'))
                    out['company_city'] = norm(row.get('Company City'))
                    out['company_state'] = norm(row.get('Company State'))
                    out['company_country'] = norm(row.get('Company Country'))
                    out['total_funding'] = norm(row.get('Total Funding Amount'))
                    out['latest_funding'] = pick(row.get('Last Round/Event Amount'), row.get('Last Round/Event Amount'))
                    out['last_raised_at'] = norm(row.get('Last Round/Event Date'))

                    extra = {
                        'company_domain': norm(row.get('Company Domain')),
                        'tags': norm(row.get('Tags')),
                        'topic_count_trend': norm(row.get('Topic Count Trend')),
                        'company_intent_topics': norm(row.get('Company Intent Topics')),
                        'company_intent_level': norm(row.get('Company Intent Level')),
                    }
                    out['extra_json'] = json.dumps({k:v for k,v in extra.items() if v}, ensure_ascii=False)

                elif fmt == 'apollo_mexico_like':
                    out['first_name'] = norm(row.get('First Name'))
                    out['last_name'] = norm(row.get('Last Name'))
                    out['title'] = norm(row.get('Title'))
                    out['seniority'] = norm(row.get('Seniority'))
                    out['departments'] = norm(row.get('Departments'))
                    out['linkedin_person_url'] = norm(row.get('Person Linkedin Url'))

                    out['email_primary'] = norm(row.get('Email'))
                    out['email_secondary'] = norm(row.get('Secondary Email'))
                    out['email_confidence'] = norm(row.get('Email Confidence'))

                    out['phone_work'] = pick(row.get('Work Direct Phone'))
                    out['phone_mobile'] = pick(row.get('Mobile Phone'))
                    out['phone_other'] = pick(row.get('Corporate Phone'), row.get('Other Phone'))

                    out['stage'] = norm(row.get('Stage'))
                    out['last_contacted'] = norm(row.get('Last Contacted'))
                    out['lists'] = norm(row.get('Lists'))

                    out['person_city'] = norm(row.get('City'))
                    out['person_state'] = norm(row.get('State'))
                    out['person_country'] = norm(row.get('Country'))

                    out['company_name'] = norm(row.get('Company Name'))
                    out['company_name_for_emails'] = norm(row.get('Company Name for Emails'))
                    out['company_website'] = norm(row.get('Website'))
                    out['company_linkedin_url'] = norm(row.get('Company Linkedin Url'))
                    out['industry'] = norm(row.get('Industry'))
                    out['keywords'] = norm(row.get('Keywords'))
                    out['technologies'] = norm(row.get('Technologies'))
                    out['employee_count'] = norm(row.get('# Employees'))
                    out['revenue'] = norm(row.get('Annual Revenue'))
                    out['total_funding'] = norm(row.get('Total Funding'))
                    out['latest_funding'] = norm(row.get('Latest Funding Amount'))
                    out['last_raised_at'] = norm(row.get('Last Raised At'))
                    out['company_address'] = norm(row.get('Company Address'))
                    out['company_city'] = norm(row.get('Company City'))
                    out['company_state'] = norm(row.get('Company State'))
                    out['company_country'] = norm(row.get('Company Country'))
                    out['company_phone'] = norm(row.get('Company Phone'))

                    out['source_person_id'] = norm(row.get('Apollo Contact Id'))
                    out['source_company_id'] = norm(row.get('Apollo Account Id'))

                    extra = {
                        'email_status': norm(row.get('Email Status')),
                        'primary_email_source': norm(row.get('Primary Email Source')),
                        'secondary_email_status': norm(row.get('Secondary Email Status')),
                        'facebook_url': norm(row.get('Facebook Url')),
                        'twitter_url': norm(row.get('Twitter Url')),
                        'apollo_company': norm(row.get('Company')),
                    }
                    out['extra_json'] = json.dumps({k:v for k,v in extra.items() if v}, ensure_ascii=False)
                else:
                    # unknown format: store raw row
                    out['extra_json'] = json.dumps({'raw': row}, ensure_ascii=False)

                # drop rows that are totally empty
                if not (out['first_name'] or out['last_name'] or out['email_primary'] or out['linkedin_person_url']):
                    continue

                w.writerow(out)
                n += 1

    print(f'normalized_rows={n} format={fmt} out={out_path}')


if __name__ == '__main__':
    main()
