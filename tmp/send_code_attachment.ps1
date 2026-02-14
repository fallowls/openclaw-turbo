$args = @(
  'gmail','send',
  '--account','amit@demonflare.com',
  '--to','aalyavar@gmail.com',
  '--subject','Da Creation - Our Services - HTML Code',
  '--body','Attached is the HTML code for the email template.',
  '--attach','C:\Users\Administrator\.openclaw\workspace\tmp\dacreation-email-expanded-preview-filled-min.html'
)

& gog @args
