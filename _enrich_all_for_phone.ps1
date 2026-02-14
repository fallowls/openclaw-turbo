$in = "C:\Users\Administrator\.openclaw\media\inbound\667e91a3-96b0-4eb4-8e8b-0284d03b6737.csv"
$out = "C:\Users\Administrator\.openclaw\workspace\enriched_phones_667e91a3.csv"

$rows = Import-Csv $in

Push-Location "C:\Users\Administrator\.openclaw\workspace\skills\explorium-prospects-match"

$i = 0
foreach ($r in $rows) {
  $i++
  $li = $r.'Person Linkedin Url'
  if (-not $li -or $li.Trim() -eq "") { continue }

  try {
    $jsonText = node "scripts\contact_details_from_linkedin.mjs" --linkedin $li
    $j = $jsonText | ConvertFrom-Json

    # Write back phone info (keep existing values if API returns null)
    $mobile = $j.contacts_information.mobile_phone
    if ($mobile) { $r.'neon_phone_mobile' = $mobile }

    $phones = $j.contacts_information.phone_numbers
    if ($phones -and $phones.Count -gt 0) {
      $r.'neon_phone_work' = $phones[0].phone_number
      if ($phones.Count -gt 1) { $r.'neon_phone_other' = $phones[1].phone_number }
    }

    # Add audit columns
    if (-not ($r.PSObject.Properties.Name -contains 'explorium_prospect_id')) {
      $r | Add-Member -NotePropertyName 'explorium_prospect_id' -NotePropertyValue ''
      $r | Add-Member -NotePropertyName 'explorium_used_api_key' -NotePropertyValue ''
      $r | Add-Member -NotePropertyName 'explorium_correlation_id' -NotePropertyValue ''
    }

    $r.explorium_prospect_id = $j.prospect_id
    $r.explorium_used_api_key = $j.api_key
    $r.explorium_correlation_id = $j.contacts_information.correlation_id
  }
  catch {
    # Keep going; record error in audit col
    if (-not ($r.PSObject.Properties.Name -contains 'explorium_error')) {
      $r | Add-Member -NotePropertyName 'explorium_error' -NotePropertyValue ''
    }
    $r.explorium_error = $_.Exception.Message
  }

  if (($i % 10) -eq 0) {
    Write-Host "Processed $i / $($rows.Count)" 
  }
}

$rows | Export-Csv $out -NoTypeInformation
Pop-Location
Write-Host "Wrote: $out"
