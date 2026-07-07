param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
} else {
    $repoRoot = $repoRoot.Trim()
}
Set-Location $repoRoot

$pathFile = "docs/commit_ready_batch_34__source_library_batch9_n03_market_structure_breakout_quality_conditions_retirement_layer__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }

git status --short -- $files

if ($DryRun) {
    git add --dry-run -- $files
    return
}

git add -- $files
git status --short -- $files
