param(
    [string]$TsvPath = "",
    [string]$BaseDir = "",
    [switch]$DryRun = $true
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($TsvPath)) {
    $TsvPath = Join-Path $PSScriptRoot "MOVE_to_old_90.tsv"
}
if ([string]::IsNullOrWhiteSpace($BaseDir)) {
    $BaseDir = Join-Path $PSScriptRoot "moved_from_00_entry"
}

if (-not (Test-Path -LiteralPath $TsvPath)) {
    Write-Error "TSV not found: $TsvPath`n(Hint: 脚本默认从 PSScriptRoot 找 MOVE_to_old_90.tsv，当前 PSScriptRoot=$PSScriptRoot)"
    exit 1
}

$lines = Get-Content $TsvPath -Encoding UTF8
if ($lines.Count -lt 2) {
    Write-Warning "No data rows in TSV"
    exit 0
}

$rows = $lines[1..($lines.Count - 1)] | ForEach-Object {
    $parts = $_ -split "`t"
    if ($parts.Count -ge 2) {
        [pscustomobject]@{
            Src = $parts[0].Trim()
            Dst = $parts[1].Trim()
            Reason = if ($parts.Count -ge 3) { $parts[2].Trim() } else { "" }
        }
    }
}

$total = $rows.Count
$done = 0
$skipped = 0
$moved = 0

foreach ($r in $rows) {
    $done++
    if (-not (Test-Path $r.Src)) {
        Write-Warning "[$done/$total] SKIP missing: $($r.Src)"
        $skipped++
        continue
    }

    $dstDir = Split-Path $r.Dst -Parent
    if (-not (Test-Path $dstDir)) {
        if ($DryRun) {
            Write-Host "[DRY-RUN] [MKDIR] $dstDir"
        } else {
            New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        }
    }

    if (Test-Path $r.Dst) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($r.Dst)
        $ext = [System.IO.Path]::GetExtension($r.Dst)
        $parent = Split-Path $r.Dst -Parent
        $i = 1
        do {
            $newDst = Join-Path $parent ("{0}__dup{1}{2}" -f $base, $i, $ext)
            $i++
        } while (Test-Path $newDst)
        Write-Warning "[$done/$total] DST exists, rename: $($r.Dst) -> $newDst"
        $r.Dst = $newDst
    }

    if ($DryRun) {
        Write-Host "[DRY-RUN] [MOVE]  $($r.Src)  ->  $($r.Dst)"
    } else {
        Move-Item -Path $r.Src -Destination $r.Dst -Force
        Write-Host "[MOVE OK] [$done/$total] $($r.Src)  ->  $($r.Dst)"
    }
    $moved++
}

Write-Host ""
Write-Host "=== SUMMARY ==="
Write-Host "Total rows   : $total"
Write-Host "Moved (plan) : $moved"
Write-Host "Skipped      : $skipped"
if ($DryRun) {
    Write-Host "Mode         : DRY-RUN (no file changed). Re-run with -DryRun:`$false to execute."
} else {
    Write-Host "Mode         : EXECUTED"
}
