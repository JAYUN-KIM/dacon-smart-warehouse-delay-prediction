Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = "C:\open\dacon-smart-warehouse-portfolio"
Set-Location $root

python .\scripts\update_daily_report.py

git add .
git commit -m "docs: update daily competition report"

try {
    git push
}
catch {
    Write-Host "Push skipped or failed. Check remote/auth configuration."
}

