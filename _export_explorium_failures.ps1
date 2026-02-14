$in='C:\Users\Administrator\.openclaw\workspace\merged_apollo_contacts_full_enriched.csv'
$out='C:\Users\Administrator\.openclaw\workspace\explorium_failures.csv'
$fails = Import-Csv $in | Where-Object { $_.explorium_error -and $_.explorium_error.Trim() }
$fails | Export-Csv $out -NoTypeInformation -Encoding UTF8
Write-Host "fail_rows=$($fails.Count)"
Write-Host "wrote=$out"
