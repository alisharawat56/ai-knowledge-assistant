
Write-Host "Setting up AI Knowledge Assistant..."

# Create virtual environment if it does not exist
if (-not (Test-Path ".\venv")) {
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Setup completed."
Write-Host "Next: make sure Ollama is running and download the required models."
