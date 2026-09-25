
# Create the virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    py -3.11 -m venv venv

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment."
        exit 1
    }
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!"
Write-Host "Python version:"
python --version

