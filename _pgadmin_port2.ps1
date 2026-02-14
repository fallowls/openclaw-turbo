$pgpid = (Get-Process pgAdmin4).Id
Get-NetTCPConnection -OwningProcess $pgpid -State Listen | Format-Table -AutoSize
