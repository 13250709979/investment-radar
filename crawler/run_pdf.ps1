# 公告 PDF 下载解析 - 一键运行
# 用法: .\run_pdf.ps1 -CompanyCode 601012 -Limit 10

param(
    [string]$CompanyCode = "",

    [int]$Limit = 50,

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

$args_list = @("main_pdf.py", "--limit", $Limit)

if ($CompanyCode) { $args_list += @("--company-code", $CompanyCode) }
if ($Verbose)       { $args_list += "--verbose" }

.\.venv\Scripts\python @args_list
