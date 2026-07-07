param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$LegacyRoot = Resolve-Path (Join-Path $PSScriptRoot "..")`nSet-Location $LegacyRoot

$pathFile = "docs/commit_ready_batch_23__tooling_runtime_mt4_probe_instance_config_text_recovered_batch1__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 23 = TOOLING_RUNTIME mt4_probe_instance config text recovered batch1"
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

