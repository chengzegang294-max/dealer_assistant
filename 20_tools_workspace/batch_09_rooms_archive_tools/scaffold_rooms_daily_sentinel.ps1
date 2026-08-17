param(
    [switch]$DryRun = $true,
    [string]$TradeDateYYYYMMDD = "AUTO_TODAY_OR_PREV_WORKDAY",
    [string]$RoomsRoot = "D:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\rooms",
    [string]$SentinelIndexPath = "",
    [string]$OutDir = "D:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\rooms_daily_sentinel"
)
$ErrorActionPreference = "Stop"
function prev-workday([DateTime]$d){
    $r = $d
    while($r.DayOfWeek -in @('Saturday','Sunday')){ $r = $r.AddDays(-1) }
    return $r.ToString('yyyyMMdd')
}
if([string]::IsNullOrWhiteSpace($SentinelIndexPath)){
    $SentinelIndexPath = Join-Path $RoomsRoot "SENTINEL_INDEX.md"
}
if($TradeDateYYYYMMDD -eq 'AUTO_TODAY_OR_PREV_WORKDAY'){
    $TradeDateYYYYMMDD = prev-workday (Get-Date)
}
$TradeDash = $TradeDateYYYYMMDD.Substring(0,4) + '-' + $TradeDateYYYYMMDD.Substring(4,2) + '-' + $TradeDateYYYYMMDD.Substring(6,2)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$OutTsv = Join-Path $OutDir ("rooms_daily_status__" + $TradeDateYYYYMMDD + ".tsv")

# 从 SENTINEL_INDEX.md 读 24 房正式名（UTF-8 无 BOM 安全读）
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$sentinelRaw = [System.IO.File]::ReadAllText($SentinelIndexPath, [System.Text.Encoding]::UTF8)
$aBucketList = New-Object System.Collections.Generic.List[object]
$mdRow = [regex]::Matches($sentinelRaw, '(?m)^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([AB])\s*\|')
foreach($m in $mdRow){
    $seq = [int]$m.Groups[1].Value
    $name = $m.Groups[2].Value.Trim()
    $bucket = $m.Groups[3].Value.Trim()
    if($bucket -eq 'A' -and $seq -ge 1 -and $seq -le 9){
        $aBucketList.Add([PSCustomObject]@{ Seq = $seq; Name = $name; Bucket = $bucket })
    }
}
$aBucketList = $aBucketList | Sort-Object Seq
Write-Host ("Loaded A Bucket {0} rooms from SENTINEL_INDEX.md (Seq 1..9)" -f $aBucketList.Count)

$tab = "`t"
$lines = New-Object System.Collections.Generic.List[string]
$header = 'BucketSeq' + $tab + 'RoomName' + $tab + 'Bucket' + $tab + 'TradeDate' + $tab + 'S1_RawTodayExist' + $tab + 'S2_RawTodayFileCount' + $tab + 'S3_RawAnomalyTooFew' + $tab + 'S4_IngestDraftExists' + $tab + 'S5_NotesAbsorbedMark' + $tab + 'S6_ManualJudgement3cellsFilled' + $tab + 'S7_LatestRawDateGTE_TradeDate' + $tab + 'SummaryTag' + $tab + 'Note'
$lines.Add($header)
$redCnt = 0
$yellowCnt = 0
$greenCnt = 0

foreach($room in $aBucketList){
    $seqStr = [string]$room.Seq
    $name = $room.Name
    $bkt = $room.Bucket
    $rd = Join-Path $RoomsRoot ($name + '\00_raw')
    $ing = Join-Path $RoomsRoot ($name + '\10_ingest')
    $abs = Join-Path $RoomsRoot ($name + '\20_absorb\NOTES.md')
    $S1 = 'NO'
    $S2 = 0
    $S3 = 'OK'
    $S4 = 'NO'
    $S5 = 'NO'
    $S6 = 'NO'
    $S7 = 'NO'
    $latestDate = 'NONE'
    if(Test-Path -LiteralPath $rd){
        $all = @(Get-ChildItem -LiteralPath $rd -Filter '*.json' -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending)
        if($all.Count -gt 0){
            $latestFile = $all[0]
            if($latestFile.Name -match '(20\d{6})'){
                $latestDate = $Matches[1]
            }
            $todayOnes = @($all | Where-Object { $_.Name -like ('*' + $TradeDateYYYYMMDD + '*') })
            $S2 = $todayOnes.Count
            if($S2 -gt 0){ $S1 = 'YES' }
            if($latestDate -ge $TradeDateYYYYMMDD){ $S7 = 'YES' }
        }
    }
    if(Test-Path -LiteralPath $ing){
        $drafts = @(Get-ChildItem -LiteralPath $ing -Filter '*_NOTES_partial_prefill.md' -ErrorAction SilentlyContinue | Where-Object { $_.Name -like ('*' + $TradeDateYYYYMMDD + '*') })
        if($drafts.Count -gt 0){ $S4 = 'YES' }
    }
    if(Test-Path -LiteralPath $abs){
        $txt = [System.IO.File]::ReadAllText($abs, [System.Text.Encoding]::UTF8)
        if($txt -match ('已吸收\s*@\s*' + [regex]::Escape($TradeDash))){
            $S5 = 'YES'
        }
        if($S4 -eq 'YES' -or $S5 -eq 'YES'){
            $m1 = [regex]::Match($txt, '情绪偏多空[^：]*：[^_\r\n]{2,}')
            $m2 = [regex]::Match($txt, '主抓风格[^：]*：[^_\r\n]{2,}')
            $m3 = [regex]::Match($txt, '次日节奏[^：]*：[^_\r\n]{2,}')
            if($m1.Success -and $m2.Success -and $m3.Success){
                $S6 = 'YES'
            } elseif ($m1.Success -or $m2.Success -or $m3.Success) {
                $S6 = 'PARTIAL'
            }
        }
    }
    $flags = @($S1,$S4,$S5,$S6,$S7)
    $g = 0
    foreach($f in $flags){ if($f -eq 'YES'){ $g++ } }
    if($S1 -eq 'NO'){
        $tag = 'RED_MISSING_RAW'
        $redCnt++
    } elseif($g -ge 4){
        $tag = 'GREEN_LOOP_DONE'
        $greenCnt++
    } elseif($g -ge 2){
        $tag = 'YELLOW_HALF'
        $yellowCnt++
    } else {
        $tag = 'YELLOW_START'
        $yellowCnt++
    }
    $note = 'LatestRaw=' + $latestDate
    if($S3 -ne 'OK'){ $note = $note + ';' + $S3 }
    $row = $seqStr + $tab + $name + $tab + $bkt + $tab + $TradeDateYYYYMMDD + $tab + $S1 + $tab + [string]$S2 + $tab + $S3 + $tab + $S4 + $tab + $S5 + $tab + $S6 + $tab + $S7 + $tab + $tag + $tab + $note
    $lines.Add($row)
}

[System.IO.File]::WriteAllLines($OutTsv, $lines, $utf8NoBom)
Write-Host '=== Rooms Daily Sentinel (A Bucket x9 x 7 states) ==='
Write-Host ('TradeDate = ' + $TradeDateYYYYMMDD + ' (previous workday if auto)')
Write-Host ('Sentinel index = ' + $SentinelIndexPath)
Write-Host ('Output TSV = ' + $OutTsv + '  (DryRun = ' + [string]$DryRun + ')')
Write-Host ('Counts  RED_MISSING_RAW=' + [string]$redCnt + '  YELLOW(START|HALF)=' + [string]$yellowCnt + '  GREEN_LOOP_DONE=' + [string]$greenCnt + '  TOTAL=' + [string]$aBucketList.Count)
Write-Host ''
Import-Csv -LiteralPath $OutTsv -Delimiter "`t" | Format-Table BucketSeq,RoomName,S1_RawTodayExist,S2_RawTodayFileCount,S4_IngestDraftExists,S5_NotesAbsorbedMark,S6_ManualJudgement3cellsFilled,S7_LatestRawDateGTE_TradeDate,SummaryTag,Note -AutoSize -Wrap
