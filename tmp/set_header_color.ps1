$in = 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview-embedded2.html'
$out = 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview-embedded3.html'
$html = Get-Content -Raw $in
$html = $html -replace 'background:#1b0d12', 'background:#601A29'
Set-Content -Path $out -Value $html
