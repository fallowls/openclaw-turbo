$zip = 'C:\Users\Administrator\.openclaw\media\inbound\6f4c8265-d3b5-4b03-b2cd-143c7089c61a.zip'
$out = 'C:\Users\Administrator\.openclaw\workspace\inbound_zip_6f4c8265'
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Path $out | Out-Null
Expand-Archive -Path $zip -DestinationPath $out -Force
Get-ChildItem -Recurse -File $out | Select-Object FullName,Length | Format-Table -AutoSize
