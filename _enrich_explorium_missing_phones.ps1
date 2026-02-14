param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$Out,
  [string]$Failures = (Join-Path (Split-Path $Out) ((Split-Path $Out -Leaf) -replace '\.csv$','_failures.csv'))
)

$ErrorActionPreference = 'Stop'

$rows = Import-Csv -Path $In
$fail = @()

function IsBlank($s) {
  return ($null -eq $s) -or ([string]$s).Trim().Length -eq 0
}

function GetPhoneArray($ci) {
  if ($null -eq $ci) { return @() }
  if ($ci.phone_numbers -is [System.Collections.IEnumerable] -and -not ($ci.phone_numbers -is [string])) {
    return @($ci.phone_numbers)
  }
  return @()
}

$processed = 0
$called = 0
$filledMobile = 0
$filledWork = 0
$filledHome = 0
$filledOther = 0
$skippedHasPhones = 0
$skippedNoLinkedIn = 0
$skippedSalesLead = 0

foreach ($r in $rows) {
  $processed++

  # Skip if the contact already has ANY direct phone info.
  $hasAny = (-not (IsBlank $r.'Mobile Phone')) -or (-not (IsBlank $r.'Work Direct Phone')) -or (-not (IsBlank $r.'Home Phone')) -or (-not (IsBlank $r.'Other Phone')) -or (-not (IsBlank $r.'Corporate Phone'))
  if ($hasAny) {
    $skippedHasPhones++
    continue
  }

  $linkedin = $r.'Person Linkedin Url'
  if (IsBlank $linkedin) {
    $skippedNoLinkedIn++
    continue
  }

  if ($linkedin -match '/sales/lead/') {
    # Sales Navigator lead URLs often fail match; skip instead of wasting credits.
    $skippedSalesLead++
    $fail += [pscustomobject]@{ first_name=$r.'First Name'; last_name=$r.'Last Name'; company=$r.'Company Name'; linkedin=$linkedin; reason='skipped_sales_lead_url' }
    continue
  }

  try {
    $called++
    Push-Location "C:\Users\Administrator\.openclaw\workspace\skills\explorium-prospects-match"
    try {
      $json = & node .\scripts\contact_details_from_linkedin.mjs --linkedin "$linkedin" 2>&1 | Out-String
    } finally {
      Pop-Location
    }

    $obj = $json | ConvertFrom-Json

    $ci = $obj.contacts_information

    # Fill blanks only. Do NOT populate Corporate Phone from these numbers.
    if (IsBlank $r.'Mobile Phone' -and -not (IsBlank $ci.mobile_phone)) {
      $r.'Mobile Phone' = $ci.mobile_phone
      $filledMobile++
    }

    $phones = GetPhoneArray $ci
    foreach ($p in $phones) {
      if ($null -eq $p) { continue }
      $num = $p.number
      $type = ($p.type | ForEach-Object { $_.ToString().ToLowerInvariant() })
      if (IsBlank $num) { continue }

      if ((IsBlank $r.'Work Direct Phone') -and ($type -match 'work|office|professional')) {
        $r.'Work Direct Phone' = $num
        $filledWork++
        continue
      }
      if ((IsBlank $r.'Home Phone') -and ($type -match 'home')) {
        $r.'Home Phone' = $num
        $filledHome++
        continue
      }
      if ((IsBlank $r.'Other Phone') -and ($type -match 'other|unknown')) {
        $r.'Other Phone' = $num
        $filledOther++
        continue
      }

      # If type is missing/ambiguous, place into Other Phone as last resort (but only if empty)
      if (IsBlank $type -and (IsBlank $r.'Other Phone')) {
        $r.'Other Phone' = $num
        $filledOther++
        continue
      }
    }

  } catch {
    $fail += [pscustomobject]@{ first_name=$r.'First Name'; last_name=$r.'Last Name'; company=$r.'Company Name'; linkedin=$linkedin; reason=($_.Exception.Message) }
  }
}

$rows | Export-Csv -Path $Out -NoTypeInformation
$fail | Export-Csv -Path $Failures -NoTypeInformation

[pscustomobject]@{
  processed=$processed
  explorium_called=$called
  filled_mobile=$filledMobile
  filled_work=$filledWork
  filled_home=$filledHome
  filled_other=$filledOther
  skipped_already_complete=$skippedHasPhones
  skipped_no_linkedin=$skippedNoLinkedIn
  skipped_sales_lead=$skippedSalesLead
  failures=$fail.Count
  out=$Out
  failures_out=$Failures
} | ConvertTo-Json -Depth 4
