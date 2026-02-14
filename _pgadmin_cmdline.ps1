Get-CimInstance Win32_Process -Filter "Name='pgAdmin4.exe'" | Select-Object CommandLine,ProcessId
