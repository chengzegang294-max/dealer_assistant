param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$LegacyRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $LegacyRoot

$pathFile = "docs/commit_ready_batch_3A__S_BUCKET_core__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 3A = S_BUCKET core truth anchors"
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
