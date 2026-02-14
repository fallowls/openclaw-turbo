$py = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
$norm = "C:\Users\Administrator\.openclaw\workspace\_normalize_to_staging_apollo.py"
$pipe = "C:\Users\Administrator\.openclaw\workspace\skills\lead-gen-db\scripts\run_pipeline.py"
$base = "C:\Users\Administrator\.openclaw\workspace\inbound_zip_6f4c8265"
$raw = Join-Path $base "raw"
$outdir = Join-Path $base "normalized"
New-Item -ItemType Directory -Force -Path $outdir | Out-Null

$env:NEON_DSN = 'postgresql://neondb_owner:npg_FZk6rC7vpchU@ep-muddy-bonus-aia9yp44-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

$files = @(
  'apollo-contacts-export (2).csv',
  'apollo-contacts-export (3).csv',
  'apollo-contacts-export (4).csv',
  'apollo-contacts-export (5).csv',
  'Mexico.csv'
)

foreach ($f in $files) {
  $in = Join-Path $raw $f
  $safe = [regex]::Replace($f, '[^a-zA-Z0-9]+', '_')
  $out = Join-Path $outdir ("$safe.normalized.csv")
  $batch = ("zip6f4c8265_" + $safe.ToLower())

  Write-Output "Normalizing: $in"
  & $py $norm $in $out $batch
  if ($LASTEXITCODE -ne 0) { throw "Normalize failed for $f" }

  Write-Output "Pipeline: $out"
  & $py $pipe apollo $out $batch
  if ($LASTEXITCODE -ne 0) { throw "Pipeline failed for $f" }
}

Write-Output "All files processed."
