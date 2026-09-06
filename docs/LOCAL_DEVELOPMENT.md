# Ejecutar VisionBots localmente

## Arquitectura en este equipo

El backend (FastAPI) y PostgreSQL corren **dentro de Ubuntu en WSL 2**. El
frontend (React + Vite) corre en Windows y se conecta al backend en
`http://localhost:8000`.

Razón: las conexiones TCP persistentes entre Windows y WSL son inestables en
este equipo, así que llevamos la base de datos y la API al mismo entorno Linux;
allí el acceso a PostgreSQL es por loopback nativo y es 100% estable.

## Estado actual (instalado y validado)

| Componente | Dónde | Estado |
| --- | --- | --- |
| WSL 2 + Ubuntu 26.04 | Windows | Instalado |
| PostgreSQL 18 | `wsl` (Ubuntu) | Instalado, base `visionbots`, arranca solo |
| Backend FastAPI | `wsl` (Ubuntu) | Servicio `visionbots-backend`, arranca solo |
| API | `http://localhost:8000/api/v1` | Online |
| Frontend React | Windows | Compila con `npm run build` |
| Keep-alive WSL | Windows (carpeta Inicio) | Mantiene la VM encendida |

Tanto PostgreSQL como el backend quedaron habilitados como servicios de
systemd, por lo que arrancan automáticamente al encender la VM. Un script de
Inicio de Windows (`VisionBots-KeepWSL.cmd`) mantiene viva la VM de WSL
abriendo una sesión persistente, así la API sigue disponible aunque no haya
terminales abiertas.

## Iniciar todo con un solo clic

Hay un script que levanta la VM, asegura los servicios y abre el panel:

```powershell
& "C:\Users\Duvan Altamar\Documents\ChatGPT\Vision-Box\VisionBots-App\scripts\Start-VisionBots.ps1"
```

Alternativa manual si algo falló:

```powershell
wsl -d Ubuntu -u root -- sh -c "service postgresql start; systemctl start visionbots-backend"
```

## Base de datos PostgreSQL

Se creó una base `visionbots` y un usuario `visionbots` con la contraseña
`visionbots_dev` (solo desarrollo). Credenciales en `backend/.env`.

Para ejecutar SQL directamente:

```powershell
wsl -d Ubuntu -u root -- su - postgres -c "psql -c '\l'"
```

## Backend

El código vive en el repo (carpeta `backend`) y el entorno Python en
`/opt/visionbots/venv` dentro de Ubuntu. La API corre en `0.0.0.0:8000`.

- OpenAPI/Swagger: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/v1/health>

### Modificar el backend y reiniciarlo

```powershell
wsl -d Ubuntu -u root -- systemctl restart visionbots-backend
```

### Ejecutar el backend en primer plano (depuración)

```powershell
wsl -d Ubuntu -u root -- sh -c "cd '/mnt/c/Users/Duvan Altamar/Documents/ChatGPT/Vision-Box/VisionBots-App/backend' && /opt/visionbots/venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
```

Con `--reload` reinicia solo al editar código.

## Frontend

Depende de Node.js (instalado oficialmente). El archivo `.env` del frontend
puede indicar `VITE_API_URL`; por defecto usa `http://localhost:8000/api/v1`.

```powershell
cd frontend
& "C:\Program Files\nodejs\npm.cmd" install
& "C:\Program Files\nodejs\npm.cmd" run dev
```

Abre <http://localhost:5173>. El panel permite crear, buscar y archivar
objetos, y muestra el resumen del inventario.

## Docker (alternativa futura)

La configuración `compose.yaml` levanta PostgreSQL 17 con las mismas
credenciales y el puerto `5432`. Se puede usar cuando Docker Desktop esté
instalado; no es necesario para el funcionamiento actual.