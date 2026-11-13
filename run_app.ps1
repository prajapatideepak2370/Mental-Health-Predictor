$projectDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    throw 'Python was not found on PATH. Install Python or add it to PATH, then run this script again.'
}

$backend = Start-Process -FilePath $python.Source -ArgumentList @(
    '-m'
    'uvicorn'
    'main:app'
    '--host'
    '127.0.0.1'
    '--port'
    '2200'
) -WorkingDirectory $projectDirectory -PassThru

$backendReady = $false
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    if ($backend.HasExited) {
        break
    }

    try {
        $health = Invoke-RestMethod -Uri 'http://127.0.0.1:2200/' -TimeoutSec 1
        if ($health.'Welcome to the Mental Health Prediction API!') {
            $backendReady = $true
            break
        }
    }
    catch [System.Net.WebException] {
        Start-Sleep -Seconds 1
    }
}

if (-not $backendReady) {
    throw 'The FastAPI backend did not become ready. Check the backend window for startup errors.'
}

Start-Process -FilePath $python.Source -ArgumentList @(
    '-m'
    'streamlit'
    'run'
    'App.py'
    '--server.address'
    '127.0.0.1'
    '--server.port'
    '8501'
) -WorkingDirectory $projectDirectory

Write-Host 'Backend:  http://127.0.0.1:2200'
Write-Host 'Frontend: http://127.0.0.1:8501'