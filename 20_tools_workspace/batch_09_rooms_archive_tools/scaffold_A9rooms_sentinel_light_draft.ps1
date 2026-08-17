<#
  scaffold_A9rooms_sentinel_light_draft.ps1 v3
  A bucket 9 rooms daily sentinel lightweight DRAFT prototype.
  Scope: ONLY 3 checks (NOT 7 states, user asked for light, no over-fitting)
    S1 = Raw JSON of trade-date exist under rooms/<name>/00_raw/*.json with YYYYMMDD prefix
    S2 = Human-readable summary (10_ingest/*_YYYYMMDD_人读摘要旧到新.md) generated today
    S3 = You put a line "已吸收 @ YYYY-MM-DD" inside rooms/<name>/20_absorb/NOTES.md
  PS5 GBK-safe rules:
    - Room names read from SENTINEL_INDEX.md table column A (1..9) using UTF-8 read
      (NEVER hardcode CJK string arrays because PS5 reads file in Default/GBK encoding)
    - Status tag strings are pure ASCII: RED_DRAFT_NO_RAW / YELLOW_DRAFT_WIP / GREEN_DRAFT_PASS
    - No full-width parenthesis U+FF08/FF09 anywhere inside status strings or string literals
  Default = DryRun (print only). Pass -Apply to write TSV.
  Example:
    & .\scaffold_A9rooms_sentinel_light_draft.ps1 -TradeDateYYYYMMDD 20260811 -Apply
#>
param(
  [string]$TradeDateYYYYMMDD = 'AUTO',
  [string]$RoomsRoot = 'D:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\rooms',
  [string]$SentinelIndexPath = '',
  [string]$OutDir = 'D:\Stock\dealer_assistant\02_runtime\info_live_room_sampling\rooms_daily_sentinel',
  [switch]$Apply = $false
)

function auto_workday([string]$d){
  if($d -ne 'AUTO'){ return $d }
  $dt = Get-Date
  for($i=0;$i -lt 10;$i++){
    $t = $dt.AddDays(-$i)
    [int]$dow = $t.DayOfWeek
    if($dow -ge 1 -and $dow -le 5){ return $t.ToString('yyyyMMdd') }
  }
  return $dt.ToString('yyyyMMdd')
}
$td = auto_workday $TradeDateYYYYMMDD
$td_dash = $td.Substring(0,4) + '-' + $td.Substring(4,2) + '-' + $td.Substring(6,2)
if([string]::IsNullOrWhiteSpace($SentinelIndexPath)){
  $SentinelIndexPath = Join-Path $RoomsRoot 'SENTINEL_INDEX.md'
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$aBucket = New-Object System.Collections.Generic.List[string]
if(-not (Test-Path -LiteralPath $SentinelIndexPath)){
  Write-Error ('FATAL: SENTINEL_INDEX not found at ' + $SentinelIndexPath)
  exit 2
}
$sentinelUtf8 = [System.IO.File]::ReadAllText($SentinelIndexPath, [System.Text.Encoding]::UTF8)
$mRow = [regex]::Matches($sentinelUtf8, '(?m)^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([AB])\s*\|')
foreach($m in $mRow){
  if($m.Groups[3].Value -ne 'A'){ continue }
  [int]$seq = [int]::Parse($m.Groups[1].Value.Trim())
  if($seq -ge 1 -and $seq -le 9){ $aBucket.Add(($m.Groups[2].Value).Trim()) }
}
if($aBucket.Count -eq 0){
  Write-Error ('FATAL: SENTINEL_INDEX parse failed - bucket A rows 1..9 empty, got ' + $aBucket.Count)
  exit 3
}

$y_re = [regex]::new('(20\d{6})')
$abs_re = [regex]::new(('已吸收\s*@\s*' + [regex]::Escape($td_dash)))
$rows = New-Object System.Collections.Generic.List[object]
$summary = New-Object System.Collections.Generic.List[string]

foreach($n in $aBucket){
  $rd = Join-Path $RoomsRoot ($n + '\00_raw')
  $s1 = 'NO'; $s1_cnt = 0; $s2 = 'NO'; $s3 = 'NO'
  if(Test-Path -LiteralPath $rd){
    $raws = @(Get-ChildItem -LiteralPath $rd -Filter '*.json' -ErrorAction SilentlyContinue)
    foreach($p in $raws){
      $mm = $y_re.Match($p.Name)
      if($mm.Success -and $mm.Groups[1].Value -eq $td){ $s1_cnt++ }
    }
    if($s1_cnt -gt 0){ $s1 = 'YES' }
  }
  $ing = Join-Path $RoomsRoot ($n + '\10_ingest')
  if(Test-Path -LiteralPath $ing){
    $dateTok = '_' + $td + '_'
    $sum = @(
      Get-ChildItem -LiteralPath $ing -File -ErrorAction SilentlyContinue |
        Where-Object {
          $_.Extension -ieq '.md' -and
          $_.Name -like ('*' + $dateTok + '*') -and
          $_.Name -notlike '*NOTES_partial_prefill*' -and
          $_.Name -ne 'NOTES.md'
        }
    )
    if($sum.Count -gt 0){ $s2 = 'YES' }
  }
  $notes = Join-Path $RoomsRoot ($n + '\20_absorb\NOTES.md')
  if(Test-Path -LiteralPath $notes){
    $txt = [System.IO.File]::ReadAllText($notes, [System.Text.Encoding]::UTF8)
    if($abs_re.IsMatch($txt)){ $s3 = 'YES' }
  }
  if($s1 -eq 'NO'){
    $light = 'RED_DRAFT_NO_RAW'
  } elseif ($s2 -eq 'NO' -or $s3 -eq 'NO') {
    $light = 'YELLOW_DRAFT_WIP'
  } else {
    $light = 'GREEN_DRAFT_PASS'
  }
  $all3 = 'NO'
  if($light -eq 'GREEN_DRAFT_PASS'){ $all3 = 'YES' }
  $rows.Add([PSCustomObject]@{
    RoomName_SeqInBucket = $n
    TradeDate = $td_dash
    S1_RawTodayExist = $s1
    S1_RawTodayFileCount = $s1_cnt
    S2_HumanSummaryTodayExist = $s2
    S3_ManualAbsorbMarkAtDateExist = $s3
    All3PASS = $all3
    LightTag_ASCII_Draft = $light
  })
  $summary.Add(('A ' + $n + ' - ' + $light + ' - S1=' + $s1 + ' S2=' + $s2 + ' S3=' + $s3))
}

Write-Host ('===== A9rooms_sentinel_light_draft  TradeDate=' + $td_dash + ' =====')
$summary | ForEach-Object { Write-Host ('  ' + $_) }
Write-Host '(Prototype DRAFT - ASCII tags only: RED_DRAFT_NO_RAW / YELLOW_DRAFT_WIP / GREEN_DRAFT_PASS)'
Write-Host ''

if($Apply){
  $outF = Join-Path $OutDir ('A9rooms_sentinel_daily__' + $td + '.tsv')
  $csvLines = @($rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation)
  $utf8NoBom = New-Object System.Text.UTF8Encoding $false
  [System.IO.File]::WriteAllLines($outF, $csvLines, $utf8NoBom)
  Write-Host ('[Apply] wrote TSV OK - ' + $outF + '   rows=' + $csvLines.Count)
  $rows | Select-Object RoomName_SeqInBucket,TradeDate,S1_RawTodayExist,S1_RawTodayFileCount,S2_HumanSummaryTodayExist,S3_ManualAbsorbMarkAtDateExist,All3PASS,LightTag_ASCII_Draft | Format-Table -AutoSize
} else {
  Write-Host '[DryRun] not written. Pass -Apply to write TSV.'
  Write-Host '  Example:'
  Write-Host ('    & ''' + $PSCommandPath + ''' -TradeDateYYYYMMDD ' + $td + ' -Apply')
}
return 0
