# Ejecutar VisionBots localmente

## Estado de las herramientas

El backend y el frontend ya están preparados y validados. PostgreSQL requiere
Docker Desktop, que en Windows necesita WSL 2.

En este equipo, WSL debe habilitarse desde una ventana de PowerShell abierta
como administrador. Ejecuta una vez:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Reinicia Windows. Después, abre PowerShell como administrador y ejecuta:

```powershell
wsl --install
```

Cuando WSL esté listo, instala y abre Docker Desktop con el backend WSL 2.
La guía oficial de Docker explica los requisitos y la instalación para Windows:
<https://docs.docker.com/desktop/setup/install/windows-install/>.

## Base de datos

Desde la raíz del proyecto, con Docker Desktop iniciado:

```powershell
docker compose up -d
```

La configuración de desarrollo crea una base `visionbots` en
`localhost:5432`. Las credenciales son solo para desarrollo y están en
`compose.yaml` y `backend/.env.example`.

## Backend

```powershell
cd backend
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abre <http://127.0.0.1:8000/docs> para usar la API. Sin `DATABASE_URL` en
`.env`, el backend usa SQLite local para poder desarrollar sin Docker. Con el
archivo `.env.example`, usa PostgreSQL.

## Frontend

En este equipo el acceso directo `npm` apunta a una ruta antigua. Usa el
ejecutable de la instalación oficial de Node:

```powershell
cd frontend
Copy-Item .env.example .env
& "C:\Program Files\nodejs\npm.cmd" install
& "C:\Program Files\nodejs\npm.cmd" run dev
```

Abre <http://localhost:5173>. El panel permite crear, buscar y archivar
objetos, y muestra el resumen del inventario.
