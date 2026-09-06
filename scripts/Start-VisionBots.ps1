# Start-VisionBots.ps1
# Encendido de una sola pasada de toda la plataforma VisionBots.
# Mantiene viva la VM de WSL (PostgreSQL + backend) y abre el frontend.

$ErrorActionPreference = "SilentlyContinue"

function Test-Api {
    try { $h = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/health" -TimeoutSec 5; return $h.status -eq "online" } catch { return $false }
}

Write-Host "== VisionBots: encendiendo entorno ==" -ForegroundColor Cyan

# 1) Arrancar la VM de WSL si está apagada y mantenerla viva
$keep = Get-CimInstance Win32_Process -Filter "Name='wsl.exe'" | Where-Object { $_.CommandLine -match "sleep 30" } | Select-Object -First 1
if (-not $keep) {
    Write-Host "Iniciando VM de WSL (keep-alive)..." -ForegroundColor Yellow
    Start-Process wscript.exe -ArgumentList "`"C:\Users\Duvan Altamar\Documents\ChatGPT\Vision-Box\VisionBots-App\scripts\VisionBots-KeepWSL.vbs`"" -WindowStyle Hidden
}

# 2) Esperar a que la VM levante
Start-Sleep -Seconds 6

# 3) Asegurar servicios dentro de la VM
wsl -d Ubuntu -u root -- sh -c "service postgresql start >/dev/null 2>&1; systemctl start visionbots-backend >/dev/null 2>&1; true"
Write-Host "Servicios PostgreSQL y backend iniciados." -ForegroundColor Green

# 4) Esperar a que el backend responda
$tries = 0
while (-not (Test-Api) -and $tries -lt 20) { Start-Sleep -Seconds 2; $tries++ }
if (Test-Api) {
    Write-Host "API lista en http://localhost:8000/api/v1" -ForegroundColor Green
} else {
    Write-Host "La API no respondió aún. Revisa: wsl -d Ubuntu -u root -- systemctl status visionbots-backend" -ForegroundColor Red
}

# 5) Abrir el frontend
Write-Host "Abriendo panel web..." -ForegroundColor Cyan
Start-Process "http://localhost:5173"