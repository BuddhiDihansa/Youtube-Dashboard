Set-Location $PSScriptRoot

if (-not (Test-Path .venv\Scripts\python.exe)) {
    Write-Host "Virtual environment not found. Create it first, then install dependencies."
    exit 1
}

& .venv\Scripts\python.exe -m streamlit run app.py