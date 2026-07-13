# 巨潮公告采集 - 一键运行脚本
# 用法: .\run.ps1 -StockCode 601012 -CompanyName 隆基绿能

param(
    [Parameter(Mandatory = $true)]
    [string]$StockCode,

    [string]$CompanyName = "",

    [string]$StartDate = "",

    [string]$EndDate = "",

    [int]$MaxPages = 0,

    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "未找到虚拟环境，正在初始化..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

$args_list = @("main.py", "--stock-code", $StockCode)

if ($CompanyName) { $args_list += @("--company-name", $CompanyName) }
if ($StartDate)     { $args_list += @("--start-date", $StartDate) }
if ($EndDate)       { $args_list += @("--end-date", $EndDate) }
if ($MaxPages -gt 0) { $args_list += @("--max-pages", $MaxPages) }
if ($Verbose)       { $args_list += "--verbose" }

.\.venv\Scripts\python @args_list
