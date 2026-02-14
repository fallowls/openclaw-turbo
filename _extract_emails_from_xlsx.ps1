param(
  [Parameter(Mandatory=$true)][string]$In,
  [string]$Out = "emails_extracted.csv"
)

$ErrorActionPreference = 'Stop'

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

try {
  $wb = $excel.Workbooks.Open($In)
  $ws = $wb.Worksheets.Item(1)
  $used = $ws.UsedRange

  $rowCount = $used.Rows.Count
  $colCount = $used.Columns.Count

  # find email column by header row (row 1)
  $emailCol = $null
  for ($c = 1; $c -le $colCount; $c++) {
    $h = $ws.Cells.Item(1, $c).Text
    if ($h -and ($h.ToString().ToLowerInvariant() -match 'email')) {
      $emailCol = $c
      break
    }
  }

  if (-not $emailCol) { throw "Could not find an email column in first sheet header row" }

  $outRows = @()
  $outRows += 'email'

  for ($r = 2; $r -le $rowCount; $r++) {
    $v = $ws.Cells.Item($r, $emailCol).Text
    if ($v) {
      $e = $v.ToString().Trim().ToLowerInvariant()
      if ($e) { $outRows += $e }
    }
  }

  Set-Content -Path $Out -Value $outRows -Encoding UTF8
  Write-Output ("{0} rows, emailCol={1}, out={2}" -f ($rowCount-1), $emailCol, $Out)
}
finally {
  if ($wb) { $wb.Close($false) | Out-Null }
  $excel.Quit() | Out-Null
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}
