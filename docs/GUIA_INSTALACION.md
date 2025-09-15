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
```bash
python test/datos_ejemplo.py
```
**¿Qué hace?** 
- Inserta datos de prueba realistas
- Crea 5 casos PQRSD de ejemplo con numeración automática (PET-2025-0001, QUE-2025-0001, etc.)
- Útil para testing, desarrollo y demostración
- Incluye casos en diferentes estados (recibido, en proceso, resuelto, cerrado)
- Demuestra el sistema de numeración inteligente por tipo y año

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