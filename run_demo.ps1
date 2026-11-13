
Write-Host "Starting AI Knowledge Assistant..."

# Activate virtual environment
if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Run .\setup.ps1 first."
    exit 1
}

.\venv\Scripts\Activate.ps1

# Check Ollama
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5 | Out-Null
    Write-Host "Ollama is running."
}
catch {
    Write-Host "Ollama is not running. Please start Ollama."
    exit 1
}

# Check required models
$modelList = ollama list | Out-String

if ($modelList -notmatch 'qwen3\.5:0\.8b') {
    Write-Host "Missing qwen3.5:0.8b"
    exit 1
}

if ($modelList -notmatch 'nomic-embed-text') {
    Write-Host "Missing nomic-embed-text"
    exit 1
}

Write-Host "Both models are available."

# Launch application
Write-Host "Launching Streamlit at http://localhost:8501"

python -m streamlit run app.py

Write-Host "Streamlit has stopped."
