$b64 = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation\logo-white.b64.txt'
$html = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview.html'
$html = $html -replace 'https://dacreation.in/images/logo-white.png', ('data:image/png;base64,' + $b64)
# header color tweak (tell me if you want maroon/gold/dark)
$html = $html -replace 'background:#0b1220', 'background:#1b0d12'
Set-Content -Path 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-corporate-email-preview-embedded2.html' -Value $html
