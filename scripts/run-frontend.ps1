#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup.ps1 first."
}

& .\venv\Scripts\python.exe -m streamlit run frontend\app.py
