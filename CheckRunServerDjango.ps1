$runServerCount = (Get-CimInstance Win32_Process |
                   Where-Object { $_.CommandLine -like '*runserver*' }).Count

exit $runServerCount