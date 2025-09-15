# 🗄️ Guía de Alembic para Sistema PQRSD

## 🖥️ Nota Importante sobre Compatibilidad

**⚠️ IMPORTANTE para usuarios de Windows:**
Esta guía incluye comandos específicos para diferentes sistemas operativos. Los comandos `psql` mencionados en esta documentación requieren diferentes enfoques:

- **🪟 Windows**: Usa `docker compose exec postgres psql` (a través de Docker)
- **🐧 Linux/Mac**: Puede usar `psql` directamente si está instalado
- **🐍 Alternativa universal**: Usa `python app/core/database.py` en cualquier sistema

Todos los comandos en esta guía incluyen las variantes para cada sistema operativo.

---

## 🔰 ¿Qué es Alembic? (Para Principiantes)

**Alembic** es como un "control de versiones para tu base de datos". Imagina que trabajas en equipo y cada uno tiene su propia base de datos local. Alembic asegura que todos tengan exactamente las mismas tablas, columnas y estructura.

### 🤔 ¿Por qué es importante?

**Sin Alembic:**
- ❌ Cada desarrollador tiene tablas diferentes
- ❌ Errores de "tabla no existe" al cambiar de PC
- ❌ Imposible sincronizar cambios de base de datos
- ❌ Caos al desplegar en producción

**Con Alembic:**
- ✅ Todos tienen la misma estructura de base de datos
- ✅ Cambios controlados y versionados
- ✅ Fácil despliegue en cualquier entorno
- ✅ Historial completo de cambios

### 🏗️ ¿Cómo funciona? (Flujo de Trabajo de la Industria)

**📋 FLUJO COMPLETO DE DESARROLLO:**

```
1. MODELO SQLAlchemy    →  2. MIGRACIÓN ALEMBIC    →  3. APLICAR MIGRACIÓN    →  4. TABLAS EN BD
   (app/models/caso.py)     (alembic revision)         (alembic upgrade)         (PostgreSQL)
        ↓                        ↓                          ↓                         ↓
   Defines estructura       Genera SQL automático      Ejecuta CREATE TABLE     Tablas creadas
```

**🔄 PASOS DETALLADOS:**

1. **📝 DEFINES el modelo** en `app/models/caso.py`
   ```python
   class Caso(Base):
       __tablename__ = "casos"
       id = Column(Integer, primary_key=True)
       # ... más columnas
   ```

2. **🔍 ALEMBIC DETECTA cambios** automáticamente
   ```bash
   alembic revision --autogenerate -m "Crear tabla casos"
   ```
   - Compara tus modelos vs base de datos actual
   - Genera archivo de migración con SQL necesario

3. **🚀 APLICAS la migración** a la base de datos
   ```bash
   alembic upgrade head
   ```
   - Ejecuta el SQL generado
   - Crea/modifica tablas en PostgreSQL

4. **📤 COMPARTES con el equipo** via Git
   - El archivo de migración se versiona
   - Tu equipo ejecuta `alembic upgrade head`
   - Todos quedan sincronizados

**🎯 PRINCIPIOS CLAVE:**
- ✅ **Nunca modifiques la BD directamente** - siempre usa migraciones
- ✅ **Los modelos son la fuente de verdad** - la BD se adapta a ellos
- ✅ **Las migraciones son automáticas** - Alembic genera el SQL
- ✅ **Versionado completo** - cada cambio queda registrado

## ✅ Configuración Actual del Proyecto

- **Variables de entorno**: Alembic usa las credenciales del archivo `.env`
- **Migración inicial**: Creada y marcada como aplicada
- **Estado actual**: Sincronizado con la base de datos existente

### 🔧 Archivos Importantes
- `alembic.ini`: Configuración principal de Alembic
- `app/migrations/env.py`: Configuración de conexión a la base de datos
- `app/migrations/versions/`: Carpeta con todas las migraciones (¡NO tocar manualmente!)

## 🚀 Comandos de Alembic

### 🔰 Comandos Básicos (Para Principiantes)

#### 📊 VERIFICACIÓN Y DIAGNÓSTICO (Ejecuta SIEMPRE primero)
```bash
# ✅ ¿En qué versión estoy?
alembic current

# 📋 Ver historial completo de cambios
alembic history --verbose

# 🔍 Verificar si hay migraciones pendientes
alembic heads

# 📁 ¿Existen archivos de migración?
ls app/migrations/versions/
# Windows: dir app\migrations\versions\
```

#### 🆕 PROYECTO NUEVO (Base de datos vacía)
```bash
# 1. ✅ VERIFICAR si existen migraciones
ls app/migrations/versions/

# 2. 🔄 Si está vacía, CREAR migración inicial
alembic revision --autogenerate -m "Initial migration"

# 3. 🚀 APLICAR migración (crea TODAS las tablas)
alembic upgrade head

# 4. ✅ VERIFICAR que se aplicó correctamente
alembic current
```

#### 🔄 PROYECTO EXISTENTE (Actualizar base de datos)
```bash
# 1. ✅ VERIFICAR estado actual
alembic current

# 2. 🚀 APLICAR nuevas migraciones del equipo
alembic upgrade head

# 3. ✅ CONFIRMAR que se aplicaron
alembic current
```

**🚨 TROUBLESHOOTING COMÚN:**
- ❌ **"tabla no existe"** → Ejecuta `alembic upgrade head`
- ❌ **"No revision files found"** → Crea migración inicial
- ❌ **Solo tabla `alembic_version`** → Faltan migraciones en `/versions/`

### 🛠️ Comandos Avanzados (Para Desarrolladores)

#### 📝 Crear migraciones
```bash
# Generar migración automáticamente (RECOMENDADO)
alembic revision --autogenerate -m "Descripción del cambio"

# Crear migración vacía (manual)
alembic revision -m "Descripción del cambio"

# Ver diferencias antes de crear migración
alembic revision --autogenerate -m "Cambio" --sql
```

#### 🎯 Aplicar migraciones específicas
```bash
# Aplicar hasta una revisión específica
alembic upgrade <revision_id>

# Aplicar solo la siguiente migración
alembic upgrade +1

# Ver SQL sin ejecutar
alembic upgrade head --sql
```

#### ⚠️ Revertir migraciones (¡CUIDADO!)
```bash
# Revertir a la migración anterior
alembic downgrade -1

# Revertir a una revisión específica
alembic downgrade <revision_id>

# Revertir todas las migraciones (¡ELIMINA TODAS LAS TABLAS!)
alembic downgrade base
```

### ✅ VALIDACIÓN Y VERIFICACIÓN (Mejores Prácticas)

#### 🔍 ANTES de cualquier operación
```bash
# Estado actual del sistema
alembic current

# Verificar migraciones disponibles
alembic heads

# Historial completo
alembic history --verbose

# Verificar archivos de migración
ls -la app/migrations/versions/
```

#### 🚀 DESPUÉS de aplicar migraciones
```bash
# Confirmar aplicación exitosa
alembic current

# Verificar tablas en PostgreSQL

# Windows (usando Docker - RECOMENDADO):
docker compose exec postgres psql -U pqrsd_user -d pqrsd_sistema -c "\dt"

# Linux/Mac (con psql instalado localmente):
psql -h localhost -U pqrsd_user -d pqrsd_sistema -c "\dt"

# Alternativa multiplataforma (usando Python):
python app/core/database.py

# Verificar estructura específica

# Windows (usando Docker):
docker compose exec postgres psql -U pqrsd_user -d pqrsd_sistema -c "\d casos"

# Linux/Mac (con psql instalado localmente):
psql -h localhost -U pqrsd_user -d pqrsd_sistema -c "\d casos"
```

#### 🎯 VALIDACIÓN DE INTEGRIDAD
```bash
# Verificar que los modelos coinciden con la BD
alembic check

# Generar migración de prueba (sin aplicar)
alembic revision --autogenerate -m "Test" --sql

# Verificar conexión a la base de datos
alembic current
```

## 🆕 ¿Acabas de Clonar el Proyecto? (Guía Completa)

### 🤔 Situaciones Típicas

#### 📥 Situación 1: Proyecto Existente (Recomendado)
Acabas de clonar el proyecto y quieres usar las migraciones existentes:
- ✅ El código fuente
- ✅ Migraciones ya creadas por el equipo
- ❌ Una base de datos completamente vacía
- ❌ Ninguna tabla creada

#### 🆕 Situación 2: Instalación Desde Cero
Quieres empezar completamente limpio, creando tus propias migraciones:
- ✅ El código fuente
- ❌ Quieres eliminar migraciones existentes
- ❌ Crear tu propia migración inicial
- ❌ Base de datos completamente vacía

**🎯 Objetivo**: Tener el proyecto funcionando según tu situación específica.

### 🗑️ Instalación Desde Cero (Opcional)

**⚠️ ADVERTENCIA**: Solo haz esto si realmente necesitas empezar desde cero. La mayoría de usuarios deben usar la "Situación 1".

#### 🧹 Archivos y Carpetas a Eliminar

```bash
# 1. Eliminar archivos de migración existentes
# Windows:
rmdir /s app\migrations\versions
mkdir app\migrations\versions

# Linux/Mac:
rm -rf app/migrations/versions/*

# 2. Eliminar base de datos Docker (si existe)
docker compose down -v
docker volume prune -f

# 3. Eliminar archivo de entorno (opcional)
del .env  # Windows
rm .env   # Linux/Mac
```

#### 📁 Estructura Después de Limpiar

```
app/migrations/
├── env.py              # ✅ MANTENER (configuración de Alembic)
├── script.py.mako      # ✅ MANTENER (plantilla de migraciones)
├── README              # ✅ MANTENER (documentación)
└── versions/           # ✅ MANTENER carpeta (pero VACÍA)
    └── (vacío)         # ❌ Todos los archivos .py eliminados
```

**🚨 Archivos que NUNCA debes eliminar:**
- `alembic.ini` (configuración principal)
- `app/migrations/env.py` (configuración de conexión)
- `app/migrations/script.py.mako` (plantilla)
- `app/migrations/README` (documentación)
- La carpeta `app/migrations/versions/` (solo vaciar contenido)

#### 🎯 ¿Cuándo Hacer Instalación Desde Cero?

**✅ Casos válidos:**
- Eres el primer desarrollador del proyecto
- Quieres personalizar completamente la estructura de BD
- Tienes conflictos irresolubles con migraciones
- Estás creando un fork independiente del proyecto

**❌ NO hagas esto si:**
- Solo quieres que el proyecto funcione (usa migraciones existentes)
- Trabajas en equipo (causarás conflictos)
- No entiendes completamente Alembic
- Es tu primera vez con el proyecto

### ✅ Solución Paso a Paso

#### 🔄 Opción A: Proyecto Existente (Recomendado)

**Para la mayoría de usuarios que solo quieren que el proyecto funcione:**

##### 1️⃣ Preparar el Entorno
```bash
# Clonar el repositorio (si no lo has hecho)
git clone <url-del-repositorio>
cd SistemaPQRSD

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 🆕 Opción B: Instalación Desde Cero

**Solo para usuarios avanzados que necesitan empezar completamente limpio:**

##### 1️⃣ Limpiar Archivos Existentes
```bash
# Clonar y entrar al proyecto
git clone <url-del-repositorio>
cd SistemaPQRSD

# LIMPIAR migraciones existentes
# Windows:
rmdir /s app\migrations\versions
mkdir app\migrations\versions

# Linux/Mac:
rm -rf app/migrations/versions/*

# Limpiar Docker (opcional)
docker compose down -v
docker volume prune -f

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2️⃣ Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo (si existe)
cp .env.example .env

# O crear .env manualmente con este contenido:
```

**Contenido del archivo `.env`:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pqrsd_sistema
DB_USER=pqrsd_user
DB_PASSWORD=desarrollo123
```

#### 3️⃣ Iniciar PostgreSQL
```bash
# Levantar PostgreSQL con Docker
docker compose up -d

# Verificar que esté funcionando
docker compose ps
# Debe mostrar "postgres" como "Up"
```

#### 4️⃣ 🚨 PASO CRÍTICO: Crear Todas las Tablas

**🔄 Para Proyecto Existente (Opción A):**
```bash
# Aplicar migraciones existentes
alembic upgrade head
```

**🆕 Para Instalación Desde Cero (Opción B):**
```bash
# 1. Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# 2. Aplicar la migración inicial
alembic upgrade head
```

**¿Qué hace `alembic upgrade head`?**
- 📋 Lee todos los archivos de migración disponibles
- 🏗️ Ejecuta todos los CREATE TABLE automáticamente
- ✅ Crea la estructura completa de la base de datos
- 🔄 Sincroniza tu BD con las migraciones del proyecto

**¿Qué hace `alembic revision --autogenerate`?**
- 🔍 Compara tus modelos con la base de datos actual
- 📝 Genera automáticamente el código SQL necesario
- 💾 Crea un archivo de migración con timestamp único
- 🎯 Solo necesario en instalación desde cero

#### 5️⃣ Verificar que Todo Funciona
```bash
# Ver estado actual
alembic current
# Debe mostrar algo como: "abc123def456 (head)"

# Iniciar el servidor
python -m uvicorn main:app --reload

# Abrir en el navegador
# http://localhost:8000/docs
```

#### 6️⃣ Agregar Datos de Prueba (Opcional)
```bash
# Cargar casos de ejemplo
python tests/fixtures/datos_ejemplo.py

# Verificar en la API
# http://localhost:8000/casos/
```

### 🆘 Errores Comunes y Soluciones (Para Principiantes)

#### ❌ Error: "relation 'casos' does not exist"
**Causa**: No has creado las tablas en tu base de datos.
```bash
# Solución:
alembic upgrade head
```

#### ❌ Error: "could not connect to server"
**Causa**: PostgreSQL no está ejecutándose.
```bash
# Solución:
docker compose up -d
# Verificar:
docker compose ps
```

#### ❌ Error: "password authentication failed"
**Causa**: Credenciales incorrectas en el archivo `.env`.
```bash
# Solución: Verificar contenido del .env
cat .env
# Debe tener:
# DB_USER=pqrsd_user
# DB_PASSWORD=desarrollo123
```

#### ❌ Error: "Target database is not up to date"
**Causa**: Hay migraciones nuevas que no has aplicado.
```bash
# Solución:
alembic upgrade head
```

#### ❌ Error: "Can't locate revision identified by 'head'"
**Causa**: No hay migraciones en tu proyecto.
```bash
# Solución: Verificar que existan archivos de migración
ls app/migrations/versions/
# Si está vacío, hay un problema con el proyecto
```

#### ❌ Error: "Port 5432 is already in use"
**Causa**: Ya tienes PostgreSQL ejecutándose.
```bash
# Solución: Parar otros PostgreSQL
docker compose down
# O cambiar puerto en docker-compose.yml
```

### 🔧 Variables de Entorno Importantes

**Archivo `.env` correcto:**
```env
# Base de datos (Docker local)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pqrsd_sistema
DB_USER=pqrsd_user
DB_PASSWORD=desarrollo123

# Otras configuraciones...
```

**⚠️ Importante**: 
- Estos valores deben coincidir con `docker-compose.yml`
- NO cambies estos valores a menos que sepas lo que haces
- El archivo `.env` NO debe subirse a Git (está en `.gitignore`)

## Escenarios de Despliegue

### 🆕 Despliegue desde Cero (Base de Datos Vacía)

Cuando despliegas en un entorno completamente nuevo:

```bash
# 1. Levantar Docker
docker-compose up postgres -d

# 2. Aplicar todas las migraciones desde el inicio
alembic upgrade head
```

**Ventajas de usar Alembic:**
- ✅ Alembic garantiza que la estructura sea idéntica en todos los entornos
- ✅ Mantiene un historial completo de cambios
- ✅ Permite versionado y rollback de cambios de esquema
- ✅ Integración nativa con SQLAlchemy

### 🔄 Despliegue con Migraciones Existentes

Cuando ya tienes una base de datos con datos:

```bash
# 1. Verificar el estado actual
alembic current

# 2. Ver migraciones pendientes
alembic history

# 3. Aplicar solo las migraciones nuevas
alembic upgrade head
```



## 👥 Flujo de Trabajo en Equipo

### 🔄 Cuando un compañero agrega una nueva migración:

**Situación**: Tu compañero hizo cambios en la base de datos y subió una migración nueva.

1. **Actualizar código**:
   ```bash
   git pull origin main
   ```

2. **Aplicar nuevas migraciones** (¡CRÍTICO!):
   ```bash
   alembic upgrade head
   ```
   > ⚠️ **Si no haces esto**: Tu aplicación fallará con errores de "tabla no existe"

3. **Verificar que todo esté bien**:
   ```bash
   alembic current
   # Debe mostrar la migración más reciente
   ```

### 📤 Antes de hacer push de una nueva migración:

**Situación**: Tú modificaste modelos y necesitas crear una migración.

1. **Verificar que tu base de datos esté actualizada**:
   ```bash
   alembic current
   alembic upgrade head
   ```

2. **Crear la migración**:
   ```bash
   alembic revision --autogenerate -m "Descripción clara del cambio"
   ```
   > 💡 **Tip**: Usa descripciones como "Agregar tabla usuarios" o "Modificar campo email"

3. **⚠️ IMPORTANTE: Revisar el archivo generado** en `app/migrations/versions/`
   - Verificar que los cambios sean correctos
   - No debe eliminar datos importantes
   - Verificar nombres de tablas y columnas

4. **Probar la migración localmente**:
   ```bash
   alembic upgrade head
   # Verificar que no hay errores
   ```

5. **Hacer commit y push**:
   ```bash
   git add .
   git commit -m "feat: agregar migración para [descripción]"
   git push origin feature/nueva-funcionalidad
   ```

### 🚨 Reglas de Oro para Equipos:

1. **NUNCA** edites manualmente archivos de migración existentes
2. **SIEMPRE** ejecuta `alembic upgrade head` después de `git pull`
3. **SIEMPRE** revisa el archivo de migración antes de hacer commit
4. **NUNCA** hagas `alembic downgrade` en producción sin consultar
5. **SIEMPRE** prueba las migraciones localmente antes de hacer push

### 🔧 Conflictos de Migraciones

Si dos desarrolladores crean migraciones al mismo tiempo:

```bash
# Problema: Dos migraciones con el mismo "down_revision"
# Solución: Crear una migración de merge

# 1. Identificar las migraciones conflictivas
alembic history

# 2. Crear migración de merge
alembic merge -m "Merge migrations" <revision1> <revision2>

# 3. Aplicar la migración de merge
alembic upgrade head
```

---

## 📚 Recursos Adicionales para Principiantes

### 🎯 Comandos que Debes Memorizar

```bash
# Los 3 comandos más importantes:
docker compose up -d          # Iniciar base de datos
alembic upgrade head          # Aplicar migraciones
python tests/fixtures/datos_ejemplo.py  # Cargar datos de prueba
```

### 🔍 Cómo Verificar que Todo Funciona

1. **Base de datos funcionando**:
   ```bash
   docker compose ps
   # Debe mostrar postgres como "running"
   ```

2. **Migraciones aplicadas**:
   ```bash
   alembic current
   # Debe mostrar un hash de migración
   ```

3. **Tablas creadas**:
   ```bash
   # Conectar a la base de datos
   docker compose exec postgres psql -U pqrsd_user -d pqrsd_sistema
   # Dentro de psql:
   \dt
   # Debe mostrar tablas como: casos, usuarios, etc.
   \q  # Para salir
   ```

### 💡 Consejos para Principiantes

- **🚀 Siempre empieza con**: `docker compose up -d` y `alembic upgrade head`
- **📝 Antes de programar**: Verifica que tienes datos de prueba cargados
- **🔄 Después de git pull**: Ejecuta `alembic upgrade head` automáticamente
- **❓ Si algo falla**: Lee el mensaje de error completo, suele decir qué hacer
- **🆘 Si estás perdido**: Borra todo y clona el proyecto de nuevo

### 🚨 Señales de que Algo Está Mal

- ❌ Error "relation does not exist" → Ejecuta `alembic upgrade head`
- ❌ Error "could not connect" → Ejecuta `docker compose up -d`
- ❌ Error "password authentication failed" → Revisa tu archivo `.env`
- ❌ La aplicación se ve vacía → Carga datos con `python tests/fixtures/datos_ejemplo.py`

### 📖 Documentación Oficial

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [FastAPI Database Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## 🚨 TROUBLESHOOTING: Problemas Comunes y Soluciones

### ❌ Problema: "tabla no existe" o "relation does not exist"

**🔍 DIAGNÓSTICO:**
```bash
# 1. Verificar estado de Alembic
alembic current

# 2. Verificar si existen migraciones
ls app/migrations/versions/
# Windows: dir app\migrations\versions\

# 3. Verificar tablas en la base de datos

# Windows (usando Docker):
docker compose exec postgres psql -U pqrsd_user -d pqrsd_sistema -c "\dt"

# Linux/Mac (con psql instalado localmente):
psql -h localhost -U pqrsd_user -d pqrsd_sistema -c "\dt"

# Alternativa multiplataforma:
python app/core/database.py
```

**✅ SOLUCIONES:**

**Caso A: No hay migraciones (carpeta versions/ vacía)**
```bash
# 1. Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# 2. Aplicar migración
alembic upgrade head

# 3. Verificar
alembic current
```

**Caso B: Hay migraciones pero no se han aplicado**
```bash
# 1. Aplicar todas las migraciones
alembic upgrade head

# 2. Verificar
alembic current
```

### ❌ Problema: Solo existe tabla "alembic_version"

**🔍 CAUSA:** Las migraciones no contienen definiciones de tablas

**✅ SOLUCIÓN:**
```bash
# 1. Verificar contenido de migraciones
cat app/migrations/versions/*.py

# 2. Si están vacías, regenerar
alembic revision --autogenerate -m "Recreate tables"

# 3. Aplicar
alembic upgrade head
```

### ❌ Problema: "No revision files found"

**✅ SOLUCIÓN:**
```bash
# 1. Verificar configuración de Alembic
cat alembic.ini | grep script_location

# 2. Crear migración inicial
alembic revision --autogenerate -m "Initial migration"
```

### ❌ Problema: Migraciones desincronizadas

**✅ SOLUCIÓN SEGURA:**
```bash
# 1. Hacer backup de la base de datos
pg_dump -h localhost -U tu_usuario tu_base_datos > backup.sql

# 2. Ver estado actual
alembic current
alembic heads

# 3. Sincronizar
alembic upgrade head
```

### 🆘 RESET COMPLETO (Solo en desarrollo)

**⚠️ ADVERTENCIA: Esto elimina TODOS los datos**

```bash
# 1. Parar servicios
docker compose down -v

# 2. Limpiar migraciones (opcional)
rm -rf app/migrations/versions/*  # Linux/Mac
rmdir /s app\migrations\versions && mkdir app\migrations\versions  # Windows

# 3. Limpiar volúmenes Docker
docker volume prune -f

# 4. Reiniciar servicios
docker compose up -d

# 5. Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# 6. Aplicar
alembic upgrade head
```

## 🛠️ Comandos de Referencia Rápida

### 🆕 Instalación Desde Cero
```bash
# 1. Limpiar migraciones existentes
rmdir /s app\migrations\versions     # Windows
rm -rf app/migrations/versions/*     # Linux/Mac

# 2. Limpiar Docker
docker compose down -v
docker volume prune -f

# 3. Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# 4. Aplicar migración
alembic upgrade head

# 5. Verificar estado
alembic current
```

### 🔄 Proyecto Existente
```bash
# 1. Aplicar migraciones existentes
alembic upgrade head

# 2. Verificar estado
alembic current

# 3. Ver historial
alembic history
```

### 🚨 Comandos de Emergencia
```bash
# Resetear completamente (BORRA TODO)
docker compose down -v
rm -rf app/migrations/versions/*
alembic revision --autogenerate -m "Reset migration"
alembic upgrade head

# Ver qué migraciones están pendientes
alembic history --verbose

# Forzar marca de migración como aplicada (CUIDADO)
alembic stamp head
```

---

**🎉 ¡Felicidades!** Si llegaste hasta aquí, ya sabes lo básico de Alembic. La práctica hace al maestro, así que no tengas miedo de experimentar en tu entorno local.

## Variables de Entorno Utilizadas

Alembic lee las siguientes variables del archivo `.env`:
- `DB_HOST`: Host de la base de datos
- `DB_PORT`: Puerto de la base de datos
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos

## Notas Importantes

⚠️ **Siempre revisa las migraciones generadas automáticamente antes de aplicarlas**

⚠️ **Haz backup de la base de datos antes de aplicar migraciones en producción**

⚠️ **No modifiques migraciones que ya han sido aplicadas**

## Ejemplo: Agregar Nueva Tabla

1. Crear el modelo en `app/models/nueva_tabla.py`
2. Importar el modelo en `app/migrations/env.py` si es necesario
3. Generar migración: `alembic revision --autogenerate -m "Add nueva_tabla"`
4. Revisar y aplicar: `alembic upgrade head`

---

**Estado actual**: Alembic configurado y listo para usar ✅
**Última actualización**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")