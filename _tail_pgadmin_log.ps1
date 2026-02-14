$p = $env:APPDATA + '\pgAdmin\pgadmin4.log'
Get-Content -Path $p -Tail 100
