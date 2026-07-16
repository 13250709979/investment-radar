# ??? ai_analysis ?
# ??: .\ai-analysis\scripts\init_db.ps1

$ErrorActionPreference = "Stop"
$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$SqlFile = Join-Path $RootDir "backend\docs\sql\ai_analysis.sql"

if (-not (Test-Path $SqlFile)) {
    Write-Error "???????: $SqlFile"
}

Write-Host "???? SQL: $SqlFile" -ForegroundColor Cyan
Get-Content $SqlFile | docker exec -i postgres psql -U postgres -d investment_radar
Write-Host "????" -ForegroundColor Green
