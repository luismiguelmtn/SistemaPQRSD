# 🚀 Sistema PQRSD - Producción

Sistema de Peticiones, Quejas, Reclamos, Sugerencias y Denuncias desarrollado con **FastAPI** y **PostgreSQL** para entornos de producción.

## 📋 Descripción

Sistema robusto y escalable para gestionar casos PQRSD con:
- ✅ **API REST completa** con FastAPI
- ✅ **Base de datos PostgreSQL** para producción
- ✅ **Validaciones automáticas** con Pydantic
- ✅ **Documentación interactiva** con Swagger
- ✅ **Arquitectura escalable** y mantenible

## 🏗️ Estructura del Proyecto

```
pqrsd-eso/
├── main.py              # Configuración principal de FastAPI
├── routes.py            # Endpoints de la API
├── services.py          # Lógica de negocio y servicios
├── models.py            # Modelos Pydantic para validación
├── db_models.py         # Modelos SQLAlchemy para PostgreSQL
├── database.py          # Configuración de base de datos
├── enums.py             # Enumeraciones (TipoCaso, EstadoCaso)
├── init_db.py           # Script de inicialización de BD
├── setup_produccion.py  # Script de configuración automática
├── .env                 # Variables de entorno (NO incluir en git)
├── requirements.txt     # Dependencias del proyecto
├── GUIAS/              # Documentación técnica
│   ├── GUIA_MIGRACION_POSTGRESQL.md
│   ├── GUIA_BASE_DE_DATOS.md
│   ├── GUIA_ENDPOINTS.md
│   └── EJEMPLO_FLUJO_DATOS.md
└── README.md           # Este archivo
```

## 🚀 Instalación para Producción

### 📋 Prerrequisitos

- **Python 3.8+**
- **PostgreSQL 12+** instalado y corriendo
- **pip** (gestor de paquetes de Python)

### 🔧 Configuración Rápida

1. **Preparar el entorno**
   ```bash
   cd pqrsd-eso
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   source venv/bin/activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar PostgreSQL**
   ```sql
   -- Crear base de datos
   CREATE DATABASE pqrsd_sistema;
   
   -- Crear usuario (opcional)
   CREATE USER pqrsd_user WITH PASSWORD 'tu_contraseña_segura';
   GRANT ALL PRIVILEGES ON DATABASE pqrsd_sistema TO pqrsd_user;
   ```

4. **Configurar variables de entorno**
   ```bash
   # Editar archivo .env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=pqrsd_sistema
   DB_USER=tu_usuario_postgresql
   DB_PASSWORD=tu_contraseña_postgresql
   DB_ECHO=false
   APP_NAME=Sistema PQRSD
   APP_VERSION=1.0.0
   APP_DEBUG=false
   ```

5. **Configuración automática**
   ```bash
   python setup_produccion.py
   ```

## 🌐 Despliegue en Producción

### 🚀 Iniciar el servidor

```bash
# Desarrollo
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 📚 Documentación de la API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

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

### 📊 Base de Datos PostgreSQL

- **Enums nativos** para tipos y estados
- **Índices optimizados** para consultas rápidas
- **Validaciones a nivel de BD** para integridad
- **Timestamps automáticos** para auditoría

### 🔧 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos robusta para producción
- **SQLAlchemy**: ORM para manejo de base de datos
- **Pydantic**: Validación de datos automática
- **Uvicorn**: Servidor ASGI de alto rendimiento

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

- **GUIA_MIGRACION_POSTGRESQL.md**: Migración completa
- **GUIA_BASE_DE_DATOS.md**: Estructura de BD
- **GUIA_ENDPOINTS.md**: Documentación de API
- **EJEMPLO_FLUJO_DATOS.md**: Flujo de datos

## 🆘 Soporte

Para problemas o consultas:
1. Revisa los logs del servidor
2. Verifica la conexión a PostgreSQL
3. Consulta la documentación en `/docs`
4. Revisa las guías técnicas

---

**🚀 Sistema PQRSD listo para producción con PostgreSQL** 🎉
- **EN_PROCESO**: Caso en revisión
- **RESUELTO**: Caso con respuesta
- **CERRADO**: Caso finalizado

## Desarrollo

### Estructura de archivos

- `main.py`: Punto de entrada de la aplicación
- `routes.py`: Definición de rutas y endpoints
- `services.py`: Lógica de negocio y operaciones de datos
- `models.py`: Esquemas de datos con Pydantic
- `enums.py`: Enumeraciones para tipos y estados

### Desactivar entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

## Notas

- Este proyecto utiliza una "base de datos" en memoria para fines educativos
- En producción, se recomienda usar una base de datos real (PostgreSQL, MySQL, etc.)
- El entorno virtual (`venv/`) no debe incluirse en el control de versiones

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Python 3.8+**: Lenguaje de programación