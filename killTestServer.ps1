$processes = (Get-WmiObject Win32_Process -Filter "name = '$process'" | Select-Object CommandLine, Handle | findStr "runserver")
foreach ($line in $processes){
    Write-Host $line.Trim().Split()[-1]
}
foreach ($line in $processes){
    Stop-Process -Id ($line.Trim().Split()[-1])
}
$processes = (Get-WmiObject Win32_Process -Filter "name = '$process'" | Select-Object CommandLine, Handle | findStr "runserver")
foreach ($line in $processes){
    Write-Host $line.Trim().Split()[-1]
}
