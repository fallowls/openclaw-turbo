# Segments (recipes)

Use these as starting points; adjust WHERE clauses as needed.

## Finance Director (intent-style)
- has email + any phone
- order by last_raised_at desc, latest_funding desc

```sql
select *
from leads
where title is not null
  and lower(title) like '%finance director%'
  and email_primary is not null
  and (phone_mobile is not null or phone_work is not null or phone_other is not null)
order by
  (case when last_raised_at is null then 1 else 0 end),
  last_raised_at desc nulls last,
  latest_funding desc nulls last;
```

## Missing-fields enrichment queue
```sql
select * from leads
where email_primary is null
   or linkedin_person_url is null
   or (phone_mobile is null and phone_work is null and phone_other is null);
```
