$ErrorActionPreference = "Stop"

$toolsWorkspace = "D:\Stock\trading_assistant\20_tools_workspace"
$outDir = "D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_oldrepo_cleanup__20260811\tools_readme_out"
$tplPath = "D:\Stock\trading_assistant\90_SCRATCH_AND_TEST_ZONE\batch_oldrepo_cleanup__20260811\skeleton_template.md"

if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$dirs = @(
    "batch_01_selected",
    "batch_02_group08_pipeline",
    "batch_03_general_ingest_tools",
    "batch_04_tk_r6_manual_sheet_tools",
    "batch_05_tk_r7_manual_sheet_tools",
    "batch_06_tk_r8_manual_sheet_tools",
    "batch_07_info_live_room_tools",
    "batch_08_quicktiny_capture_tools",
    "_raw_snapshot_batch09"
)

$skeletonTpl = [System.IO.File]::ReadAllText($tplPath, [System.Text.Encoding]::UTF8)

$auditResults = New-Object System.Collections.ArrayList

foreach ($dirName in $dirs) {
    $dirPath = Join-Path $toolsWorkspace $dirName
    $readmePath = Join-Path $dirPath "README.md"

    $hasReadme = Test-Path $readmePath

    if ($hasReadme) {
        $content = [System.IO.File]::ReadAllText($readmePath, [System.Text.Encoding]::UTF8)
    } else {
        $content = ""
    }

    $lines = @()
    if ($content.Length -gt 0) {
        $lines = $content -split "`r?`n"
    }

    function Test-SectionPresence {
        param(
            [string[]]$Lines,
            [string[]]$Keywords,
            [int]$MinContextLen = 25,
            [int]$LookAhead = 12,
            [scriptblock]$ExtraCheck = $null
        )
        if ($Lines.Count -eq 0) { return $false }
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            foreach ($kw in $Keywords) {
                if ($Lines[$i] -match [regex]::Escape($kw) -or `
                    ($Lines[$i] -match "(?i)$kw") {
                    $ctx = New-Object System.Collections.ArrayList
                    for ($j = $i; $j -lt [Math]::Min($i + $LookAhead, $Lines.Count); $j++) {
                        [void]$ctx.Add($Lines[$j])
                    }
                    $ctxText = ($ctx -join "`n").Trim()
                    if ($ctxText.Length -ge $MinContextLen) {
                        if ($ExtraCheck -ne $null) {
                            return & $ExtraCheck $ctxText
                        }
                        return $true
                    }
                }
            }
        }
        return $false
    }

    $depKws = @("依赖", "requirements", "depend", "pip install", "Python 版本", "Python version", "系统库", "环境要求")
    $hasDep = Test-SectionPresence -Lines $lines -Keywords $depKws -MinContextLen 20 -LookAhead 10

    $inKws = @("输入", "input", "数据来源", "TSV", "JSON", "CSV", "文件路径", "示例文件", "文件名")
    $hasInput = Test-SectionPresence -Lines $lines -Keywords $inKws -MinContextLen 25 -LookAhead 12

    $outKws = @("输出", "output", "结果", "产物", "artifact", "列结构", "字段", "命名规范", "文件命名")
    $hasOutput = Test-SectionPresence -Lines $lines -Keywords $outKws -MinContextLen 25 -LookAhead 12

    $cmdCheck = {
        param($t)
        if ($t.Length -lt 20) { return $false }
        return ($t -match "python" -or $t -match "\.ps1" -or $t -match "\.bat" -or `
                $t -match "--dry-run" -or $t -match "\.py" -or $t -match "Usage" -or $t -match "Example")
    }
    $cmdKws = @("命令样例", "使用示例", "运行命令", "示例", "Example", "Usage", "python", ".\", "--dry-run", "实跑", "命令行")
    $hasCmd = Test-SectionPresence -Lines $lines -Keywords $cmdKws -MinContextLen 20 -LookAhead 15 -ExtraCheck $cmdCheck

    $missingCount = 0
    if (-not $hasDep) { $missingCount++ }
    if (-not $hasInput) { $missingCount++ }
    if (-not $hasOutput) { $missingCount++ }
    if (-not $hasCmd) { $missingCount++ }

    $allComplete = ($hasDep -and $hasInput -and $hasOutput -and $hasCmd)

    if ($allComplete) {
        $statusFile = Join-Path $outDir ($dirName + "_README_status.md")
        [System.IO.File]::WriteAllText($statusFile, "4要素齐全，无需补", [System.Text.Encoding]::UTF8)
        $result = "生成status"
    } else {
        $skeletonFile = Join-Path $outDir ($dirName + "_README_skeleton.md")
        $filled = $skeletonTpl.Replace("__DIR_NAME__", $dirName)
        [System.IO.File]::WriteAllText($skeletonFile, $filled, [System.Text.Encoding]::UTF8)
        $result = "生成skeleton"
    }

    $obj = [PSCustomObject]@{
        DirName     = $dirName
        HasReadme   = $(if ($hasReadme) { "Y" } else { "N" })
        Dep         = $(if ($hasDep) { "Y" } else { "N" })
        Inp         = $(if ($hasInput) { "Y" } else { "N" })
        Out         = $(if ($hasOutput) { "Y" } else { "N" })
        Cmd         = $(if ($hasCmd) { "Y" } else { "N" })
        Missing     = $missingCount
        Result      = $result
    }
    [void]$auditResults.Add($obj)
}

function Write-ColoredCell {
    param([string]$Text, [string]$Val, [int]$Pad)
    $c = if ($Val -eq "Y") { "Green" } else { "Red" }
    Write-Host (" {0,-$Pad}" -f $Text) -ForegroundColor $c -NoNewline
}

Write-Host ""
Write-Host ("=" * 110) -ForegroundColor Cyan
Write-Host ("{0,-34} {1,-7} {2,-5} {3,-5} {4,-5} {5,-7} {6,-7} {7,-12}" -f `
    "目录名", "README", "依赖", "输入", "输出", "命令样例", "缺失数", "处理结果") `
    -ForegroundColor Cyan
Write-Host ("-" * 110)

$totalMissing = 0
foreach ($r in $auditResults) {
    $totalMissing += $r.Missing
    Write-Host ("{0,-34} {1,-7}" -f $r.DirName, $r.HasReadme) -NoNewline
    Write-ColoredCell -Text $r.Dep -Val $r.Dep -Pad 5
    Write-ColoredCell -Text $r.Inp -Val $r.Inp -Pad 5
    Write-ColoredCell -Text $r.Out -Val $r.Out -Pad 5
    Write-ColoredCell -Text $r.Cmd -Val $r.Cmd -Pad 7
    Write-Host (" {0,-7} {1,-12}" -f $r.Missing, $r.Result)
}

Write-Host ("-" * 110)
Write-Host ("{0,-34} {1,-7} {2,-5} {3,-5} {4,-5} {5,-7} {6,-7}" -f `
    "合计（9个目录）", "", "", "", "", "", $totalMissing) `
    -ForegroundColor Yellow
Write-Host ("=" * 110) -ForegroundColor Cyan
Write-Host ""
Write-Host ("输出目录: {0}" -f $outDir) -ForegroundColor Gray
