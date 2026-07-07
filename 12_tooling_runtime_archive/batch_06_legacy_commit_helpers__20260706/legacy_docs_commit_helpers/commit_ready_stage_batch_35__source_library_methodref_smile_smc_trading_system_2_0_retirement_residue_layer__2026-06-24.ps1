param([switch]$DryRun)

$ErrorActionPreference = "Stop"
$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
} else {
    $repoRoot = $repoRoot.Trim()
}
Set-Location $repoRoot

$pathFile = "docs/commit_ready_batch_35__source_library_methodref_smile_smc_trading_system_2_0_retirement_residue_layer__paths.txt"
$files = Get-Content -Path $pathFile -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }
$docFiles = $files | Where-Object { $_ -like "docs/*" }
$firstDeletion = $files | Where-Object { $_ -notlike "docs/*" } | Select-Object -First 1
$targetRoot = Split-Path -Path $firstDeletion -Parent

git status --short -- $targetRoot
git status --short -- $docFiles

if ($DryRun) {
    git add -u --dry-run -- $targetRoot
    git add --dry-run -- $docFiles
    return
}

git add -u -- $targetRoot
git add -- $docFiles
git status --short -- $targetRoot
git status --short -- $docFiles
