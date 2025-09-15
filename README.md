# 🚀 Sistema PQRSD

Sistema de **Peticiones, Quejas, Reclamos, Sugerencias y Denuncias** desarrollado con **FastAPI** y **PostgreSQL**.

## 📋 Descripción

Sistema robusto y escalable para gestionar casos PQRSD con:
- ✅ **API REST completa** con FastAPI y documentación automática
- ✅ **Base de datos PostgreSQL** con Docker para desarrollo y producción
- ✅ **Numeración inteligente** con formato TIPO-AÑO-NÚMERO (ej: PET-2025-0001)
- ✅ **Validaciones automáticas** con Pydantic y SQLAlchemy
- ✅ **Documentación interactiva** con Swagger UI y ReDoc
- ✅ **Arquitectura escalable** y mantenible con separación de responsabilidades
- ✅ **Contenedores Docker** para fácil despliegue
- ✅ **Scripts de inicialización** automatizados

## 🏗️ Estructura del Proyecto

```
pqrsd/
├── main.py              # Configuración principal de FastAPI
├── routes.py            # Endpoints de la API REST
├── services.py          # Lógica de negocio y servicios
├── models.py            # Modelos Pydantic para validación
├── db_models.py         # Modelos SQLAlchemy para PostgreSQL
├── app/
│   ├── core/
│   │   └── database.py  # Configuración de conexión PostgreSQL
│   └── migrations/      # Migraciones de base de datos con Alembic
├── enums.py             # Enumeraciones (TipoCaso, EstadoCaso)
├── alembic.ini          # Configuración de Alembic (migraciones)

├── docker-compose.yml   # Configuración de Docker para PostgreSQL
├── .env                 # Variables de entorno (NO incluir en git)
├── .env.docker          # Variables para Docker
├── requirements.txt     # Dependencias del proyecto
├── GUIAS/              # Documentación técnica completa
│   ├── GUIA_INSTALACION.md
│   ├── GUIA_BASE_DE_DATOS.md
│   ├── GUIA_ENDPOINTS.md
│   └── EJEMPLO_FLUJO_DATOS.md
└── README.md           # Este archivo
```

## 🚀 Instalación y Configuración

### 📋 Prerrequisitos

- **Python 3.8+**
- **Docker y Docker Compose** (recomendado)
- **Git** para clonar el repositorio

### 🐳 Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd pqrsd
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar archivo de ejemplo
   cp .env.docker .env
   
   # Editar .env si es necesario
   # Las configuraciones por defecto funcionan con Docker
   ```

5. **Iniciar PostgreSQL con Docker**
   ```bash
   docker compose up -d
   ```

6. **Inicializar la base de datos** 🗄️
   
   **⚠️ IMPORTANTE**: Si es la primera vez que clonas el proyecto o tienes una base de datos vacía, DEBES ejecutar estos comandos:
   
   ```bash
   # 1. Aplicar migraciones (crear todas las tablas)
   alembic upgrade head
   
   # 2. Opcional: Cargar datos de ejemplo para pruebas
   python tests/fixtures/datos_ejemplo.py
   ```
   
   **🔰 Para programadores nuevos en Alembic:**
   - `alembic upgrade head` crea TODAS las tablas en tu base de datos vacía
   - Es como ejecutar todos los CREATE TABLE automáticamente
   - SIEMPRE ejecuta este comando en un proyecto nuevo
   - Si no lo haces, tendrás errores de "tabla no existe"

### 🔧 Instalación Manual (Sin Docker)

1. **Instalar PostgreSQL 12+** en tu sistema
2. **Crear base de datos**
   ```sql
   CREATE DATABASE pqrsd;
   CREATE USER pqrsd_user WITH PASSWORD 'tu_contraseña';
   GRANT ALL PRIVILEGES ON DATABASE pqrsd TO pqrsd_user;
   ```
3. **Configurar .env** con tus credenciales
4. **Seguir pasos 2-6** de la instalación con Docker

## 🚀 Ejecutar el Sistema

### 🌐 Iniciar el servidor

```bash
# Desarrollo (con recarga automática)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción (múltiples workers)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 📚 Documentación de la API

Una vez iniciado el servidor, accede a:

- **🎯 Swagger UI**: http://localhost:8000/docs
- **📖 ReDoc**: http://localhost:8000/redoc
- **📄 OpenAPI JSON**: http://localhost:8000/openapi.json

### 🛠️ Comandos Útiles

```bash
# Verificar estado de migraciones
alembic current

# Ver historial de migraciones
alembic history

# Aplicar migraciones
alembic upgrade head

# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Revertir migración
alembic downgrade -1

# Ver logs de Docker
docker compose logs postgres

# Parar PostgreSQL
docker compose down
```

## 🗄️ Sistema de Migraciones con Alembic

**🔰 ¿Qué es Alembic?** Es una herramienta que gestiona cambios en la base de datos de forma controlada y versionada.

**🤔 ¿Por qué usamos Alembic?** Imagina que trabajas en equipo y cada uno tiene su propia base de datos. Alembic asegura que todos tengan exactamente las mismas tablas y estructura.

### ✅ Ventajas de Alembic
- **Versionado**: Cada cambio queda registrado con un ID único
- **Reversibilidad**: Puedes aplicar y revertir cambios
- **Sincronización**: Mantiene la BD idéntica entre entornos
- **Seguridad**: Usa variables de entorno para credenciales

### 🚀 Comandos Esenciales para Principiantes

```bash
# 🆕 PROYECTO NUEVO: Crear todas las tablas (OBLIGATORIO)
alembic upgrade head

# 📊 Ver qué versión tienes actualmente
alembic current

# 📜 Ver historial de cambios
alembic history

# 🔄 Actualizar a la última versión (cuando hay cambios nuevos)
alembic upgrade head
```

### 🛠️ Comandos Avanzados (Para desarrolladores)

```bash
# Crear migración después de modificar modelos
alembic revision --autogenerate -m "Agregar tabla usuarios"

# Ver historial completo con detalles
alembic history --verbose

# Revertir a versión anterior
alembic downgrade -1
```

### 🆘 Errores Comunes y Soluciones

**❌ Error: "relation 'casos' does not exist"**
```bash
# Solución: Ejecutar migraciones
alembic upgrade head
```

**❌ Error: "Target database is not up to date"**
```bash
# Solución: Actualizar base de datos
alembic upgrade head
```

### 🆕 ¿Acabas de clonar el proyecto? (Guía para principiantes)

**Situación**: Clonaste el proyecto en tu PC y tienes una base de datos completamente vacía.

**✅ Pasos obligatorios:**

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar PostgreSQL**
   ```bash
   docker compose up -d
   ```

3. **🚨 PASO CRÍTICO: Crear todas las tablas**
   ```bash
   alembic upgrade head
   ```
   
   **¿Qué hace este comando?**
   - Crea TODAS las tablas necesarias (casos, etc.)
   - Es como ejecutar todos los CREATE TABLE automáticamente
   - Sin esto, tu aplicación NO funcionará

4. **Verificar que funcionó**
   ```bash
   alembic current
   # Debe mostrar algo como: "abc123def456 (head)"
   ```

5. **Opcional: Agregar datos de prueba**
   ```bash
   python tests/fixtures/datos_ejemplo.py
   ```

**🎉 ¡Listo!** Ahora puedes ejecutar `python -m uvicorn main:app --reload`

### 📖 Documentación Completa
Para más detalles, consulta: **[docs/GUIA_ALEMBIC.md](docs/GUIA_ALEMBIC.md)**

## 🔗 Endpoints Principales

### 📋 Casos PQRSD

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/casos/` | Crear nuevo caso |
| `GET` | `/casos/` | Listar casos (con filtros) |
| `GET` | `/casos/{caso_id}` | Obtener caso por ID |
| `GET` | `/casos/numero/{numero_caso}` | Obtener caso por número |
| `PUT` | `/casos/{caso_id}` | Actualizar caso |

### 📊 Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/estadisticas/` | Estadísticas del sistema |

## 💡 Ejemplos de Uso

### Crear un nuevo caso

```bash
curl -X POST "http://localhost:8000/casos/" \
     -H "Content-Type: application/json" \
     -d '{
       "tipo": "peticion",
       "asunto": "Solicitud de información",
       "descripcion": "Necesito información sobre horarios de atención",
       "nombre_solicitante": "Juan Pérez",
       "email_solicitante": "juan@email.com",
       "telefono_solicitante": "3001234567"
     }'
```

**Respuesta:**
```json
{
  "id": 1,
  "numero_caso": 1,
  "anio": 2025,
  "numero_caso_formateado": "PET-2025-0001",
  "tipo": "peticion",
  "estado": "recibido",
  "asunto": "Solicitud de información",
  ...
}
```

### Listar casos con filtros

```bash
# Todos los casos
curl "http://localhost:8000/casos/"

# Solo peticiones
curl "http://localhost:8000/casos/?tipo=peticion"

# Solo casos pendientes
curl "http://localhost:8000/casos/?estado=recibido"
```

### Ver estadísticas

```bash
curl "http://localhost:8000/estadisticas/"
```

## 🏗️ Arquitectura del Sistema

### 🗄️ Base de Datos PostgreSQL

- **Numeración optimizada** con campos separados (numero_caso, anio, tipo)
- **Enums nativos** para tipos y estados
- **Índices compuestos** para consultas rápidas por tipo, año y número
- **Validaciones a nivel de BD** para integridad
- **Timestamps automáticos** para auditoría
- **Formato legible** generado automáticamente (PET-2025-0001)

### 🔧 Tecnologías Utilizadas

- **🚀 FastAPI**: Framework web moderno y rápido para APIs
- **🐘 PostgreSQL**: Base de datos robusta para producción
- **🔗 SQLAlchemy**: ORM avanzado para manejo de base de datos
- **✅ Pydantic**: Validación de datos automática y serialización
- **⚡ Uvicorn**: Servidor ASGI de alto rendimiento
- **🐳 Docker**: Contenedores para PostgreSQL
- **📊 Enums**: Tipos de datos nativos de PostgreSQL

## 🔒 Configuración de Producción

### 🌐 Proxy Reverso (Nginx)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 🔐 HTTPS con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com
```

### 📊 Monitoreo y Logs

```bash
# Ver logs en tiempo real
tail -f /var/log/nginx/access.log

# Monitorear procesos
ps aux | grep uvicorn

# Verificar conexiones PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## 🛡️ Seguridad

- ✅ **Variables de entorno** para credenciales
- ✅ **Validación de entrada** con Pydantic
- ✅ **Conexiones seguras** a PostgreSQL
- ✅ **CORS configurado** para APIs
- ✅ **Rate limiting** recomendado

## 📚 Documentación Adicional

Consulta la carpeta `GUIAS/` para documentación detallada:

- **📋 GUIA_INSTALACION.md**: Guía completa de instalación y configuración
- **🗄️ GUIA_BASE_DE_DATOS.md**: Estructura y modelos de PostgreSQL
- **🔗 GUIA_ENDPOINTS.md**: Documentación completa de la API
- **📊 EJEMPLO_FLUJO_DATOS.md**: Flujo de datos y casos de uso

## 🆘 Solución de Problemas

### 🔍 Problemas Comunes

**Error de conexión a PostgreSQL:**
```bash
# Verificar que Docker esté ejecutándose
docker compose ps

# Reiniciar PostgreSQL
docker compose restart postgres

# Verificar logs
docker compose logs postgres
```

**Error "duplicate key value violates unique constraint":**
- El número de caso ya existe
- Usar un número diferente o verificar casos existentes
- Verificar casos existentes con la API en `/casos/`

**Puerto 8000 ocupado:**
```bash
# Usar otro puerto
python -m uvicorn main:app --reload --port 8001
```

### 📞 Soporte

Para problemas o consultas:
1. 🔍 Revisa los logs del servidor y Docker
2. 🔗 Verifica la conexión a PostgreSQL con `--check`
3. 📖 Consulta la documentación en `/docs`
4. 📚 Revisa las guías técnicas en `GUIAS/`

## 🎯 Estados de Casos PQRSD

- **📥 RECIBIDO**: Caso recién creado
- **⏳ EN_PROCESO**: Caso en revisión
- **✅ RESUELTO**: Caso con respuesta
- **🔒 CERRADO**: Caso finalizado

---

**🚀 Sistema PQRSD - Listo para producción con PostgreSQL** 🎉