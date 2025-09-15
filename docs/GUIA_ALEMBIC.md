# 🗄️ Guía de Alembic para Sistema PQRSD

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

### 🏗️ ¿Cómo funciona?

1. **Modificas un modelo** (agregas una columna, tabla, etc.)
2. **Alembic detecta el cambio** y crea un "archivo de migración"
3. **Aplicas la migración** y tu base de datos se actualiza
4. **Compartes el archivo** con tu equipo via Git
5. **Tu equipo aplica la misma migración** y todos quedan sincronizados

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

#### 📊 Ver información
```bash
# ¿En qué versión estoy? (SIEMPRE ejecuta esto primero)
alembic current

# Ver historial de cambios
alembic history

# Ver historial con detalles
alembic history --verbose
```

#### 🆕 Proyecto nuevo o base de datos vacía
```bash
# Crear TODAS las tablas (OBLIGATORIO en proyecto nuevo)
alembic upgrade head
```

#### 🔄 Actualizar base de datos
```bash
# Aplicar nuevas migraciones del equipo
alembic upgrade head
```

### 🛠️ Comandos Avanzados (Para Desarrolladores)

#### Crear migraciones
```bash
# Generar migración automáticamente (recomendado)
alembic revision --autogenerate -m "Descripción del cambio"

# Crear migración vacía (manual)
alembic revision -m "Descripción del cambio"
```

#### Aplicar migraciones específicas
```bash
# Aplicar hasta una revisión específica
alembic upgrade <revision_id>

# Aplicar solo la siguiente migración
alembic upgrade +1
```

#### Revertir migraciones (¡CUIDADO!)
```bash
# Revertir a la migración anterior
alembic downgrade -1

# Revertir a una revisión específica
alembic downgrade <revision_id>

# Revertir todas las migraciones (¡ELIMINA TODAS LAS TABLAS!)
alembic downgrade base
```

## 🆕 ¿Acabas de Clonar el Proyecto? (Guía Completa)

### 🤔 Situación Típica

Acabas de clonar el proyecto en tu PC y tienes:
- ✅ El código fuente
- ❌ Una base de datos completamente vacía
- ❌ Ninguna tabla creada
- ❌ El servidor no funciona (errores de "tabla no existe")

**🎯 Objetivo**: Tener el proyecto funcionando igual que el desarrollador original.

### ✅ Solución Paso a Paso (¡Sigue este orden!)

#### 1️⃣ Preparar el Entorno
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
```bash
# Este comando crea TODAS las tablas necesarias
alembic upgrade head
```

**¿Qué hace este comando?**
- 📋 Lee todos los archivos de migración
- 🏗️ Ejecuta todos los CREATE TABLE automáticamente
- ✅ Crea la estructura completa de la base de datos
- 🔄 Sincroniza tu BD con la del proyecto original

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