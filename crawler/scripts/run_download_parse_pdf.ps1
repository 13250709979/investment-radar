# Download and parse announcement PDFs into DB
# Usage: .\crawler\scripts\run_download_parse_pdf.ps1 -CompanyCode 601888 -Limit 20

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

$args = @("download_parse_pdf.py", "--limit", "$Limit")
if ($CompanyCode) { $args += @("--company-code", $CompanyCode) }
if ($Verbose)     { $args += "--verbose" }

& $Python @args
