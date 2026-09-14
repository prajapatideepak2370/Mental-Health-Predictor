$projectDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

Start-Process powershell -ArgumentList @(
    '-NoExit'
    '-Command'
    "Set-Location -LiteralPath '$projectDirectory'; python -m uvicorn main:app --host 127.0.0.1 --port 2200"
)

Start-Process powershell -ArgumentList @(
    '-NoExit'
    '-Command'
    "Set-Location -LiteralPath '$projectDirectory'; python -m streamlit run App.py --server.address 127.0.0.1 --server.port 8501"
)

Write-Host 'Backend:  http://127.0.0.1:2200'
Write-Host 'Frontend: http://127.0.0.1:8501'