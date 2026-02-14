$ErrorActionPreference = 'Stop'

$u = Get-LocalUser -Name 'Administrator'
$u | Select-Object Name,Enabled,LockedOut | Format-List

if ($u.LockedOut) {
  Unlock-LocalUser -Name 'Administrator'
  Write-Output 'UNLOCKED'
} else {
  Write-Output 'NOT_LOCKED'
}
