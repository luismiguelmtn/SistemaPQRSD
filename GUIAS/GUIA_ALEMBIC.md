# Guía de Alembic para Sistema PQRSD

## Configuración Completada

Alembic ha sido configurado exitosamente en el proyecto con las siguientes características:

### ✅ Configuración Actual
- **Variables de entorno**: Alembic usa las credenciales del archivo `.env`
- **Migración inicial**: Creada y marcada como aplicada
- **Estado actual**: Sincronizado con la base de datos existente

### 🔧 Archivos Configurados
- `alembic.ini`: Configurado para usar variables de entorno
- `app/migrations/env.py`: Actualizado para cargar credenciales desde `.env`
- `app/migrations/versions/`: Contiene las migraciones

## Comandos Útiles

### Crear una nueva migración
```bash
# Generar migración automáticamente (recomendado)
alembic revision --autogenerate -m "Descripción del cambio"

# Crear migración vacía (manual)
alembic revision -m "Descripción del cambio"
```

### Aplicar migraciones
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una revisión específica
alembic upgrade <revision_id>

# Aplicar solo la siguiente migración
alembic upgrade +1
```

### Revertir migraciones
```bash
# Revertir a la migración anterior
alembic downgrade -1

# Revertir a una revisión específica
alembic downgrade <revision_id>

# Revertir todas las migraciones
alembic downgrade base
```

### Información y estado
```bash
# Ver la revisión actual
alembic current

# Ver historial de migraciones
alembic history

# Ver migraciones pendientes
alembic show <revision_id>
```

## Escenarios de Despliegue

### 🆕 Despliegue desde Cero (Base de Datos Vacía)

Cuando despliegas en un entorno completamente nuevo:

```bash
# 1. Crear la base de datos (si no existe)
# 2. Aplicar todas las migraciones desde el inicio
alembic upgrade head
```

**¿Por qué no usar init_db.py?**
- ❌ `init_db.py` fue eliminado porque Alembic maneja mejor la creación de tablas
- ✅ Alembic garantiza que la estructura sea idéntica en todos los entornos
- ✅ Mantiene un historial completo de cambios

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

### 🏗️ Migración desde init_db.py a Alembic

Si anteriormente usabas `init_db.py`:

```bash
# 1. Marcar el estado actual como la migración inicial
alembic stamp head

# 2. A partir de ahora, usar solo Alembic
alembic revision --autogenerate -m "Próximo cambio"
alembic upgrade head
```

## Flujo de Trabajo Recomendado

1. **Modificar modelos**: Edita los archivos en `app/models/`
2. **Generar migración**: `alembic revision --autogenerate -m "Descripción"`
3. **Revisar migración**: Verifica el archivo generado en `app/migrations/versions/`
4. **Aplicar migración**: `alembic upgrade head`
5. **Confirmar cambios**: Verifica que los cambios se aplicaron correctamente

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