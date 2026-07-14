# 公告 AI 分析 - 一键运行
#
# 在 ai 目录内:
#   .\run.ps1 -CompanyCode 601012 -Limit 5
# 在项目根目录:
#   .\ai\run.ps1 -CompanyCode 601012 -Limit 5

param(
    [string]$CompanyCode = "",

    [int]$Limit = 20,

    [int]$Loops = 1,

    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Write-Host "工作目录: $ScriptDir" -ForegroundColor DarkGray

if (-not (Test-Path ".\.env")) {
    if (Test-Path ".\.env.example") {
        Copy-Item ".\.env.example" ".\.env"
        Write-Host "已从 .env.example 生成 .env，请先填写 API_KEY" -ForegroundColor Yellow
        exit 1
    }
    Write-Error "缺少 .env，请参考 .env.example 创建"
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "未找到虚拟环境，正在初始化..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

$args_list = @("main.py", "--limit", $Limit, "--loops", $Loops)

if ($CompanyCode) { $args_list += @("--company-code", $CompanyCode) }
if ($Verbose)       { $args_list += "--verbose" }

.\.venv\Scripts\python @args_list
