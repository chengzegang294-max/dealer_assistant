param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$LegacyRoot = Resolve-Path (Join-Path $PSScriptRoot "..")`nSet-Location $LegacyRoot

$pathFile = "docs/commit_ready_batch_13__group_03_entry_layer__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 13 = GROUP_03 entry layer"
Write-Host "Target file count:" $files.Count
Write-Host "Path file:" $pathFile

git status --short -- $files

if ($DryRun) {
    Write-Host "Running git add --dry-run ..."
    git add --dry-run -- $files
    return
}

Write-Host "Running git add ..."
git add -- $files
git status --short -- $files

