$ErrorActionPreference = 'Stop'

$skillDir = 'C:\Users\Administrator\.openclaw\workspace\skills\explorium-prospects-match'
$nodeScript = 'scripts\contact_details_from_linkedin.mjs'

$inputCsv  = 'C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts_neon_enriched.csv'
$outputCsv = 'C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts_full_enriched.csv'

# Load rows (already Neon-enriched)
$rows = Import-Csv -Path $inputCsv

# Ensure audit columns exist
$auditCols = @('explorium_prospect_id','explorium_used_api_key','explorium_error')
foreach ($c in $auditCols) {
  foreach ($r in $rows) {
    if (-not ($r.PSObject.Properties.Name -contains $c)) {
      Add-Member -InputObject $r -NotePropertyName $c -NotePropertyValue ''
    }
  }
}

function Normalize-LinkedIn([string]$u) {
  if (-not $u) { return '' }
  $u = $u.Trim()
  if ($u.EndsWith('/')) { $u = $u.Substring(0, $u.Length-1) }
  return $u
}

function Pick-FirstPhone($phones, [string[]]$typeHints) {
  if (-not $phones) { return '' }

  # phones might be:
  # - array of objects { phone_number, type }
  # - array of strings
  foreach ($hint in $typeHints) {
    foreach ($p in $phones) {
      if ($p -is [string]) { continue }
      $t = ('' + $p.type).ToLowerInvariant()
      if ($t -like "*$hint*") {
        $n = ('' + $p.phone_number).Trim()
        if ($n) { return $n }
      }
    }
  }

  # fallback: first phone_number
  foreach ($p in $phones) {
    if ($p -is [string]) {
      $n = $p.Trim(); if ($n) { return $n }
    } else {
      $n = ('' + $p.phone_number).Trim(); if ($n) { return $n }
    }
  }

  return ''
}

function Extract-Phones($payload) {
  # Try common shapes
  $phones = $null
  if ($payload.phones) { $phones = $payload.phones }
  elseif ($payload.contact_details -and $payload.contact_details.phones) { $phones = $payload.contact_details.phones }
  elseif ($payload.contacts_information -and $payload.contacts_information.phones) { $phones = $payload.contacts_information.phones }
  return $phones
}

# Build list of candidates needing Explorium: no phones + has LinkedIn
$candidates = @()
for ($i=0; $i -lt $rows.Count; $i++) {
  $r = $rows[$i]
  $li = Normalize-LinkedIn $r.'Person Linkedin Url'
  if (-not $li) { continue }

  $hasAnyPhone = @($r.'Mobile Phone', $r.'Work Direct Phone', $r.'Corporate Phone', $r.'Other Phone') | ForEach-Object { ('' + $_).Trim() } | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count
  if ($hasAnyPhone -gt 0) { continue }

  $candidates += [pscustomobject]@{ index=$i; linkedin=$li }
}

Write-Host "Total rows: $($rows.Count). Candidates for Explorium: $($candidates.Count)"

$processed = 0
$success = 0
$failed = 0

foreach ($c in $candidates) {
  $processed++
  $i = [int]$c.index
  $li = $c.linkedin

  Write-Host "[$processed/$($candidates.Count)] Explorium enrich: $li"

  try {
    $stdout = & node $nodeScript --linkedin $li 2>&1
    $json = $stdout | Out-String | ConvertFrom-Json

    $apiKey = ('' + $json.api_key).Trim()
    $prospectId = ('' + $json.prospect_id).Trim()

    $phones = Extract-Phones $json
    if (-not $phones) {
      # sometimes nested under contacts_information
      if ($json.contacts_information) { $phones = Extract-Phones $json.contacts_information }
    }

    $mobile = Pick-FirstPhone $phones @('mobile','cell')
    $work   = Pick-FirstPhone $phones @('work','direct','office')
    $corp   = Pick-FirstPhone $phones @('corporate','hq','company','main')
    $other  = Pick-FirstPhone $phones @('other')

    # Fill only if blank
    if (-not (('' + $rows[$i].'Mobile Phone').Trim()) -and $mobile) { $rows[$i].'Mobile Phone' = $mobile }
    if (-not (('' + $rows[$i].'Work Direct Phone').Trim()) -and $work) { $rows[$i].'Work Direct Phone' = $work }
    if (-not (('' + $rows[$i].'Corporate Phone').Trim()) -and $corp) { $rows[$i].'Corporate Phone' = $corp }
    if (-not (('' + $rows[$i].'Other Phone').Trim()) -and $other) { $rows[$i].'Other Phone' = $other }

    $rows[$i].explorium_used_api_key = $apiKey
    $rows[$i].explorium_prospect_id = $prospectId
    $rows[$i].explorium_error = ''

    $success++
  } catch {
    $rows[$i].explorium_error = ('' + $_.Exception.Message)
    $failed++
    Write-Warning "Failed: $li :: $($_.Exception.Message)"
    # IMPORTANT: no retries (per policy)
  }
}

# Preserve original column order as much as possible, append audit cols if needed
$header = (Get-Content -Path $inputCsv -TotalCount 1)
$cols = $header -split ','
# add any missing audit cols
foreach ($c in $auditCols) { if ($cols -notcontains $c) { $cols += $c } }

$rows | Select-Object -Property $cols | Export-Csv -Path $outputCsv -NoTypeInformation -Encoding UTF8

Write-Host "Done. processed=$processed success=$success failed=$failed"
Write-Host "Wrote: $outputCsv"