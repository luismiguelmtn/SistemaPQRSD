# 🚀 Guía de Instalación y Puesta en Marcha - Sistema PQRSD

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8+** - [Descargar aquí](https://www.python.org/downloads/)
- **Docker Desktop** - [Descargar aquí](https://www.docker.com/products/docker-desktop/)
- **Git** (opcional) - Para clonar el repositorio

---

## 🛠️ Instalación Paso a Paso

### 1️⃣ **Crear Entorno Virtual**
```bash
python -m venv venv
```
**¿Qué hace?** Crea un entorno virtual aislado para las dependencias del proyecto.

---

### 2️⃣ **Activar Entorno Virtual**
```powershell
.\venv\Scripts\Activate.ps1
```
**¿Qué hace?** Activa el entorno virtual. Verás `(venv)` al inicio de tu prompt.

**💡 Nota:** Si tienes problemas de permisos en PowerShell, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 3️⃣ **Instalar Dependencias**
```bash
pip install -r requirements.txt
```
**¿Qué hace?** Instala todas las librerías necesarias (FastAPI, SQLAlchemy, psycopg2, etc.).

---

### 4️⃣ **Configurar Variables de Entorno**

1. **Copia el archivo de ejemplo:**
   ```bash
   copy .env.example .env
   ```

2. **Edita el archivo `.env`** con tus configuraciones:
   ```env
   # Base de datos PostgreSQL
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=pqrsd_db
   DB_USER=pqrsd_user
   DB_PASSWORD=pqrsd_password
   
   # Configuración de la aplicación
   SECRET_KEY=tu_clave_secreta_muy_segura_aqui
   DEBUG=True
   ```

---

### 5️⃣ **Iniciar Base de Datos (PostgreSQL)**
```bash
docker compose up
```
**¿Qué hace?** 
- Descarga e inicia un contenedor PostgreSQL
- Crea automáticamente la base de datos `pqrsd_db`
- Configura usuario y contraseña según `.env`

**💡 Tip:** Usa `docker compose up -d` para ejecutar en segundo plano.

---

### 6️⃣ **Inicializar Base de Datos**
```bash
alembic upgrade head
```
**¿Qué hace?** 
- Aplica todas las migraciones de Alembic
- Crea todas las tablas necesarias
- Configura índices y relaciones de forma versionada

---

### 7️⃣ **Cargar Datos de Ejemplo (Opcional)**

**⚠️ Prerrequisitos antes de cargar datos:**
1. ✅ PostgreSQL debe estar ejecutándose
2. ✅ Las migraciones deben estar aplicadas
3. ✅ El entorno virtual debe estar activado

**Verificar prerrequisitos:**
```bash
# 1. Verificar que PostgreSQL esté corriendo
docker compose ps
# Debe mostrar el contenedor 'postgres' como 'Up'

# 2. Verificar migraciones aplicadas
alembic current
# Debe mostrar el ID de la migración actual

# 3. Verificar entorno virtual (debe mostrar la ruta del proyecto)
echo $VIRTUAL_ENV  # Linux/Mac
echo $env:VIRTUAL_ENV  # Windows PowerShell
```

**Cargar datos de ejemplo:**
```bash
python -m tests.fixtures.insertar_casos_ejemplo
```

**Opciones de carga:**
```bash
# Cargar 100 casos (por defecto)
python -m tests.fixtures.insertar_casos_ejemplo

# Cargar cantidad específica
python -m tests.fixtures.insertar_casos_ejemplo 50
python -m tests.fixtures.insertar_casos_ejemplo 500
```

**¿Qué hace?** 
- Inserta datos de prueba realistas
- Crea casos PQRSD de ejemplo con numeración automática (PET-2025-0001, QUE-2025-0001, etc.)
- Útil para testing, desarrollo y demostración
- Incluye casos en diferentes estados (recibido, en proceso, resuelto, cerrado)
- Demuestra el sistema de numeración inteligente por tipo y año

**Verificar que los datos se cargaron correctamente:**
```bash
# Opción 1: Usando curl (requiere que el servidor esté corriendo)
curl "http://localhost:8000/casos/" | jq 'length'

# Opción 2: Usando Python directamente
python -c "from app.services.caso import obtener_todos_los_casos; print(f'Total casos insertados: {len(obtener_todos_los_casos())}')"

# Opción 3: Usando psql (si tienes PostgreSQL client instalado)
psql -h localhost -U pqrsd_user -d pqrsd_db -c "SELECT COUNT(*) as total_casos FROM casos;"
```

---

### 8️⃣ **Iniciar Servidor de Desarrollo**
```bash
uvicorn main:app --host localhost --port 8000 --reload
```
**¿Qué hace?** 
- Inicia el servidor FastAPI
- Habilita recarga automática en desarrollo
- Disponible en: http://localhost:8000

---

## 🌐 Acceso al Sistema

### **Interfaz Principal**
- **URL:** http://localhost:8000
- **Descripción:** Interfaz web del sistema PQRSD

### **Documentación API**
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### **Endpoints Principales**
- **Estadísticas:** http://localhost:8000/estadisticas/
- **Casos:** http://localhost:8000/casos/
- **Crear Caso:** http://localhost:8000/casos/ (POST)
- **Buscar por Número:** http://localhost:8000/casos/numero/{numero_formateado}

---

## 🔧 Comandos Útiles

### **Verificar Estado de Migraciones**
```bash
alembic current
```

### **Ver Historial de Migraciones**
```bash
alembic history
```

### **Crear Nueva Migración**
```bash
alembic revision --autogenerate -m "descripción del cambio"
```

### **Revertir Migración**
```bash
alembic downgrade -1
```

### **Verificar Conectividad a PostgreSQL**
```bash
docker compose exec postgres psql -U pqrsd_user -d pqrsd_db -c "SELECT version();"
```

### **Parar Docker**
```bash
docker compose down
```

### **Ver Contenedores Activos**
```bash
docker ps
```

---

## 🐳 Docker Compose y Gestión de Volúmenes

### **🔍 Diferencia Crítica: Preservar vs Eliminar Datos**

#### ✅ **Comando SEGURO** (Preserva datos)
```bash
docker compose down
```
**¿Qué hace?**
- ✅ Detiene los contenedores
- ✅ Elimina los contenedores
- ✅ Elimina las redes creadas
- ✅ **PRESERVA los volúmenes** (¡tus datos están seguros!)

**Resultado:** Los datos de PostgreSQL se mantienen intactos.

#### ❌ **Comando PELIGROSO** (Elimina datos)
```bash
docker compose down -v
```
**¿Qué hace?**
- ❌ Detiene los contenedores
- ❌ Elimina los contenedores
- ❌ Elimina las redes creadas
- ❌ **ELIMINA los volúmenes** (¡se pierden TODOS los datos!)

**Resultado:** Los datos de PostgreSQL se eliminan completamente.

### **🔄 Flujo de Trabajo Seguro**

#### Para reiniciar servicios manteniendo datos:
```bash
# 1. Detener servicios (datos seguros)
docker compose down

# 2. Volver a iniciar servicios
docker compose up -d

# ✅ Resultado: Mismos datos, contenedores frescos
```

#### Para verificar que los datos se mantuvieron:
```bash
# Verificar que los casos siguen ahí
docker exec -it sistemapqrsd-postgres-1 psql -U postgres -d pqrsd_db -c "SELECT COUNT(*) FROM casos;"
```

### **📊 Comparación de Comandos**

| Comando | Contenedores | Volúmenes | Datos | Uso Recomendado |
|---------|-------------|-----------|-------|----------------|
| `docker compose stop` | ⏸️ Detiene | ✅ Mantiene | ✅ Seguros | Pausa temporal |
| `docker compose down` | ❌ Elimina | ✅ Mantiene | ✅ Seguros | Reinicio limpio |
| `docker compose down -v` | ❌ Elimina | ❌ Elimina | ❌ Perdidos | Reset completo |

### **🎯 Casos de Uso**

#### ✅ Cuándo usar `docker compose down`:
- Actualizar configuración en `docker-compose.yml`
- Reiniciar servicios con problemas
- Aplicar cambios en variables de entorno
- Limpiar contenedores pero mantener datos
- **Desarrollo diario normal**

#### ⚠️ Cuándo usar `docker compose down -v`:
- **Solo en desarrollo:** resetear base de datos completamente
- Problemas de corrupción de datos
- Cambiar esquema de base de datos desde cero
- **NUNCA en producción sin backup**

### **🛡️ Mejores Prácticas**

#### Para desarrollo seguro:
```bash
# ✅ Comando por defecto (seguro)
docker compose down
docker compose up -d

# ⚠️ Solo si necesitas reset completo
docker compose down -v
docker compose up -d
# Luego cargar datos de ejemplo:
python -m tests.fixtures.insertar_casos_ejemplo
```

#### Para hacer backup antes de operaciones peligrosas:
```bash
# Backup de la base de datos
docker exec sistemapqrsd-postgres-1 pg_dump -U postgres pqrsd_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar desde backup (si es necesario)
docker exec -i sistemapqrsd-postgres-1 psql -U postgres pqrsd_db < backup_20250101_120000.sql
```

### **⚠️ Advertencias Importantes**

- **🚨 NUNCA uses `docker compose down -v` en producción** sin hacer backup primero
- **✅ Usa `docker compose down` como comando por defecto** para desarrollo
- **📋 Siempre verifica que los datos se mantuvieron** después de reiniciar
- **💾 Haz backups regulares** antes de cambios importantes

---

## 🚨 Solución de Problemas

### **Error: "No module named 'dotenv'"**
```bash
# Asegúrate de que el entorno virtual esté activado
.\venv\Scripts\Activate.ps1
pip install python-dotenv
```

### **Error: "Connection refused" (PostgreSQL)**
```bash
# Verifica que Docker esté ejecutándose
docker compose up
# Espera unos segundos y vuelve a intentar
```

### **Error: "Permission denied" (PowerShell)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Puerto 8000 ocupado**
```bash
# Usa un puerto diferente
uvicorn main:app --host localhost --port 8001 --reload
```

### **Error: Puerto 5432 ocupado**
```bash
# Ver qué proceso usa el puerto
netstat -tulpn | grep 5432

# Cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"  # Usar puerto 5433 en lugar de 5432
```

### **Error: "relation does not exist"**
```bash
# Ejecutar migraciones
alembic upgrade head
```

### **Error: Permisos de Docker**
```bash
# Linux: Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Reiniciar sesión después
```

### **❌ Errores al insertar casos de ejemplo**

**Error: "relation 'casos' does not exist"**
```bash
# Causa: Las migraciones no se han aplicado
# Solución:
alembic upgrade head

# Verificar que la tabla existe:
psql -h localhost -U pqrsd_user -d pqrsd_db -c "\dt casos"
```

**Error: "connection refused" o "could not connect to server"**
```bash
# Causa: PostgreSQL no está corriendo
# Solución:
docker compose up -d

# Verificar estado:
docker compose ps
# El contenedor 'postgres' debe estar 'Up'
```

**Error: "ImportError" o "ModuleNotFoundError"**
```bash
# Causa: Entorno virtual no activado o dependencias faltantes
# Solución:

# Windows:
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "No module named 'tests.fixtures'"**
```bash
# Causa: Ejecutando desde directorio incorrecto
# Solución: Asegurarse de estar en el directorio raíz del proyecto
cd /ruta/al/proyecto/SistemaPQRSD
python -m tests.fixtures.insertar_casos_ejemplo
```

**Verificar que los datos se insertaron correctamente:**
```bash
# Método 1: Contar registros en la base de datos
psql -h localhost -U pqrsd_user -d pqrsd_db -c "SELECT COUNT(*) FROM casos;"

# Método 2: Usar la API (requiere servidor corriendo)
curl "http://localhost:8000/casos/" | jq 'length'

# Método 3: Script Python directo
python -c "from app.services.caso import obtener_todos_los_casos; print(f'Casos insertados: {len(obtener_todos_los_casos())}')"
```

---

## 📁 Estructura del Proyecto

```
pqrsd/
├── 📄 main.py              # Aplicación principal FastAPI
├── 📁 app/routers/         # Rutas y endpoints
│   └── 📄 caso.py          # Endpoints de casos PQRSD
├── 📄 models.py            # Modelos Pydantic
├── 📄 db_models.py         # Modelos SQLAlchemy
├── 📁 app/core/
│   └── 📄 database.py      # Configuración de base de datos
├── 📁 app/services/        # Lógica de negocio
│   └── 📄 caso.py          # Servicios de casos PQRSD
├── 📄 alembic.ini          # Configuración de Alembic
├── 📁 app/migrations/      # Migraciones de base de datos
├── 📄 requirements.txt     # Dependencias Python
├── 📄 docker-compose.yml   # Configuración Docker
├── 📄 .env                 # Variables de entorno
└── 📁 GUIAS/               # Documentación adicional
```

---

## 🎯 Próximos Pasos

1. **Explora la documentación:** http://localhost:8000/docs
2. **Revisa las guías adicionales** en la carpeta `GUIAS/`
3. **Personaliza la configuración** en `.env`
4. **Desarrolla nuevas funcionalidades** siguiendo la estructura existente

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs** del servidor y Docker
2. **Consulta las guías** en `GUIAS/`
3. **Verifica la configuración** en `.env`
4. **Reinicia los servicios** si es necesario

---

**¡Sistema PQRSD listo para usar! 🎉**