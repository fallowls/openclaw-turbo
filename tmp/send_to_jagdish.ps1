$path = 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview-filled-min.html'
$html = (Get-Content -Raw $path) -replace "`r?`n", ''
$html = $html -replace '"', "'"

gog gmail send --account 'amit@demonflare.com' --to 'jagdish@dacreation.in' --subject 'Da Creation - Our Services' --body-html $html
