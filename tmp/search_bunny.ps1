$patterns = @('storage.bunnycdn.com','AccessKey','b-cdn.net','BUNNY','bunny')
$root = 'C:\Users\Administrator\.openclaw\workspace'
$exclude = @('node_modules','dist','.git','.openclaw','media')

$files = Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object {
    $p = $_.FullName
    foreach($e in $exclude){ if($p -match ('\\' + [regex]::Escape($e) + '\\')){ return $false } }
    return $true
  }

$hits = @()
foreach($pat in $patterns){
  $m = $files | Select-String -SimpleMatch -Pattern $pat -List -ErrorAction SilentlyContinue
  if($m){ $hits += $m }
}
$hits | Select-Object -ExpandProperty Path -Unique | Select-Object -First 50
