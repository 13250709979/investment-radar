# Announcement crawl
# Usage: .\crawler\scripts\run.ps1 -StockCode 601012 -CompanyName LonGi

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

$args = @("main.py", "--stock-code", $StockCode)
if ($CompanyName) { $args += @("--company-name", $CompanyName) }
if ($StartDate)   { $args += @("--start-date", $StartDate) }
if ($EndDate)     { $args += @("--end-date", $EndDate) }
if ($MaxPages -gt 0) { $args += @("--max-pages", $MaxPages) }
if ($Verbose)     { $args += "--verbose" }

& $Python @args
