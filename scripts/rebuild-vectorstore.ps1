#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup.ps1 first."
}

Write-Host "Rebuilding vectorstore (rulebooks, reviews, games.json)..." -ForegroundColor Cyan
& .\venv\Scripts\python.exe ingest\build_vectorstore.py
if ($LASTEXITCODE -ne 0) {
    throw "Vectorstore rebuild failed. If the error mentions cryptography, run: .\venv\Scripts\python.exe -m pip install cryptography"
}

Write-Host "Done. Restart the backend if it is running." -ForegroundColor Green
