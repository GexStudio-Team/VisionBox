# Base de datos de VisionBox

La base de datos es **PostgreSQL 18** y corre dentro de **Ubuntu 26.04 (WSL 2)** como servicio systemd. En desarrollo el acceso se hace por loopback nativo (`127.0.0.1:5432`), lo que es totalmente estable en este equipo.

## Conexión

URL usada por el backend (en `backend/.env`):

```
postgresql+psycopg://visionbots:visionbots_dev@127.0.0.1:5432/visionbots?connect_timeout=5
```

| Parámetro | Valor |
| --- | --- |
| Motor | `postgresql+psycopg` (psycopg 3) |
| Base de datos | `visionbots` |
| Usuario | `visionbots` |
| Contraseña | `visionbots_dev` (**solo desarrollo**) |
| Puerto | `5432` |
| Tiempo de espera | `connect_timeout=5`: si la red falla, la conexión falla rápido en vez de colgarse |

## Pool de conexiones

Para que un corte de red no genere conexiones colgadas, `backend/app/db.py` configura:

- `pool_pre_ping=True`: valida la conexión antes de cada uso y la descarta si está muerta.
- `pool_recycle=120`: recicla conexiones cada 2 minutos.

## Esquema

El esquema se crea automáticamente al arrancar el backend (`Base.metadata.create_all`). Aún no hay migraciones versionadas (pendiente).

### Tabla `items` — catálogo e inventario

| Columna | Tipo | Notas |
| --- | --- | --- |
| `id` | integer | Clave primaria. |
| `name` | varchar(160) | Nombre del objeto (indexado). |
| `category` | varchar(80) \| null | Categoría (indexado). |
| `description` | text \| null | Descripción libre. |
| `quantity` | integer | Unidades (def. 1). |
| `location` | varchar(120) \| null | Ubicación física. |
| `status` | varchar(20) | `active` \| `archived` (indexado). |
| `image_url` | varchar(500) \| null | Referencia a imagen. |
| `created_at` | timestamptz | Se asigna en la base (`now()`). |
| `updated_at` | timestamptz | Se actualiza automáticamente al editar. |

### Tabla `item_events` — historial inmutable

| Columna | Tipo | Notas |
| --- | --- | --- |
| `id` | integer | Clave primaria. |
| `item_id` | integer | FK a `items.id` con `ON DELETE CASCADE` (indexado). |
| `action` | varchar(40) | `created`, `updated`, `archived` (indexado). |
| `detail` | text \| null | Descripción del evento. |
| `created_at` | timestamptz | Marca de tiempo. |

Los eventos se escriben, nunca se modifican ni se borran: son la pista de auditoría del sistema.

## Consultas útiles

```sql
-- Todo el inventario
select * from items order by updated_at desc;

-- Solo activos con su histograma de eventos
select i.id, i.name, count(e.id) as eventos
from items i
left join item_events e on e.item_id = i.id
where i.status = 'active'
group by i.id, i.name;
```

Desde Windows, ejecutar con WSL:

```powershell
wsl -d Ubuntu -u root -- PGPASSWORD=visionbots_dev psql -h 127.0.0.1 -U visionbots -d visionbots -c "select * from items;"
```

## Administración del servicio

```powershell
# Estado de PostgreSQL
wsl -d Ubuntu -u root -- systemctl status postgresql --no-pager

# Listar bases de datos (como el súper usuario)
wsl -d Ubuntu -u root -- su - postgres -c "psql -c '\l'"
```

## Modelo de datos futuro

El plan de producto define además: `users` (administradores), `boxes` y `compartments` (ubicaciones), `media_assets` (fotos/videos) y `detections` (resultados de la IA con revisión humana). Documentado en [`PRODUCT_FOUNDATION.md`](PRODUCT_FOUNDATION.md).

## Alternativa Docker

`compose.yaml` levanta PostgreSQL 17 con las mismas credenciales y el puerto `5432`. No es necesario para el funcionamiento actual.