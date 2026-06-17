#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

function Invoke-Checked {
    param([scriptblock]$Command, [string]$ErrorMessage)
    & $Command
    if ($LASTEXITCODE -ne 0) { throw $ErrorMessage }
}

function Wait-Postgres {
    param([int]$MaxAttempts = 24)
    for ($i = 1; $i -le $MaxAttempts; $i++) {
        & .\venv\Scripts\python.exe -c @"
from sqlalchemy import create_engine, text
from config import DATABASE_URL
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text('SELECT 1'))
print('PostgreSQL ready')
"@
        if ($LASTEXITCODE -eq 0) { return }
        Write-Host "  Waiting for PostgreSQL ($i/$MaxAttempts)..."
        Start-Sleep -Seconds 5
    }
    throw "PostgreSQL not ready. Check: docker compose ps"
}

Write-Host "=== BoardGame GPT - Setup ===" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw @"
Python not found.
Install Python 3.12+ from https://www.python.org/downloads/
Important: check 'Add Python to PATH' during installation.
"@
}

$pyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "Python $pyVersion"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw @"
Docker not found.
Install Docker Desktop from https://www.docker.com/products/docker-desktop/
"@
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw @"
Docker Desktop is not running.
Open Docker Desktop, wait until it shows 'Running', then run setup again.
"@
}

if (-not (Test-Path "data\games.json")) {
    throw "Missing data\games.json. Make sure the full project was copied or cloned."
}

if (-not (Test-Path "venv")) {
    Write-Host "`n[1/6] Creating virtual environment..."
    Invoke-Checked { python -m venv venv } "Failed to create virtual environment."
} else {
    Write-Host "`n[1/6] Virtual environment already exists."
}

Write-Host "[2/6] Installing Python dependencies..."
Invoke-Checked { & .\venv\Scripts\python.exe -m pip install --upgrade pip } "Failed to upgrade pip."
Invoke-Checked { & .\venv\Scripts\python.exe -m pip install -r requirements.txt } "pip install failed."

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}

Write-Host "[3/6] Starting Docker (PostgreSQL + Ollama)..."
Invoke-Checked { docker compose up -d } "Failed to start Docker services."

Write-Host "[4/6] Waiting for PostgreSQL..."
Wait-Postgres

Write-Host "[5/6] Loading PostgreSQL data..."
Invoke-Checked { & .\venv\Scripts\python.exe ingest\load_postgres.py } "Failed to load PostgreSQL data."

Write-Host "[6/6] Building vectorstore (first run may take several minutes)..."
Invoke-Checked { & .\venv\Scripts\python.exe ingest\build_vectorstore.py } "Failed to build vectorstore."

Write-Host "`nPulling Ollama model (may take several minutes)..."
$ollamaId = docker compose ps -q ollama
if (-not $ollamaId) { throw "Ollama container not running." }
Invoke-Checked { docker exec $ollamaId ollama pull llama3.1:8b } "Failed to pull Ollama model."

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  Terminal 1: .\scripts\run-backend.ps1"
Write-Host "  Terminal 2: .\scripts\run-frontend.ps1"
Write-Host "  Browser:    http://localhost:8501"
