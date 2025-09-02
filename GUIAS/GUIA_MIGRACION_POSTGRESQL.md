# 🐘 Guía Completa de Migración a PostgreSQL

## 📋 Resumen de la Migración

Este documento describe la migración completa del sistema PQRSD de **SQLite** a **PostgreSQL**, incluyendo todos los cambios realizados, configuración necesaria y pasos para implementar el sistema en producción.

---

## 🎯 Objetivos de la Migración

### ✅ Ventajas Obtenidas
- **Escalabilidad**: Soporte para múltiples usuarios concurrentes
- **Rendimiento**: Índices optimizados y consultas más eficientes
- **Robustez**: Transacciones ACID completas y recuperación ante fallos
- **Funcionalidades**: Tipos de datos avanzados y funciones SQL empresariales
- **Seguridad**: Autenticación, autorización y encriptación de nivel empresarial
- **Mantenimiento**: Respaldos automáticos, replicación y monitoreo

### 📊 Comparación SQLite vs PostgreSQL

| Característica | SQLite | PostgreSQL |
|---|---|---|
| **Concurrencia** | Limitada (1 escritor) | ✅ Múltiples usuarios simultáneos |
| **Escalabilidad** | Archivos pequeños | ✅ Terabytes de datos |
| **Transacciones** | Básicas | ✅ ACID completas |
| **Índices** | Simples | ✅ Compuestos, parciales, funcionales |
| **Tipos de datos** | Limitados | ✅ JSON, Arrays, UUID, etc. |
| **Funciones** | Básicas | ✅ Agregaciones, ventanas, etc. |
| **Seguridad** | Archivo local | ✅ Roles, permisos, SSL |
| **Respaldos** | Copia de archivo | ✅ Automáticos, incrementales |

---

## 🔧 Archivos Modificados

### 1. **requirements.txt**
```diff
+ psycopg2-binary==2.9.9
+ python-dotenv==1.0.0
```
**Cambios**: Agregadas dependencias para PostgreSQL y manejo de variables de entorno.

### 2. **database.py** - Configuración Principal
**Cambios Principales**:
- ✅ Reemplazada configuración SQLite por PostgreSQL
- ✅ Agregado pool de conexiones para mejor rendimiento
- ✅ Implementadas variables de entorno para seguridad
- ✅ Mejorado manejo de errores y logging
- ✅ Agregadas funciones de conectividad y diagnóstico

### 3. **db_models.py** - Modelos de Datos
**Optimizaciones PostgreSQL**:
- ✅ Índices compuestos para consultas frecuentes
- ✅ Comentarios en tabla y columnas
- ✅ Tipos de datos optimizados
- ✅ Métodos mejorados con type hints

### 4. **init_db.py** - Inicialización
**Nuevas Funcionalidades**:
- ✅ Verificación de conectividad PostgreSQL
- ✅ Información detallada del servidor
- ✅ Datos de ejemplo más realistas
- ✅ Estadísticas avanzadas de la base de datos
- ✅ Opciones de línea de comandos mejoradas

### 5. **services.py** - Lógica de Negocio
**Actualizaciones**:
- ✅ Comentarios actualizados para PostgreSQL
- ✅ Documentación de ventajas implementadas
- ✅ Notas educativas sobre PostgreSQL

### 6. **.env.example** - Variables de Entorno
**Nuevo archivo** con configuración de ejemplo para PostgreSQL.

---

## 🚀 Instalación y Configuración

### 🐳 **OPCIÓN 1: Docker (RECOMENDADO PARA DESARROLLO)**

#### ✅ Ventajas de Docker:
- **Aislamiento completo** del sistema operativo
- **Misma versión** que en producción
- **Fácil de eliminar** cuando termines el proyecto
- **Portable** entre Windows, Mac y Linux
- **No contamina** tu máquina local

#### 📋 Prerrequisitos:
```bash
# Instalar Docker Desktop
# Windows/Mac: https://www.docker.com/products/docker-desktop
# Linux: sudo apt install docker.io docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

#### 🚀 Configuración Paso a Paso:

**1. Configurar variables de entorno:**
```bash
# Copiar configuración de Docker
cp .env.docker .env

# Editar si es necesario (opcional)
nano .env
```

**2. Iniciar PostgreSQL con Docker:**
```bash
# Iniciar solo PostgreSQL
docker-compose up -d postgres

# Verificar que esté corriendo
docker-compose ps

# Ver logs si hay problemas
docker-compose logs postgres
```

**3. (Opcional) Iniciar Adminer para interfaz web:**
```bash
# Iniciar con perfil de desarrollo
docker-compose --profile dev up -d

# Acceder a Adminer: http://localhost:8080
# Servidor: postgres
# Usuario: pqrsd_user
# Contraseña: desarrollo123
# Base de datos: pqrsd_sistema
```

**4. Verificar conectividad:**
```bash
# Desde tu aplicación Python
python init_db.py

# O conectar directamente al contenedor
docker exec -it pqrsd-postgres psql -U pqrsd_user -d pqrsd_sistema
```

#### 🛠️ Comandos Útiles de Docker:
```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra datos)
docker-compose down -v

# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f postgres

# Backup de la base de datos
docker exec pqrsd-postgres pg_dump -U pqrsd_user pqrsd_sistema > backup.sql

# Restaurar backup
docker exec -i pqrsd-postgres psql -U pqrsd_user -d pqrsd_sistema < backup.sql
```

---

### 🖥️ **OPCIÓN 2: Instalación Local (PRODUCCIÓN)**

#### Windows:
```bash
# Descargar desde: https://www.postgresql.org/download/windows/
# O usar Chocolatey:
choco install postgresql
```

#### macOS:
```bash
# Usando Homebrew:
brew install postgresql
brew services start postgresql
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 2: Configurar Base de Datos

```sql
-- Conectar como superusuario
sudo -u postgres psql

-- Crear base de datos
CREATE DATABASE pqrsd_sistema;

-- Crear usuario
CREATE USER pqrsd_user WITH PASSWORD 'tu_password_seguro';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE pqrsd_sistema TO pqrsd_user;

-- Salir
\q
```

### Paso 3: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus datos
nano .env
```

**Contenido del archivo .env**:
```env
# Configuración PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pqrsd_sistema
DB_USER=pqrsd_user
DB_PASSWORD=tu_password_seguro

# Configuración de aplicación
DEBUG=True
LOG_LEVEL=INFO
```

### Paso 4: Instalar Dependencias Python

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Inicializar Base de Datos

```bash
# Verificar conectividad
python init_db.py --check

# Crear tablas
python init_db.py --crear

# Agregar datos de ejemplo (opcional)
python init_db.py --datos

# Ver estado de la base de datos
python init_db.py --info
```

---

## 🔍 Verificación de la Migración

### 1. Verificar Conectividad
```bash
python init_db.py --check --verbose
```

### 2. Verificar Tablas Creadas
```sql
-- Conectar a PostgreSQL
psql -h localhost -U pqrsd_user -d pqrsd_sistema

-- Listar tablas
\dt

-- Ver estructura de tabla casos
\d casos

-- Ver índices
\di
```

### 3. Verificar Datos de Ejemplo
```sql
-- Contar registros
SELECT COUNT(*) FROM casos;

-- Ver casos por tipo
SELECT tipo, COUNT(*) FROM casos GROUP BY tipo;

-- Ver casos por estado
SELECT estado, COUNT(*) FROM casos GROUP BY estado;
```

### 4. Probar API
```bash
# Iniciar servidor
python main.py

# En otra terminal, probar endpoints
curl http://localhost:8000/casos
curl http://localhost:8000/estadisticas
```

---

## 📊 Optimizaciones Implementadas

### Índices Estratégicos
```sql
-- Índices automáticamente creados:
CREATE INDEX idx_caso_tipo_estado ON casos(tipo, estado);
CREATE INDEX idx_caso_fecha_estado ON casos(fecha_creacion, estado);
CREATE INDEX idx_caso_email_estado ON casos(email_solicitante, estado);
CREATE INDEX idx_caso_fecha_desc ON casos(fecha_creacion);
```

### Pool de Conexiones
- **pool_size**: 5 conexiones base
- **max_overflow**: 10 conexiones adicionales
- **pool_timeout**: 30 segundos
- **pool_recycle**: 1 hora

### Configuraciones de Rendimiento
```python
# En database.py
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False  # True para debugging SQL
)
```

---

## 🛡️ Seguridad

### Variables de Entorno
- ✅ Credenciales fuera del código fuente
- ✅ Archivo .env en .gitignore
- ✅ Ejemplo sin credenciales reales

### Conexión Segura
- ✅ Pool de conexiones controlado
- ✅ Timeouts configurados
- ✅ Manejo de errores robusto

### Recomendaciones Adicionales
```bash
# Configurar SSL en producción
DB_SSLMODE=require

# Usar contraseñas fuertes
DB_PASSWORD=contraseña_muy_segura_con_símbolos_123!

# Restringir acceso por IP en pg_hba.conf
host pqrsd_sistema pqrsd_user 192.168.1.0/24 md5
```

---

## 🚨 Solución de Problemas

### Error: "psycopg2 not found"
```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get install libpq-dev python3-dev

# Reinstalar psycopg2
pip uninstall psycopg2-binary
pip install psycopg2-binary
```

### Error: "Connection refused"
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Iniciar si está detenido
sudo systemctl start postgresql

# Verificar puerto
sudo netstat -tlnp | grep 5432
```

### Error: "Authentication failed"
```bash
# Verificar usuario y contraseña
psql -h localhost -U pqrsd_user -d pqrsd_sistema

# Resetear contraseña si es necesario
sudo -u postgres psql
ALTER USER pqrsd_user PASSWORD 'nueva_contraseña';
```

### Error: "Database does not exist"
```sql
-- Crear base de datos
sudo -u postgres createdb pqrsd_sistema

-- O desde psql
sudo -u postgres psql
CREATE DATABASE pqrsd_sistema;
```

---

## 📈 Monitoreo y Mantenimiento

### Consultas de Monitoreo
```sql
-- Actividad actual
SELECT * FROM pg_stat_activity WHERE datname = 'pqrsd_sistema';

-- Estadísticas de tablas
SELECT * FROM pg_stat_user_tables WHERE relname = 'casos';

-- Uso de índices
SELECT * FROM pg_stat_user_indexes WHERE relname = 'casos';

-- Tamaño de base de datos
SELECT pg_size_pretty(pg_database_size('pqrsd_sistema'));
```

### Respaldos Automáticos
```bash
# Script de respaldo diario
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/pqrsd"
mkdir -p $BACKUP_DIR

pg_dump -h localhost -U pqrsd_user pqrsd_sistema > \
  $BACKUP_DIR/pqrsd_backup_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/pqrsd_backup_$DATE.sql

# Eliminar respaldos antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

---

## 🎉 Próximos Pasos

### Mejoras Recomendadas
1. **Autenticación JWT** para la API
2. **Paginación** en listados de casos
3. **Búsqueda full-text** con PostgreSQL
4. **Auditoría** de cambios en casos
5. **Notificaciones** por email/SMS
6. **Dashboard** con métricas en tiempo real
7. **API de reportes** con filtros avanzados
8. **Integración** con sistemas externos

### Escalabilidad
- **Read replicas** para consultas
- **Particionamiento** de tablas grandes
- **Cache** con Redis
- **Load balancer** para múltiples instancias
- **Containerización** con Docker
- **Orquestación** con Kubernetes

---

## 📞 Soporte

Para problemas o preguntas sobre la migración:

1. **Revisar logs** de la aplicación
2. **Consultar documentación** de PostgreSQL
3. **Verificar configuración** de variables de entorno
4. **Probar conectividad** con `init_db.py --check`

---

**✅ Migración Completada Exitosamente**

El sistema PQRSD ahora utiliza PostgreSQL como base de datos principal, proporcionando mayor robustez, escalabilidad y funcionalidades empresariales para el manejo eficiente de Peticiones, Quejas, Reclamos, Sugerencias y Denuncias.