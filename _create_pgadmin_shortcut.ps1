$target = 'C:\Program Files\pgAdmin 4\bin\pgAdmin4.exe'
if (!(Test-Path $target)) { $target = 'C:\Program Files\pgAdmin 4\runtime\pgAdmin4.exe' }
$shortcut = 'C:\Users\Public\Desktop\pgAdmin 4.url'
$content = @"
[InternetShortcut]
URL=file:///$($target -replace '\\','/')
IconFile=$target
IconIndex=0
"@
$content | Set-Content -Path $shortcut -Encoding ASCII
Start-Process -FilePath $target
