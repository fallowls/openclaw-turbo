$b64 = (Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation\logo-white-180.b64.txt').Trim()
$html = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview.html'
$html = $html -replace '\{\{LOGO_B64\}\}', $b64
Set-Content -Path 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview-filled.html' -Value $html
