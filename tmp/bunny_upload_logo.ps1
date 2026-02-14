$zone='mypcown'
$dest='dacreation/logo-white.png'
$file='C:\Users\Administrator\.openclaw\workspace\tmp\dacreation\logo-white.png'
$url="https://storage.bunnycdn.com/$zone/$dest"
$headers=@{ 'AccessKey'='Arpu@254039A' }

$resp = Invoke-WebRequest -Method Put -Uri $url -Headers $headers -InFile $file
Write-Output "status=$($resp.StatusCode)"
