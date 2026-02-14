$paths = @(
  "$env:APPDATA\pgAdmin\config_local.py",
  "$env:APPDATA\pgAdmin\pgadmin4.log"
)
foreach($p in $paths){
  if(Test-Path $p){
    Write-Host "--- $p ---"
    Get-Content $p | Select-String -Pattern 'PORT|SERVER' -CaseSensitive
  }
}
