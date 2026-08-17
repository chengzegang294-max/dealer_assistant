[CmdletBinding()]
param(
    [switch]$DryRun = $true
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OldRepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$TsvPath = Join-Path $ScriptDir "oldrepo_small_dirs_ruling__20260811.tsv"
$LogTime = Get-Date -Format "yyyyMMdd_HHmmss"
if ($DryRun) { $LogModeTag = "DRYRUN" } else { $LogModeTag = "LIVE" }
$LogPath = Join-Path $ScriptDir ("cleanup_log_{0}_{1}.log" -f $LogModeTag, $LogTime)

$TopDirBuckets = @(
    "00_entry",
    "01_active_objects",
    "02_runtime",
    "03_docs",
    "04_active_main_docs",
    "99_ARCHIVE_SYNCHED_TO_NEW_REPO",
    "临时文件夹"
)

function Write-Log {
    param([string]$Msg, [string]$Level = "INFO")
    $Line = "[{0}] [{1}] {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Level, $Msg
    Add-Content -Path $LogPath -Value $Line -Encoding UTF8
    Write-Host $Line
}

Write-Log "========================================"
if ($DryRun) { $ModeText1 = "DRYRUN (仅日志不删除)" } else { $ModeText1 = "LIVE (真实删除)" }
Write-Log ("旧仓清理脚本启动 - 模式: {0}" -f $ModeText1)
Write-Log ("旧仓根目录: {0}" -f $OldRepoRoot)
Write-Log ("裁决TSV: {0}" -f $TsvPath)
Write-Log ("日志文件: {0}" -f $LogPath)
Write-Log "========================================"

if (-not (Test-Path $TsvPath)) {
    Write-Log ("TSV文件不存在: {0}" -f $TsvPath) "ERROR"
    exit 1
}

$AllRows = Import-Csv $TsvPath -Delimiter "`t"
Write-Log ("TSV加载成功，总行数: {0}" -f $AllRows.Count)

$DeletableRows = $AllRows | Where-Object { $_.裁决 -eq "可删除" }
Write-Log ("裁决=可删除: {0} 份" -f $DeletableRows.Count)

$ProtectRows = $AllRows | Where-Object { $_.裁决 -ne "可删除" }
$PendingRows = $ProtectRows | Where-Object { $_.裁决 -eq "待裁决" }
$ArchiveRows = $ProtectRows | Where-Object { $_.裁决 -eq "可归档" }
Write-Log ("保护名单总计: {0} 份 (待裁决={1}, 可归档={2})" -f $ProtectRows.Count, $PendingRows.Count, $ArchiveRows.Count)

$BucketStats = @{}
foreach ($b in $TopDirBuckets) {
    $BucketStats[$b] = @{ Count = 0; SizeKB = 0.0; DeletedOK = 0; DeletedFail = 0 }
}

$TotalDeletedOK = 0
$TotalDeletedFail = 0
$TotalSkippedProtect = 0

Write-Log ""
Write-Log "========== 开始逐个文件处理 =========="

foreach ($row in $DeletableRows) {
    $TopDir = $row.目录
    $RelPath = $row.相对路径
    $SizeKB = [double]$row.大小KB
    $FullPath = Join-Path $OldRepoRoot $RelPath

    if (-not $BucketStats.ContainsKey($TopDir)) {
        Write-Log ("未知TopDir跳过: {0} -> {1}" -f $TopDir, $RelPath) "WARN"
        continue
    }

    $BucketStats[$TopDir].Count++
    $BucketStats[$TopDir].SizeKB += $SizeKB

    $protectHit = $ProtectRows | Where-Object { $_.相对路径 -eq $RelPath }
    if ($protectHit) {
        $TotalSkippedProtect++
        Write-Log ("[SKIP] 命中保护名单不删除: {0} (裁决={1})" -f $RelPath, $protectHit[0].裁决) "WARN"
        continue
    }

    if ($DryRun) {
        Write-Log ("[DRYRUN] 将删除: {0} ({1:N2} KB, TopDir={2})" -f $RelPath, $SizeKB, $TopDir)
        $BucketStats[$TopDir].DeletedOK++
        $TotalDeletedOK++
    } else {
        if (Test-Path $FullPath -PathType Leaf) {
            try {
                Remove-Item $FullPath -Force -ErrorAction Stop
                Write-Log ("[DELETE OK] 已删除: {0} ({1:N2} KB, TopDir={2})" -f $RelPath, $SizeKB, $TopDir)
                $BucketStats[$TopDir].DeletedOK++
                $TotalDeletedOK++
            } catch {
                $BucketStats[$TopDir].DeletedFail++
                $TotalDeletedFail++
                Write-Log ("[DELETE FAIL] 删除失败: {0} - {1}" -f $RelPath, $_.Exception.Message) "ERROR"
            }
        } else {
            Write-Log ("[MISSING] 文件不存在，跳过: {0}" -f $RelPath) "WARN"
            $BucketStats[$TopDir].DeletedOK++
            $TotalDeletedOK++
        }
    }
}

Write-Log ""
Write-Log "========================================"
Write-Log "              SUMMARY 汇总"
Write-Log "========================================"
if ($DryRun) { $ModeTextSum = "DRYRUN (仅日志不删除)" } else { $ModeTextSum = "LIVE (真实删除)" }
Write-Log ("模式: {0}" -f $ModeTextSum)
Write-Log ""

$GrandCount = 0
$GrandSizeKB = 0.0
$GrandDeletedOK = 0
$GrandDeletedFail = 0

foreach ($b in $TopDirBuckets) {
    $s = $BucketStats[$b]
    $GrandCount += $s.Count
    $GrandSizeKB += $s.SizeKB
    $GrandDeletedOK += $s.DeletedOK
    $GrandDeletedFail += $s.DeletedFail
    Write-Log ("桶[{0}] => 可删除 {1} 份 | {2:N2} KB ({3:N2} MB) | 删除成功={4} | 删除失败={5}" -f `
        $b.PadRight(35), $s.Count.ToString().PadLeft(5), $s.SizeKB, ($s.SizeKB/1024), $s.DeletedOK, $s.DeletedFail)
}

Write-Log "------------------------------------------------------------------------"
Write-Log ("总计可删除      => {0} 份 | {1:N2} KB = {2:N2} MB" -f $GrandCount, $GrandSizeKB, ($GrandSizeKB/1024))
Write-Log ("删除成功        => {0} 份" -f $GrandDeletedOK)
Write-Log ("删除失败        => {0} 份" -f $GrandDeletedFail)
Write-Log ("命中保护名单跳过=> {0} 份" -f $TotalSkippedProtect)
Write-Log ("保护名单总数    => {0} 份 (待裁决 {1} + 可归档 {2})" -f $ProtectRows.Count, $PendingRows.Count, $ArchiveRows.Count)
Write-Log "========================================"

if ($DryRun) {
    Write-Log ""
    Write-Log "[DRYRUN] 本次未真实删除任何文件。"
    Write-Log "[DRYRUN] 若确认无误，请执行:  .\execute_cleanup_oldrepo.ps1 -DryRun:`$false"
}

Write-Log ""
Write-Log "========================================"
Write-Log " 保护名单 (KEEP: 待裁决621份 + 可归档91份 = 712份，绝不删除)"
Write-Log "========================================"

Write-Log ""
Write-Log "--- [子名单A] 待裁决 = 621 份 (需后续人工裁决，禁止删除) ---"
foreach ($r in ($PendingRows | Sort-Object 目录, 相对路径)) {
    Write-Log ("KEEP PENDING  | {0} | {1:N2} KB | {2}" -f $r.目录, [double]$r.大小KB, $r.相对路径)
}

Write-Log ""
Write-Log "--- [子名单B] 可归档 = 91 份 (保留到归档流程，禁止删除) ---"
foreach ($r in ($ArchiveRows | Sort-Object 目录, 相对路径)) {
    Write-Log ("KEEP ARCHIVE  | {0} | {1:N2} KB | {2}" -f $r.目录, [double]$r.大小KB, $r.相对路径)
}

Write-Log ""
Write-Log "========================================"
Write-Log ("脚本完成。日志保存在: {0}" -f $LogPath)
Write-Log "========================================"
