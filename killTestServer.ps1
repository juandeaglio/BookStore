$process = "Python.exe"
$processes = (Get-WmiObject Win32_Process -Filter "name = '$process'" -erroraction 'silentlycontinue' | Select-Object CommandLine, Handle  | findStr "runserver")
foreach ($line in $processes){
    Write-Host $line.Trim().Split()[-1] -erroraction 'silentlycontinue'
}
foreach ($line in $processes){
    Stop-Process -Id ($line.Trim().Split()[-1]) -erroraction 'silentlycontinue'
}
$processes = (Get-WmiObject Win32_Process -Filter "name = '$process'" -erroraction 'silentlycontinue' | Select-Object CommandLine, Handle | findStr "runserver")
foreach ($line in $processes){
    Write-Host $line.Trim().Split()[-1] -erroraction 'silentlycontinue'
}
