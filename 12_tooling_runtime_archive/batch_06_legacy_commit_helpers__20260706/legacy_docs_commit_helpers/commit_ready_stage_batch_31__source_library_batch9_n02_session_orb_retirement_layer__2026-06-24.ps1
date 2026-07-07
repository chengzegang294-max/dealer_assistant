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

$pathFile = "docs/commit_ready_batch_31__source_library_batch9_n02_session_orb_retirement_layer__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

Write-Host "Batch 31 = SOURCE_LIBRARY Batch9 N02 session/orb retirement layer"
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
