$path = 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview-filled-min.html'
$html = (Get-Content -Raw $path) -replace "`r?`n", ''
# make it safe to wrap in double-quotes by removing internal double quotes
$html = $html -replace '"', "'"

& gog gmail send --account 'amit@demonflare.com' --to 'aalyavar@gmail.com' --subject 'Da Creation - Our Services' --body-html "$html"
