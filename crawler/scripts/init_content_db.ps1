# 初始化 announcement_content 表
# 在项目根目录执行: .\crawler\scripts\init_content_db.ps1

$ErrorActionPreference = "Stop"
$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$SqlFile = Join-Path $RootDir "backend\docs\sql\announcement_content.sql"

if (-not (Test-Path $SqlFile)) {
    Write-Error "找不到建表脚本: $SqlFile"
}

Write-Host "执行建表 SQL: $SqlFile" -ForegroundColor Cyan
Get-Content $SqlFile | docker exec -i postgres psql -U postgres -d investment_radar
Write-Host "建表完成" -ForegroundColor Green
