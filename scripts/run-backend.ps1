#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup.ps1 first."
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Docker Desktop does not appear to be running. Start it before using the app."
}

& .\venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8080
