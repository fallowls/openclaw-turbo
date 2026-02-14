$html = Get-Content -Raw 'C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview-filled-min.html'

$argList = @(
  'gmail','send',
  '--account','amit@demonflare.com',
  '--to','aalyavar@gmail.com',
  '--subject','Da Creation - Our Services',
  '--body-html', $html
)

$p = Start-Process -FilePath 'gog' -ArgumentList $argList -NoNewWindow -Wait -PassThru
if($p.ExitCode -ne 0){ exit $p.ExitCode }
