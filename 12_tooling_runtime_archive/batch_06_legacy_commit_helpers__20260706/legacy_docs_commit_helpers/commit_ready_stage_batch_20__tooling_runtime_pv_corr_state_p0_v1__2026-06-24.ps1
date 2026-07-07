param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$LegacyRoot = Resolve-Path (Join-Path $PSScriptRoot "..")`nSet-Location $LegacyRoot

$pathFile = "docs/commit_ready_batch_20__tooling_runtime_pv_corr_state_p0_v1__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 20 = TOOLING_RUNTIME pv_corr_state_p0_v1"
Write-Host "Target path count:" $files.Count
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

