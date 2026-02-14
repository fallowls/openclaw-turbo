$py = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
$norm = "C:\Users\Administrator\.openclaw\workspace\_normalize_to_staging_apollo.py"
$pipe = "C:\Users\Administrator\.openclaw\workspace\skills\lead-gen-db\scripts\run_pipeline.py"

$base = "C:\Users\Administrator\.openclaw\workspace\inbound_zip_229862bd\new data"
$outdir = "C:\Users\Administrator\.openclaw\workspace\inbound_zip_229862bd\normalized"
New-Item -ItemType Directory -Force -Path $outdir | Out-Null

$env:NEON_DSN = 'postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Pick only Apollo-style raw contact CSVs (header starts with "First Name,Last Name") and skip the huge accounts export.
$files = Get-ChildItem -Path $base -Filter '*.csv' | Where-Object {
  $_.Name -notlike 'apollo-accounts-export*'
} | ForEach-Object {
  $first = Get-Content -LiteralPath $_.FullName -TotalCount 1
  if ($first -like 'First Name,Last Name*') { $_.FullName }
}

if (-not $files -or $files.Count -eq 0) {
  throw "No Apollo-style contact CSVs found to import in $base"
}

foreach ($in in $files) {
  $name = Split-Path -Leaf $in
  $safe = [regex]::Replace($name, '[^a-zA-Z0-9]+', '_')
  $out = Join-Path $outdir ("$safe.normalized.csv")
  $batch = ("zip229862bd_" + $safe.ToLower())

  Write-Output "Normalizing: $name"
  & $py $norm $in $out $batch
  if ($LASTEXITCODE -ne 0) { throw "Normalize failed for $name" }

  Write-Output "Pipeline: $name"
  & $py $pipe apollo $out $batch
  if ($LASTEXITCODE -ne 0) { throw "Pipeline failed for $name" }
}

Write-Output "All files processed: $($files.Count)"
