# 🚀 Guía de Despliegue - Sistema PQRSD

Guía completa para desplegar el Sistema de Peticiones, Quejas, Reclamos, Sugerencias y Denuncias.

## 📋 Prerrequisitos

- Python 3.8 o superior
- Docker y Docker Compose
- Git (para clonar el repositorio)

## 🔧 Configuración del Entorno

### 1. Preparar el Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Instalar todas las dependencias del proyecto
pip install -r requirements.txt
```

## 🐘 Configuración de Base de Datos PostgreSQL

### 3. Configurar Variables de Entorno

El archivo `.env` ya está configurado con valores por defecto para desarrollo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pqrsd_sistema
DB_USER=pqrsd_user
DB_PASSWORD=desarrollo123
```

### 4. Desplegar PostgreSQL con Docker

```bash
# Iniciar contenedor de PostgreSQL
docker compose up -d postgres

# Verificar que el contenedor esté ejecutándose
docker compose ps
```

### 5. Inicializar Base de Datos

```bash
# Crear tablas y estructura de la base de datos
python init_db.py

# Opcional: Crear datos de ejemplo
python init_db.py --sample-data
```

## 🌐 Ejecutar la Aplicación

### 6. Iniciar el Servidor de Desarrollo

```bash
# Iniciar servidor con recarga automática
uvicorn main:app --reload

# O usando python directamente
python -m uvicorn main:app --reload
```

### 7. Verificar el Despliegue

La aplicación estará disponible en:

- **API Principal:** http://127.0.0.1:8000
- **Documentación Swagger:** http://127.0.0.1:8000/docs
- **Documentación ReDoc:** http://127.0.0.1:8000/redoc

## 🧪 Verificación del Sistema

### Probar Endpoints Principales

```bash
# Listar casos (debe devolver [])
curl http://127.0.0.1:8000/casos/

# Crear un caso de prueba
curl -X POST "http://127.0.0.1:8000/casos/" \
     -H "Content-Type: application/json" \
     -d '{
       "tipo": "peticion",
       "asunto": "Solicitud de información",
       "descripcion": "Prueba del sistema",
       "nombre_solicitante": "Usuario Prueba",
       "email_solicitante": "prueba@email.com",
       "telefono_solicitante": "1234567890"
     }'

# Ver estadísticas
curl http://127.0.0.1:8000/estadisticas/
```

## 🛠️ Comandos Útiles

### Gestión de Docker

```bash
# Ver logs de PostgreSQL
docker compose logs postgres

# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Limpiar volúmenes (⚠️ elimina datos)
docker compose down -v
```

### Gestión de Base de Datos

```bash
# Resetear base de datos completamente
python init_db.py --reset

# Verificar estado de la base de datos
python init_db.py --check

# Ver información detallada
python init_db.py --info
```

## 🔍 Solución de Problemas

### Error: "relation 'casos' does not exist"

```bash
# Ejecutar inicialización de base de datos
python init_db.py
```

### Error de conexión a PostgreSQL

```bash
# Verificar que Docker esté ejecutándose
docker compose ps

# Reiniciar contenedor de PostgreSQL
docker compose restart postgres
```

### Puerto 8000 en uso

```bash
# Usar puerto diferente
uvicorn main:app --reload --port 8001
```

## 📁 Estructura del Proyecto

```
pqrsd/
├── main.py              # Configuración principal FastAPI
├── routes.py            # Endpoints de la API
├── services.py          # Lógica de negocio
├── models.py            # Modelos Pydantic
├── db_models.py         # Modelos SQLAlchemy
├── database.py          # Configuración PostgreSQL
├── init_db.py           # Script inicialización BD
├── requirements.txt     # Dependencias Python
├── docker-compose.yml   # Configuración Docker
├── .env                 # Variables de entorno
└── GUIAS/              # Documentación adicional
```

## ✅ Lista de Verificación

- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] PostgreSQL ejecutándose en Docker
- [ ] Base de datos inicializada
- [ ] Servidor FastAPI ejecutándose
- [ ] Endpoints respondiendo correctamente
- [ ] Documentación accesible en /docs

---

**¡Sistema PQRSD listo para usar!** 🎉
