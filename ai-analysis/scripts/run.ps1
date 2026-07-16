# 公告 AI 分析 — 配置全部在 ai-analysis/.env，本脚本只负责启动
# 用法: .\ai-analysis\scripts\run.ps1 -CompanyCode 601012 -Limit 5 [-Model google]

param(
    [string]$CompanyCode = "",
    [string]$Model = "",
    [int]$Limit = 20,
    [int]$Loops = 1,
    [switch]$ListModels,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$AiRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $AiRoot

if (-not (Test-Path ".\.env")) {
    if (-not (Test-Path ".\.env.example")) { Write-Error "缺少 .env / .env.example" }
    Copy-Item ".\.env.example" ".\.env"
    Write-Host "已生成 .env，请填写 API_KEY 后再运行" -ForegroundColor Yellow
    exit 1
}

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "初始化虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    & $Python -m pip install -r requirements.txt
}

$args = @("main.py")
if ($ListModels) { & $Python @($args + "--list-models"); exit $LASTEXITCODE }

$args += @("--limit", "$Limit", "--loops", "$Loops")
if ($CompanyCode) { $args += @("--company-code", $CompanyCode) }
if ($Model)       { $args += @("--model", $Model) }
if ($Verbose)     { $args += "--verbose" }

& $Python @args
