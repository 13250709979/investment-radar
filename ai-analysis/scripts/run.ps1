# ?? AI ?? ? ????? ai-analysis/.env?????????
# ??: .\ai-analysis\scripts\run.ps1 -CompanyCode 601012 -Limit 5 [-Model google]

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
    if (-not (Test-Path ".\.env.example")) { Write-Error "?? .env / .env.example" }
    Copy-Item ".\.env.example" ".\.env"
    Write-Host "??? .env???? API_KEY ????" -ForegroundColor Yellow
    exit 1
}

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "???????..." -ForegroundColor Yellow
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
