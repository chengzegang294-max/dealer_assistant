param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
} else {
    $repoRoot = $repoRoot.Trim()
}
Set-Location $repoRoot

$pathFile = "docs/commit_ready_batch_32__source_library_batch9_sources_kimi_retirement_layer__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 32 = SOURCE_LIBRARY Batch9 batch9_sources_kimi retirement layer"
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
