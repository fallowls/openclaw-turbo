# Dedupe Rules

Priority order:
1) **Email** (case-insensitive)
2) **Person LinkedIn URL** (normalized)
3) **First + Last + Company** (normalized)

When conflicts occur:
- **Do not delete existing rows**
- **Update missing fields only** (preserve existing values)
- Prefer rows with any phone number + complete profile
