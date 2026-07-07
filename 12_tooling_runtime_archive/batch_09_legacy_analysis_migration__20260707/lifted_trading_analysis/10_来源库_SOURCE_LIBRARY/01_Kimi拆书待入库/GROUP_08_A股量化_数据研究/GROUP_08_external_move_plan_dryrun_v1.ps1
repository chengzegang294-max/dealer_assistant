param([switch]$Execute)
$DryRun = -not $Execute
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $env:ALLOW_ARCHIVE_ONLY_RUN) { throw "ARCHIVE_ONLY: legacy dryrun script references D:\\Stock\\cut_file (physically removed). Set ALLOW_ARCHIVE_ONLY_RUN=1 to run intentionally." }

Write-Host 'MOVE A-001'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之一：——利用债券YTM打造行业风格导航仪.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之一：——利用债券YTM打造行业风格导航仪.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-002'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之二——强弱趋势捕捉组合投资机会.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之二——强弱趋势捕捉组合投资机会.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-003'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之三：——基于涨跌比择时的绝对收益动量策略.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之三：——基于涨跌比择时的绝对收益动量策略.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-004'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之四：——基于残差动量的相对收益动量策略.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\风格轮动模型\华夏上证行业ETF风格轮动策略之四：——基于残差动量的相对收益动量策略.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-005'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\基于涨跌比的行业轮动与择时研究.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\基于涨跌比的行业轮动与择时研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-006'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\妙用涨跌比，小盘指数巧择时.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\妙用涨跌比，小盘指数巧择时.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-007'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\基于板块效应动量反转特征的alpha策略研究.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\基于板块效应动量反转特征的alpha策略研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-008'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\行业动量策略进阶之一：间隔期、系统性风险及换手率的影响.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\行业动量策略进阶之一：间隔期、系统性风险及换手率的影响.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-009'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\板块持仓测算在创业板风格轮动中的应用.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\板块持仓测算在创业板风格轮动中的应用.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-010'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\海通AK行业轮动策略——结构性行情必杀技.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\海通AK行业轮动策略——结构性行情必杀技.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-011'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\风格轮动模型\如虎添翼,两融带给ETF的投资机会——海通ETF风格轮动模型实证分析.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\风格轮动模型\如虎添翼,两融带给ETF的投资机会——海通ETF风格轮动模型实证分析.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-012'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在工程机械行业的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在工程机械行业的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-013'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在煤炭行业的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在煤炭行业的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-014'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在电力行业的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在电力行业的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-015'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在钢铁行业的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业基本面预测模型\行业基本面预测——在钢铁行业的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE A-016'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化资产配置 17份\行业轮动模型\衍生产品及量化组合管理策略介绍.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化资产配置 17份\行业轮动模型\衍生产品及量化组合管理策略介绍.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-001'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\A股全市场选股策略研究.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\A股全市场选股策略研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-002'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\财务指标选股研究系列\A股上市公司毛利率的均值回归及选股实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\财务指标选股研究系列\A股上市公司毛利率的均值回归及选股实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-004'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\A股市场特征研究（二）——波段划分新方法及应用展望.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\选股因子研究系列\A股市场特征研究（二）——波段划分新方法及应用展望.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-005'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\从极值角度进行选股因子有效性的确认——在换手率上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\从极值角度进行选股因子有效性的确认——在换手率上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-006'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\分析师荐股能力评定与跟踪.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\分析师荐股能力评定与跟踪.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-007'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\高估值，你是否师出有名？.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\高估值，你是否师出有名？.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-008'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\工欲善其事，必先利其器——选股因子深度解析.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\选股因子研究系列\工欲善其事，必先利其器——选股因子深度解析.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-011'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\量化选股之事件驱动策略.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\量化选股之事件驱动策略.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-012'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\如何捕捉短线反弹机会？.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\选股因子研究系列\如何捕捉短线反弹机会？.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-013'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\商业贸易行业选股策略.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\商业贸易行业选股策略.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-014'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\财务指标选股研究系列\上市公司动量反转以及市值因子的选股识别度.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\财务指标选股研究系列\上市公司动量反转以及市值因子的选股识别度.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-015'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\财务指标选股研究系列\上市公司估值指标的稳定性与选股识别度.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\财务指标选股研究系列\上市公司估值指标的稳定性与选股识别度.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-016'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之一——业绩预告之一——把握扭亏、预减公告，获取短期超额收益.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之一——业绩预告之一——把握扭亏、预减公告，获取短期超额收益.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-017'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之二——关注主板预减快报后的短期反弹机会以及中小板盈利公告.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之二——关注主板预减快报后的短期反弹机会以及中小板盈利公告.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-018'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之三——指数样本股调整.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之三——指数样本股调整.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-019'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之四——ETF事件套利研究.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之四——ETF事件套利研究.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-020'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之五——大股东增减持——关注增持比例较大的事件机会.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之五——大股东增减持——关注增持比例较大的事件机会.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-021'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之六——规避预案陷阱，把握实施收益.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之六——规避预案陷阱，把握实施收益.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-022'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之七——高送转行情下的事件性投资机会.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之七——高送转行情下的事件性投资机会.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-023'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之九——股权激励续篇.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之九——股权激励续篇.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-024'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之十一——事件驱动组合止损机制设计.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之十一——事件驱动组合止损机制设计.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-025'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之十二——重要股东持股结构变化蕴含的信息分析.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之十二——重要股东持股结构变化蕴含的信息分析.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-026'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\事件驱动策略系列\事件驱动策略之十三——定增事件投资——甄别市场，把握买点.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\事件驱动策略系列\事件驱动策略之十三——定增事件投资——甄别市场，把握买点.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-027'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\现金流量市值比因子的极值效应.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\选股因子研究系列\现金流量市值比因子的极值效应.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-028'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——全市场选股方法改进.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——全市场选股方法改进.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-029'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——在房地产行业上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——在房地产行业上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-030'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——在纺织服装行业上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——在纺织服装行业上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-031'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——在公用事业行业上的实证以及选股因子权重的再讨论.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——在公用事业行业上的实证以及选股因子权重的再讨论.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-032'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——在化学工业行业上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——在化学工业行业上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-033'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\多因子选股模型\相关性选股策略——在有色金属行业上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\多因子选股模型\相关性选股策略——在有色金属行业上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-034'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\选股因子研究系列\行业内股票业绩弹性分析——在钢铁行业上的实证.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\选股因子研究系列\行业内股票业绩弹性分析——在钢铁行业上的实证.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-035'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\成长股选股模型\行业内选股策略——钢铁行业.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\成长股选股模型\行业内选股策略——钢铁行业.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE S-036'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化选股 40份\成长股选股模型\行业内选股策略——有色金属行业.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化选股 40份\成长股选股模型\行业内选股策略——有色金属行业.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE T-001'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化择时 3份\度量市场“恐惧与贪婪”的量化择时指标.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化择时 3份\度量市场“恐惧与贪婪”的量化择时指标.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE T-002'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化择时 3份\通过产业资本增减持数据构建的量化择时指标.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化择时 3份\通过产业资本增减持数据构建的量化择时指标.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

Write-Host 'MOVE T-003'
$src = 'D:\Stock\cut_file\《Python股票量化交易从入门到实践》完整版\2.其他量化资料(62份)（赠品）\量化择时 3份\量化择时——度量市场“恐惧与贪婪”的量化择时指标.pdf'
$dst = 'D:\Stock\cut_file\__GROUP_08_sorted\BOOKDIR\量化择时 3份\量化择时——度量市场“恐惧与贪婪”的量化择时指标.pdf'
if (-not (Test-Path -LiteralPath $src)) { Write-Warning ("missing source: " + $src); continue }
$dstDir = Split-Path -Parent $dst
if ($DryRun) { New-Item -ItemType Directory -Force -Path $dstDir -WhatIf | Out-Null } else { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
if ($DryRun) { Move-Item -LiteralPath $src -Destination $dst -Force -WhatIf } else { Move-Item -LiteralPath $src -Destination $dst -Force }

