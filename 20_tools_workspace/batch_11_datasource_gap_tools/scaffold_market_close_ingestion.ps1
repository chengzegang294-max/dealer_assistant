# scaffold_market_close_ingestion.ps1
# PowerShell 5 Compatible

param(
    [switch]$DryRun = $true,
    [string]$Date = (Get-Date).ToString("yyyyMMdd"),
    [string]$QuickTinyBinPath = "D:\Stock\quicktiny-stock-ladder-desktop.exe"
)

$ErrorActionPreference = "Stop"

$ScriptDir = [System.IO.Path]::GetDirectoryName($MyInvocation.MyCommand.Path)
$BatchRoot = $ScriptDir
$OutRoot = Join-Path $BatchRoot "out_market_close_dryrun"

$CH_DASH = [char]45
$CH_SPC  = [char]32
$CH_SQ   = [char]39
$CH_AMP  = [char]38
$CH_SLASH = [char]47
$CH_BT   = [char]96
$DD = $CH_DASH + $CH_DASH
$CRLF = [char]13 + [char]10
$MD_CODE_FENCE = $CH_BT + $CH_BT + $CH_BT

$ROOM_NAMES = @(
    "复盘哥",
    "独家老师5号",
    "独家短线老师6号",
    "机构电话会议纪要+小作文+情报",
    "梅森",
    "顺势而为",
    "混江龙",
    "天赢居",
    "先知",
    "天机",
    "游资胖大叔",
    "潜伏王者",
    "k神",
    "周期女王",
    "格兰投研",
    "擒龙小师姐",
    "独家竞价低吸",
    "小锦鲤",
    "核心逻辑社",
    "梦幻一步",
    "新生代",
    "龙头交易猿",
    "机构研报资讯精选",
    "小作文嗅嗅+机构研报"
)

function Write-Utf8BomFile {
    param(
        [string]$FilePath,
        [string]$FileContent
    )
    $encUtf8Bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllText($FilePath, $FileContent, $encUtf8Bom)
}

function CreateEmptyFile {
    param([string]$FilePath)
    $parentDir = [System.IO.Path]::GetDirectoryName($FilePath)
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    $fileStream = [System.IO.File]::Create($FilePath)
    $fileStream.Close()
}

function NewChecklistRow {
    param(
        [string]$s,
        [string]$a,
        [string]$p,
        [string]$st,
        [string]$dn
    )
    $obj = New-Object PSObject
    $obj | Add-Member NoteProperty Step $s
    $obj | Add-Member NoteProperty Action $a
    $obj | Add-Member NoteProperty Path $p
    $obj | Add-Member NoteProperty Status $st
    $obj | Add-Member NoteProperty DryRunNote $dn
    return $obj
}

function ConcatArgs {
    param(
        [string]$binPath,
        [string]$dateVal,
        [string]$outDir
    )
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append($CH_AMP)
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($CH_SQ)
    [void]$sb.Append($binPath)
    [void]$sb.Append($CH_SQ)
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($DD)
    [void]$sb.Append("mode")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append("capture")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($DD)
    [void]$sb.Append("date")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($dateVal)
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($DD)
    [void]$sb.Append("outdir")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($CH_SQ)
    [void]$sb.Append($outDir)
    [void]$sb.Append($CH_SQ)
    return $sb.ToString()
}

function ConcatParamsOnly {
    param(
        [string]$dateVal,
        [string]$outDir
    )
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append($DD)
    [void]$sb.Append("mode")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append("capture")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($DD)
    [void]$sb.Append("date")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($dateVal)
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($DD)
    [void]$sb.Append("outdir")
    [void]$sb.Append($CH_SPC)
    [void]$sb.Append($outDir)
    return $sb.ToString()
}

$checklistRows = New-Object System.Collections.ArrayList

$SEPARATOR = "============================================================"
$SEP_THIN  = "------------------------------------------------------------"

Write-Host $SEPARATOR -ForegroundColor Cyan
$headerLine = "  scaffold_market_close_ingestion.ps1  |  DryRun = {0}  |  Date = {1}" -f $DryRun, $Date
Write-Host $headerLine -ForegroundColor Cyan
Write-Host $SEPARATOR -ForegroundColor Cyan
Write-Host ""

# ============================================================
# STEP 1
# ============================================================
Write-Host "[Step 1/3] QuickTiny Capture" -ForegroundColor Yellow
Write-Host $SEP_THIN -ForegroundColor Gray

$Step1_DirName = "quicktiny_" + $Date
$Step1_Dir = Join-Path $OutRoot $Step1_DirName
$Step1_LadderFile = Join-Path $Step1_Dir ("LADDER_SNAPSHOT_PLACEHOLDER_" + $Date + ".txt")
$Step1_SectorFile = Join-Path $Step1_Dir ("SECTOR_SNAPSHOT_PLACEHOLDER_" + $Date + ".txt")

if ($DryRun) {
    if (-not (Test-Path $Step1_Dir)) {
        New-Item -ItemType Directory -Path $Step1_Dir -Force | Out-Null
    }

    $qtExists = Test-Path $QuickTinyBinPath
    if (-not $qtExists) {
        $warnLine = "  [WARN] QuickTiny binary not found: {0} (hint only, will NOT launch)" -f $QuickTinyBinPath
        Write-Host $warnLine -ForegroundColor Magenta
    }

    $infoLine1 = "  [INFO] Will execute: {0}" -f $QuickTinyBinPath
    Write-Host $infoLine1 -ForegroundColor Green

    $argLineOnly = ConcatParamsOnly -dateVal $Date -outDir $Step1_Dir
    $infoLine2 = "         Params = {0}" -f $argLineOnly
    Write-Host $infoLine2 -ForegroundColor Green
    Write-Host "  [INFO] (DryRun: NO exe launched, placeholder files only)" -ForegroundColor DarkGray

    $lcLines = @(
        "LADDER_SNAPSHOT_PLACEHOLDER",
        ("Date: " + $Date),
        "Generator: scaffold_market_close_ingestion.ps1 (DryRun mode)",
        "Action required: replace this file with real quicktiny output."
    )
    $lcContent = ($lcLines -join $CRLF) + $CRLF
    Write-Utf8BomFile -FilePath $Step1_LadderFile -FileContent $lcContent

    $scLines = @(
        "SECTOR_SNAPSHOT_PLACEHOLDER",
        ("Date: " + $Date),
        "Generator: scaffold_market_close_ingestion.ps1 (DryRun mode)",
        "Action required: replace this file with real quicktiny output."
    )
    $scContent = ($scLines -join $CRLF) + $CRLF
    Write-Utf8BomFile -FilePath $Step1_SectorFile -FileContent $scContent

    Write-Host "  [DONE] Placeholder files created:" -ForegroundColor Green
    $doneL = "         - {0}" -f $Step1_LadderFile
    $doneS = "         - {0}" -f $Step1_SectorFile
    Write-Host $doneL -ForegroundColor Green
    Write-Host $doneS -ForegroundColor Green

    $r1 = NewChecklistRow -s "Step1" `
        -a "QuickTiny Capture (Ladder + Sector)" `
        -p $Step1_Dir `
        -st "OK Placeholder" `
        -dn "No exe. Run quicktiny manually to replace 2 placeholder txt."
    [void]$checklistRows.Add($r1)
}
Write-Host ""

# ============================================================
# STEP 2
# ============================================================
Write-Host "[Step 2/3] LiveRoom 24 Viewport JSON" -ForegroundColor Yellow
Write-Host $SEP_THIN -ForegroundColor Gray

$Step2_DirName = "live_room_raw_" + $Date
$Step2_Dir = Join-Path $OutRoot $Step2_DirName

if ($DryRun) {
    if (-not (Test-Path $Step2_Dir)) {
        New-Item -ItemType Directory -Path $Step2_Dir -Force | Out-Null
    }

    $mxUrlPieces = @("mx2025.hhhuu.com", $CH_SLASH, "#")
    $mxUrl = $mxUrlPieces -join ""
    $remind1 = "  [REMIND] USER ACTION REQUIRED: open " + $mxUrl + " and manually export 24 rooms viewport JSON"
    $remind2 = "  [REMIND] Overwrite files into: {0}" -f $Step2_Dir
    Write-Host $remind1 -ForegroundColor Magenta
    Write-Host $remind2 -ForegroundColor Magenta
    Write-Host ""

    $idxRoom = 0
    foreach ($roomName in $ROOM_NAMES) {
        $idxRoom++
        $prefixStr = $idxRoom.ToString("00")
        $jsonFileName = $prefixStr + $roomName + "_" + $Date + ".json"
        $jsonFullPath = Join-Path $Step2_Dir $jsonFileName
        CreateEmptyFile -FilePath $jsonFullPath
        if ($idxRoom -le 9) {
            $lineA = "  [A] {0} (0-byte placeholder)" -f $jsonFullPath
            Write-Host $lineA -ForegroundColor Cyan
        } else {
            $lineB = "  [B] {0} (0-byte placeholder)" -f $jsonFullPath
            Write-Host $lineB -ForegroundColor DarkCyan
        }
    }

    Write-Host ""
    Write-Host "  [DONE] 24 placeholder JSON created (Bucket A: 9 rooms + Bucket B: 15 rooms)" -ForegroundColor Green
    $dirHint = "         Directory: {0}" -f $Step2_Dir
    Write-Host $dirHint -ForegroundColor Green

    $r2 = NewChecklistRow -s "Step2" `
        -a "LiveRoom 24 Viewport JSON (A9 + B15)" `
        -p $Step2_Dir `
        -st "OK Placeholder" `
        -dn "24 zero-byte JSON. Export from mx2025 to overwrite each."
    [void]$checklistRows.Add($r2)
}
Write-Host ""

# ============================================================
# STEP 3
# ============================================================
Write-Host "[Step 3/3] Ingestion Checklist Markdown" -ForegroundColor Yellow
Write-Host $SEP_THIN -ForegroundColor Gray

$Step3_FileName = "ingestion_checklist_" + $Date + ".md"
$Step3_FilePath = Join-Path $OutRoot $Step3_FileName

if ($DryRun) {
    $mdBuilder = New-Object System.Text.StringBuilder

    [void]$mdBuilder.Append("# Ingestion Checklist | ")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("> Generator: scaffold_market_close_ingestion.ps1 -DryRun -Date ")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("> BatchDir: ")
    [void]$mdBuilder.Append($BatchRoot)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("---")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("## Placeholders Generated (DryRun Auto)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("### Step1: QuickTiny (Ladder + Sector Top5)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- OutDir: ")
    [void]$mdBuilder.Append($Step1_Dir)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- [x] LADDER_SNAPSHOT_PLACEHOLDER_")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append(".txt")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- [x] SECTOR_SNAPSHOT_PLACEHOLDER_")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append(".txt")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("### Step2: LiveRoom 24 Viewport JSON")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- OutDir: ")
    [void]$mdBuilder.Append($Step2_Dir)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("#### Bucket A (Tier1, 9 rooms)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    $iA = 0
    foreach ($rn in $ROOM_NAMES) {
        $iA++
        if ($iA -le 9) {
            $s = $iA.ToString("00")
            [void]$mdBuilder.Append("- [x] ")
            [void]$mdBuilder.Append($s)
            [void]$mdBuilder.Append($rn)
            [void]$mdBuilder.Append("_")
            [void]$mdBuilder.Append($Date)
            [void]$mdBuilder.Append(".json (0B)")
            [void]$mdBuilder.Append($CRLF)
        }
    }
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("#### Bucket B (Tier2, 15 rooms)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    $iB = 0
    foreach ($rn in $ROOM_NAMES) {
        $iB++
        if ($iB -ge 10) {
            $s = $iB.ToString("00")
            [void]$mdBuilder.Append("- [x] ")
            [void]$mdBuilder.Append($s)
            [void]$mdBuilder.Append($rn)
            [void]$mdBuilder.Append("_")
            [void]$mdBuilder.Append($Date)
            [void]$mdBuilder.Append(".json (0B)")
            [void]$mdBuilder.Append($CRLF)
        }
    }
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("---")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("## Manual Tasks (2 items)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("### Manual Task 1 of 2: Launch QuickTiny for real capture")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("Command line (copy, paste, execute):")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($MD_CODE_FENCE)
    [void]$mdBuilder.Append($CRLF)
    $realCmd = ConcatArgs -binPath $QuickTinyBinPath -dateVal $Date -outDir $Step1_Dir
    [void]$mdBuilder.Append($realCmd)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($MD_CODE_FENCE)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    if (-not $qtExists) {
        [void]$mdBuilder.Append("- WARNING: QuickTiny binary missing at ")
        [void]$mdBuilder.Append($QuickTinyBinPath)
        [void]$mdBuilder.Append(". Verify path first.")
        [void]$mdBuilder.Append($CRLF)
        [void]$mdBuilder.Append($CRLF)
    }

    [void]$mdBuilder.Append("Expected result: ladder TSV + sector Top5 JSON written into the same outdir, replacing placeholders.")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("### Manual Task 2 of 2: Export 24 JSON from mx2025 site")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- Site URL: ")
    [void]$mdBuilder.Append($mxUrl)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- Enter each of 24 rooms, export that day viewport JSON")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- Naming rule: 2-digit prefix + room name + _YYYYMMDD.json (match placeholder exactly)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- Overwrite into: ")
    [void]$mdBuilder.Append($Step2_Dir)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("- Order: Bucket A first (9 rooms), then Bucket B (15 rooms)")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("---")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("## Next Step: Deploy to daily batch dir + Trigger ingestion")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append("When all placeholders replaced with real data:")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("1. Copy real quicktiny outputs from ")
    [void]$mdBuilder.Append($Step1_DirName)
    [void]$mdBuilder.Append(" into oldrepo 02_runtime")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("batch_daily_")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("00_raw")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("quicktiny")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("2. Copy real JSON files from ")
    [void]$mdBuilder.Append($Step2_DirName)
    [void]$mdBuilder.Append(" into oldrepo 02_runtime")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("batch_daily_")
    [void]$mdBuilder.Append($Date)
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("00_raw")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append("live_rooms")
    [void]$mdBuilder.Append($CH_SLASH)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("3. Trigger ingestion command (see A5 unified index doc for exact口令).")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    [void]$mdBuilder.Append("---")
    [void]$mdBuilder.Append($CRLF)
    [void]$mdBuilder.Append($CRLF)

    $tsNow = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    [void]$mdBuilder.Append("_Generated by scaffold_market_close_ingestion.ps1 (DryRun) at ")
    [void]$mdBuilder.Append($tsNow)
    [void]$mdBuilder.Append("_")
    [void]$mdBuilder.Append($CRLF)

    Write-Utf8BomFile -FilePath $Step3_FilePath -FileContent $mdBuilder.ToString()

    Write-Host "  [DONE] Checklist MD created:" -ForegroundColor Green
    $ckDone = "         {0}" -f $Step3_FilePath
    Write-Host $ckDone -ForegroundColor Green

    $r3 = NewChecklistRow -s "Step3" `
        -a "Ingestion Checklist Markdown" `
        -p $Step3_FilePath `
        -st "OK Generated" `
        -dn "MD: placeholders list + 2 manual tasks + next steps."
    [void]$checklistRows.Add($r3)
}
Write-Host ""

# ============================================================
# CONSOLE TABLE SUMMARY  (3 x 5)
# ============================================================
Write-Host $SEPARATOR -ForegroundColor Cyan
Write-Host "  DryRun Checklist (3 rows x 5 cols)" -ForegroundColor Cyan
Write-Host $SEPARATOR -ForegroundColor Cyan
Write-Host ""

$colStepW = 6
$colActW  = 22
$colPathW = 42
$colStW   = 14
$colNoteW = 36

function Pad-R {
    param([string]$s, [int]$w)
    if ($s.Length -ge $w) { return $s.Substring(0, $w) }
    return $s + ($CH_SPC.ToString() * ($w - $s.Length))
}
function Pad-L {
    param([string]$s, [int]$w)
    if ($s.Length -ge $w) { return $s.Substring(0, $w) }
    return ($CH_SPC.ToString() * ($w - $s.Length)) + $s
}
$V = [char]124
function PaintLine {
    param($a,$b,$c,$d,$e,$color="Gray")
    $line = (Pad-R $a $colStepW) + $V + (Pad-R $b $colActW) + $V + (Pad-R $c $colPathW) + $V + (Pad-R $d $colStW) + $V + (Pad-R $e $colNoteW)
    Write-Host $line -ForegroundColor $color
}

$dashLine = ($CH_DASH.ToString() * ($colStepW + $colActW + $colPathW + $colStW + $colNoteW + 4))

Write-Host $dashLine -ForegroundColor DarkCyan
PaintLine "Step" "Action" "Path" "Status" "DryRun Note" Cyan
Write-Host $dashLine -ForegroundColor DarkCyan
$rn = 0
foreach ($cr in $checklistRows) {
    $rn++
    if ($rn % 2 -eq 0) { $fc = "White" } else { $fc = "Gray" }
    PaintLine $cr.Step $cr.Action $cr.Path $cr.Status $cr.DryRunNote $fc
}
Write-Host $dashLine -ForegroundColor DarkCyan
Write-Host ""
Write-Host ("Cols: 1=Step  2=Action  3=Path  4=Status  5=DryRun Note  (Total 5 cols)") -ForegroundColor DarkCyan
Write-Host ""
Write-Host ("All 3 Steps DryRun completed. Review checklist for manual tasks.") -ForegroundColor Cyan
Write-Host ("Checklist file: {0}" -f $Step3_FilePath) -ForegroundColor Cyan
