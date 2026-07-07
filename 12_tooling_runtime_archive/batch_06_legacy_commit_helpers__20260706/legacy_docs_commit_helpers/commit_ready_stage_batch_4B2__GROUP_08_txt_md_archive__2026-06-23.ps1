param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$LegacyRoot = Resolve-Path (Join-Path $PSScriptRoot "..")`nSet-Location $LegacyRoot

$pathFile = "docs/commit_ready_batch_4B2__GROUP_08_txt_md_archive__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 4B2 = GROUP_08 txt md archive"
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

