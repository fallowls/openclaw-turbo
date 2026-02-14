-- Normalize NaN/NA/blank strings to NULL
update leads set
  title = nullif(nullif(lower(title), 'nan'), 'na')
where title is not null;

update leads set
  email_primary = nullif(nullif(lower(email_primary), 'nan'), 'na')
where email_primary is not null;

update leads set
  email_secondary = nullif(nullif(lower(email_secondary), 'nan'), 'na')
where email_secondary is not null;
