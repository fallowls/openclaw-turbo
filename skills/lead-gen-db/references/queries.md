# Prebuilt Queries (Phase 3)

## 1) By title + country
```sql
select * from leads
where lower(title) like '%it manager%'
  and lower(person_country) = 'mexico';
```

## 2) By revenue range
```sql
select * from leads
where revenue >= 50000000 and revenue <= 200000000;
```

## 3) Missing fields (enrichment queue)
```sql
select * from leads
where email_primary is null
   or linkedin_person_url is null
   or (phone_mobile is null and phone_work is null and phone_other is null);
```

## 4) Newest batch
```sql
select * from leads
where batch_id = 'BATCH_YYYYMMDD';
```
