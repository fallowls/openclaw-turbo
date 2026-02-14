$b64 = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-logo.b64.txt'
$html = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview.html'
$html = $html -replace 'https://dacreation.in/images/logo-white.png', ('data:image/png;base64,' + $b64)
$html = $html -replace 'background:#0b1220', 'background:#601A29'
Set-Content -Path 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview-embedded.html' -Value $html
