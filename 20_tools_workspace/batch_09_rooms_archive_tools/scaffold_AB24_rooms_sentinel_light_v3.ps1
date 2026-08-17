<#
  scaffold_AB24_rooms_sentinel_light_v3.ps1
  A+B 24 房每日盯梢 轻量原型 v3 (24房版；ASCII tag PS5 中文安全）
  Scope:
    S1 = rooms/<房>/00_raw/*.json 今日有没
    S2 = rooms/<房>/10_ingest/*_YYYYMMDD_*.md  Prefill草稿 / 人读摘要（至少1件）（排除 NOTES.md）
    S3 = rooms/<房>/20_absorb/NOTES.md 有没 已吸收 @ YYYY-MM-DD
  PS5 GBK-safe rules:
    - Room names read from UTF-8 SENTINEL_INDEX.md regex table rows #1..#24 (NOT hardcode CJK arrays)
    - Status tags pure ASCII: RED_NO_RAW / YELLOW_WIP / GREEN_PASS
    - No full-width parenthesis / CJK tag strings inside PowerShell string literals
  Default: DryRun (print only). Pass -Apply to write TSV.
  Example:
    & .\scaffold_AB24_rooms_sentinel_light_v3.ps1 -TradeDateYYYYMMDD 20260811 -Apply
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
if([string]::IsNullOrWhiteSpace($SentinelIndexPath)){ $SentinelIndexPath = Join-Path $RoomsRoot 'SENTINEL_INDEX.md' }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# Read 24 rooms from UTF-8 SENTINEL table (seq 1..24)
$bucket24 = New-Object System.Collections.Generic.List[string]
if(-not (Test-Path -LiteralPath $SentinelIndexPath)){
  Write-Error ('FATAL: SENTINEL_INDEX missing - ' + $SentinelIndexPath)
  exit 2
}
$utf8 = [System.IO.File]::ReadAllText($SentinelIndexPath, [System.Text.Encoding]::UTF8)
$rows = [regex]::Matches($utf8, '(?m)^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([AB])\s*\|')
foreach($m in $rows){
  [int]$seq = [int]::Parse($m.Groups[1].Value.Trim())
  if($seq -ge 1 -and $seq -le 24){ $bucket24.Add(($m.Groups[2].Value).Trim()) }
}
if($bucket24.Count -ne 24){
  Write-Error ('FATAL: SENTINEL parse got ' + $bucket24.Count + ' rows, must be exactly 24 (A#1-9 + B#10-24)')
  exit 3
}

$y_re = [regex]::new('(20\d{6})')
$abs_re = [regex]::new(('已吸收\s*@\s*' + [regex]::Escape($td_dash)))
$dateTok = '_' + $td + '_'
$outRows = New-Object System.Collections.Generic.List[object]
$summary = New-Object System.Collections.Generic.List[string]

foreach($n in $bucket24){
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
    $hits = @(
      Get-ChildItem -LiteralPath $ing -File -ErrorAction SilentlyContinue |
        Where-Object {
          $_.Extension -ieq '.md' -and
          $_.Name -like ('*' + $dateTok + '*') -and
          $_.Name -ne 'NOTES.md'
        }
    )
    if($hits.Count -gt 0){ $s2 = 'YES' }
  }
  $notes = Join-Path $RoomsRoot ($n + '\20_absorb\NOTES.md')
  if(Test-Path -LiteralPath $notes){
    $txt = [System.IO.File]::ReadAllText($notes, [System.Text.Encoding]::UTF8)
    if($abs_re.IsMatch($txt)){ $s3 = 'YES' }
  }
  if($s1 -eq 'NO'){
    $light = 'RED_NO_RAW'
  } elseif ($s2 -eq 'NO' -or $s3 -eq 'NO') {
    $light = 'YELLOW_WIP'
  } else {
    $light = 'GREEN_PASS'
  }
  $all3 = 'NO'
  if($light -eq 'GREEN_PASS'){ $all3 = 'YES' }
  $outRows.Add([PSCustomObject]@{
    Seq24 = ([array]::IndexOf($bucket24.ToArray(),$n) + 1)
    RoomName = $n
    TradeDate = $td_dash
    S1_RawTodayExist = $s1
    S1_RawTodayFileCount = $s1_cnt
    S2_DraftOrSummaryTodayExist = $s2
    S3_ManualAbsorbMarkAtDateExist = $s3
    All3PASS = $all3
    LightTag_ASCII_Draft = $light
  })
  $summary.Add(('  #{0,-2}  {1,-22}  {2}  S1={3}({4})  S2={5}  S3={6}' -f ($outRows.Count), $n, $light, $s1, $s1_cnt, $s2, $s3))
}

Write-Host ('===== AB24 rooms sentinel v3  td=' + $td_dash + '  24 rooms total =====')
$summary | ForEach-Object { Write-Host $_ }
$r = $outRows | Group-Object LightTag_ASCII_Draft -AsHashTable -AsString
Write-Host ''
Write-Host ('SUMMARY: 24 rooms = ' +
  'RED_NO_RAW='   + $(if($r -and $r.ContainsKey('RED_NO_RAW')){$r['RED_NO_RAW'].Count}else{0})   +
  '  YELLOW_WIP=' + $(if($r -and $r.ContainsKey('YELLOW_WIP')){$r['YELLOW_WIP'].Count}else{0}) +
  '  GREEN_PASS=' + $(if($r -and $r.ContainsKey('GREEN_PASS')){$r['GREEN_PASS'].Count}else{0}))
Write-Host ''

if($Apply){
  $outF = Join-Path $OutDir ('AB24rooms_sentinel_daily__' + $td + '.tsv')
  $csvLines = @($outRows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation)
  $utf8nobom = New-Object System.Text.UTF8Encoding $false
  [System.IO.File]::WriteAllLines($outF, $csvLines, $utf8nobom)
  Write-Host ('[Apply] wrote TSV - ' + $outF + '   rows (hdr+data)=' + $csvLines.Count)
  $outRows | Select-Object Seq24,RoomName,TradeDate,S1_RawTodayExist,S1_RawTodayFileCount,S2_DraftOrSummaryTodayExist,S3_ManualAbsorbMarkAtDateExist,All3PASS,LightTag_ASCII_Draft | Format-Table -AutoSize
} else {
  Write-Host '[DryRun] not written. Pass -Apply to write TSV.'
  Write-Host ('  Example: & ''' + $PSCommandPath + ''' -TradeDateYYYYMMDD ' + $td + ' -Apply')
}
return 0
