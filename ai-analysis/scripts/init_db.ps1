# 初始化 ai_analysis 表
# 用法: .\ai-analysis\scripts\init_db.ps1

$ErrorActionPreference = "Stop"
$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$SqlFile = Join-Path $RootDir "backend\docs\sql\ai_analysis.sql"

if (-not (Test-Path $SqlFile)) {
    Write-Error "找不到建表脚本: $SqlFile"
}

Write-Host "执行建表 SQL: $SqlFile" -ForegroundColor Cyan
Get-Content $SqlFile | docker exec -i postgres psql -U postgres -d investment_radar
Write-Host "建表完成" -ForegroundColor Green
