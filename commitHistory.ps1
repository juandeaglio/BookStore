$totalInsertions = 0
$totalDeletions = 0

foreach ($index in 0..($totalCount - 1)) {
    $commit = $gitLogOutput[$index]

    if ($index -eq ($totalCount - 1)) {
        continue
    }

    $diffOutput = git diff --shortstat $commit~ $commit

    $columns = ($diffOutput -split ", ")[1..3] -replace "[^\d]+"
    $insertions = [int]$columns[0]
    $deletions = [int]$columns[1]

    $totalInsertions += $insertions
    $totalDeletions += $deletions
}

Write-Host "Total Insertions: $totalInsertions"
Write-Host "Total Deletions: $totalDeletions"