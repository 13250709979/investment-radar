# PDF download + parse
# Usage: .\crawler\scripts\run_pdf.ps1 -CompanyCode 601012 -Limit 10

param(
    [string]$CompanyCode = "",
    [int]$Limit = 50,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not (Test-Path ".\.env")) {
    if (Test-Path ".\.env.example") {
        Copy-Item ".\.env.example" ".\.env"
        Write-Host "Created .env from .env.example" -ForegroundColor Yellow
    }
}

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "Creating venv..." -ForegroundColor Yellow
    python -m venv .venv
    & $Python -m pip install -r requirements.txt
}

$args = @("main_pdf.py", "--limit", "$Limit")
if ($CompanyCode) { $args += @("--company-code", $CompanyCode) }
if ($Verbose)     { $args += "--verbose" }

& $Python @args
