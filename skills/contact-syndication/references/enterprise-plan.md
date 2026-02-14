# Enterprise Plan: Research → Acquire → Enrich → Store → Syndicate

Goal: Increase the size and quality of the lead database by continuously adding **net-new contacts** and enriching existing ones, using compliant data sources and repeatable workflows.

## 0) Definitions

- **Account**: A company you target (company_name + domain).
- **Contact**: A person at an account (name + role) with at least one reliable identifier (email/LinkedIn) and optionally phone.
- **Net-new**: A contact not already present in `leads` by (email_primary) or (linkedin_person_url).
- **Enrichment**: Filling missing fields, without overwriting existing values; extra values go to secondary fields.

## 1) Targeting Strategy (Accounts-first)

### 1.1 ICP + Segments
Create explicit segments (examples):
- Accounting/Finance decision-makers (CFO, Finance Director, Controller)
- IT leaders (IT Manager, Head of IT)
- Operations leadership (Ops Director, Site Lead)

### 1.2 Account sourcing (high-signal)
Prioritize sources that signal urgency/need:
- **Funding / recent raise** (growth → hiring → tooling)
- **Headcount growth** (scaling ops)
- **Tech stack** (accounting systems: NetSuite/Xero/QuickBooks/Sage Intacct/Dynamics)
- **Hiring signals** (job posts mentioning finance systems, ERP, accounting automation)

### 1.3 Account lists
Maintain:
- **Master target accounts** table/list (domain, company size, region, priority)
- **Do-not-contact / suppression** list

## 2) Contact Acquisition Strategy

### 2.1 Primary acquisition tools (recommended)
- **Apollo**: People + Companies search (filters, list building, export)
- **Lusha**: Contact discovery/verification/phones (where allowed)

### 2.2 Secondary tools (optional)
- ZoomInfo / SalesIntel / UpLead / Lead411 (depending on budget)
- Hunter (domain-level email patterns) + verifier

### 2.3 Compliance & safety
- Avoid automating account creation across many vendors using temp emails.
- Avoid scraping gated platforms (LinkedIn) at scale.
- Use exports + API/official workflows where possible.

## 3) Enterprise Workflow (Pipeline)

### Step A — Build account list
Inputs:
- Apollo company search export
- Funding lists (Crunchbase/exported lists)
- Tech stack lists (BuiltWith)

Output:
- `accounts_target.csv` (domain, company, size, region, priority)

### Step B — Acquire contacts per account
For each target account:
- Pull 3–10 contacts matching titles/department.
- Prefer contacts with verified email and direct/mobile phone.

Output:
- `contacts_raw_<source>.csv`

### Step C — Normalize + Dedupe
- Normalize headers
- Normalize domain/LinkedIn URLs
- Clean NaN/NA/blank
- Dedupe match order: email → LinkedIn → name+company

### Step D — Upsert to DB (no overwrite)
- Insert net-new
- Update only missing fields
- If new value arrives for filled field → store in secondary fields
- Update batch_id + last_updated_source + field_sources

### Step E — QA + Metrics
Create run-level reports:
- rows ingested
- net-new contacts added
- rows enriched
- % completeness by field (email, phone, linkedin, title)

### Step F — Syndicate
Push curated exports to:
- WhatsApp (small)
- Drive/Sheets (large)
- Bunny Storage (archive)

## 4) Tools & Knowledge Required

### 4.1 Tools
- OpenClaw browser for manual, compliant workflows
- Python 3.12 + packages:
  - pandas
  - psycopg[binary]
  - pyyaml
- Neon Postgres
- Google Drive/Sheets (optional)

### 4.2 Knowledge assets (reference docs)
- Canonical schema + mapping rules
- Dedupe/update policy
- Segment SQL library
- Destination delivery rules

## 5) Recommended DB Additions (for scale)

### 5.1 Tables
- `syndication_runs` (already in skill)
- (optional) `imports` (file_name, source, row_count, batch_id)
- (optional) `accounts` table (domain-level targeting & scoring)

### 5.2 Indexes
- index on lower(email_primary)
- index on linkedin_person_url
- index on company_domain

## 6) Operating Cadence

Daily:
- ingest new exports
- run QA + small syndication

Weekly:
- new account sourcing + net-new contact acquisition
- enrichment run

Monthly:
- dedupe review + schema improvements
- segment refresh + automation improvements
