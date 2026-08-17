$ErrorActionPreference = "Stop"

$sourceRoot = "D:\Stock\trading_assistant\10_source_library_archive"
$outputDir  = "D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_workbench_design_map__20260811"

$outExact   = Join-Path $outputDir "exact_duplicates__20260811.tsv"
$outNear    = Join-Path $outputDir "near_duplicates_bysize__20260811.tsv"
$outUnique  = Join-Path $outputDir "unique_html_master_list__20260811.tsv"

Write-Host "==> Scanning batch_149* directories for HTML files..."
$batchDirs = Get-ChildItem -Path $sourceRoot -Directory -Filter "batch_149*"
$allFiles  = @()
foreach ($bd in $batchDirs) {
    $htmls = Get-ChildItem -Path $bd.FullName -File -Recurse -Include "*.html","*.htm"
    $allFiles += $htmls
}
$totalCount = $allFiles.Count
Write-Host ("    Total HTML files found: " + $totalCount)
if ($totalCount -eq 0) { Write-Error "No HTML files found, aborting." }

Write-Host "==> Computing Length + SHA256..."
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$records = New-Object System.Collections.Generic.List[object]
$i = 0
foreach ($f in $allFiles) {
    $i++
    if ($i % 500 -eq 0) { Write-Host ("    Processed " + $i + " / " + $totalCount + " ...") }
    $length = $f.Length
    $fs     = [System.IO.File]::OpenRead($f.FullName)
    try {
        $hashBytes = $sha256.ComputeHash($fs)
    } finally {
        $fs.Dispose()
    }
    $hashHex = [BitConverter]::ToString($hashBytes) -replace '-',''
    $records.Add([PSCustomObject]@{
        Path     = $f.FullName
        Name     = $f.Name
        Length   = $length
        SHA256   = $hashHex
        LengthKB = [math]::Round($length / 1KB, 2)
    })
}

Write-Host "==> Building exact_duplicates (group by Length+SHA256)..."
$exactGroups = $records | Group-Object Length, SHA256 | Where-Object { $_.Count -gt 1 } | Sort-Object Count -Descending
$exactLines = New-Object System.Collections.Generic.List[string]
$exactLines.Add("GroupID`tFileCount`tTotalKB`tSHA256`tTop10Paths")
$gid = 0
$totalSavedKB = 0.0
foreach ($g in $exactGroups) {
    $gid++
    $sha   = ($g.Group[0].SHA256)
    $cnt   = $g.Count
    $oneKB = [double]$g.Group[0].LengthKB
    $totKB = [math]::Round($cnt * $oneKB, 2)
    $saved = [math]::Round(($cnt - 1) * $oneKB, 2)
    $totalSavedKB += $saved
    $top10 = ($g.Group | Select-Object -First 10 -ExpandProperty Path) -join '|'
    $exactLines.Add("$gid`t$cnt`t$totKB`t$sha`t$top10")
}
[System.IO.File]::WriteAllLines($outExact, $exactLines, [System.Text.UTF8Encoding]::new($false))
Write-Host ("    exact_dup groups: " + $exactGroups.Count + ", estimated save: " + [math]::Round($totalSavedKB,2) + " KB")

Write-Host "==> Building near_duplicates (same Length, different SHA256)..."
$sizeGroups = $records | Group-Object Length | Where-Object { $_.Count -gt 1 }
$nearGroups = @()
foreach ($sg in $sizeGroups) {
    $distinctHash = ($sg.Group | Select-Object -ExpandProperty SHA256 -Unique).Count
    if ($distinctHash -gt 1) { $nearGroups += $sg }
}
$nearLines = New-Object System.Collections.Generic.List[string]
$nearLines.Add("SizeBytes`tFileCount`tDistinctHashCount`tTop10Paths")
foreach ($g in ($nearGroups | Sort-Object Count -Descending)) {
    $sz    = $g.Name
    $cnt   = $g.Count
    $dhc   = ($g.Group | Select-Object -ExpandProperty SHA256 -Unique).Count
    $top10 = ($g.Group | Select-Object -First 10 -ExpandProperty Path) -join '|'
    $nearLines.Add("$sz`t$cnt`t$dhc`t$top10")
}
[System.IO.File]::WriteAllLines($outNear, $nearLines, [System.Text.UTF8Encoding]::new($false))
Write-Host ("    near_dup groups: " + $nearGroups.Count)

Write-Host "==> Building unique_html_master_list (unique Length+SHA256, min-path rep)..."
$uniqueGroups = $records | Group-Object Length, SHA256
$uniqueLines = New-Object System.Collections.Generic.List[string]
$uniqueLines.Add("RepresentativePath`tSizeKB`tSHA256`tDupCount")
foreach ($g in $uniqueGroups) {
    $rep = ($g.Group | Sort-Object Path | Select-Object -First 1)
    $uniqueLines.Add("$($rep.Path)`t$($rep.LengthKB)`t$($rep.SHA256)`t$($g.Count)")
}
[System.IO.File]::WriteAllLines($outUnique, $uniqueLines, [System.Text.UTF8Encoding]::new($false))
$uniqueCount = $uniqueGroups.Count
$reducePct = if ($totalCount -gt 0) { [math]::Round((1 - $uniqueCount / $totalCount) * 100, 2) } else { 0 }
Write-Host ("    Unique kept after dedup: " + $uniqueCount)

Write-Host ""
Write-Host "==================== SUMMARY ===================="
Write-Host ("  Total files              : " + $totalCount)
Write-Host ("  exact_dup groups         : " + $exactGroups.Count + "   (saves ~ " + [math]::Round($totalSavedKB,2) + " KB)")
Write-Host ("  near_dup groups          : " + $nearGroups.Count)
Write-Host ("  Unique kept after dedup  : " + $uniqueCount + "   (reduction: " + $reducePct + " %)")
Write-Host "================================================="
Write-Host ""
Write-Host "Output files:"
Write-Host ("  " + $outExact)
Write-Host ("  " + $outNear)
Write-Host ("  " + $outUnique)
