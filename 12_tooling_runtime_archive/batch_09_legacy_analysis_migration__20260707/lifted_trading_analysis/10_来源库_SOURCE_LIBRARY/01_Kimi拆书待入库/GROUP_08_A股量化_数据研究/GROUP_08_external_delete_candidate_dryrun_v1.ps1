param([switch]$Execute)
$DryRun = -not $Execute
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $env:ALLOW_ARCHIVE_ONLY_RUN) { throw "ARCHIVE_ONLY: legacy dryrun script references D:\\Stock\\cut_file (physically removed). Set ALLOW_ARCHIVE_ONLY_RUN=1 to run intentionally." }

Write-Host 'DELETE_CANDIDATE S-003'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究2：因子模型的尾部相关性研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-003: basename=3 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-009'
$src = 'd:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究6：极值视角下的多因子选股策略.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-009: basename=3 fullpath=0'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-010'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究21：分析师一致预期相关因子.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-010: basename=2 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-037'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究1：弱者终有逆袭日,强势几无持续时：A股市场的动量反转效应研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-037: basename=3 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-038'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究2：因子模型的尾部相关性研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-038: basename=3 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-039'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究3：从Spearman相关系数出发研究因子有效性，Kalman+Filter模型在因子选择中的应用.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-039: basename=2 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-040'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究4：多因子选股模型的有效与失效.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-040: basename=2 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

Write-Host 'DELETE_CANDIDATE S-041'
$src = 'D:\Stock\cut_file\S\03_券商研报\04_多因子\海通选股因子系列研究5：寻找股价驱动新因子净换手率.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
Write-Warning 'outside_group08_refs>0 for S-041: basename=2 fullpath=1'
if ($DryRun) { Remove-Item -LiteralPath $src -Force -WhatIf } else { Remove-Item -LiteralPath $src -Force }

