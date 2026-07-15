# 公告 AI 分析
# 用法: .\ai\scripts\run.ps1 -CompanyCode 601012 -Limit 5 [-Model google]

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
    if (Test-Path ".\.env.example") {
        Copy-Item ".\.env.example" ".\.env"
        Write-Host "已生成 .env，请填写对应模型的 API_KEY" -ForegroundColor Yellow
        exit 1
    }
    Write-Error "缺少 .env，请参考 .env.example"
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "初始化虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
}

$pyArgs = @("main.py")
if ($ListModels) {
    .\.venv\Scripts\python @($pyArgs + "--list-models")
    exit $LASTEXITCODE
}

$pyArgs += @("--limit", $Limit, "--loops", $Loops)
if ($CompanyCode) { $pyArgs += @("--company-code", $CompanyCode) }
if ($Model)       { $pyArgs += @("--model", $Model) }
if ($Verbose)     { $pyArgs += "--verbose" }

.\.venv\Scripts\python @pyArgs
