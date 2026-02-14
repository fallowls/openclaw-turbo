$html = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-send-min.html'

gog gmail send --account 'amit@demonflare.com' --to 'aalyavar@gmail.com' --subject 'Da Creation — Services' --body-html $html
