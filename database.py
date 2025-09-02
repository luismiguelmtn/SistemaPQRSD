# -*- coding: utf-8 -*-
"""
Configuración de Base de Datos PostgreSQL para el Sistema PQRSD

Este archivo configura la conexión a PostgreSQL usando SQLAlchemy con variables de entorno
para mayor seguridad y flexibilidad en diferentes entornos (desarrollo, testing, producción).

¿Qué hace este archivo?
1. Carga configuración de PostgreSQL desde variables de entorno
2. Crea el "motor" de base de datos (engine) con pool de conexiones
3. Configura las sesiones para interactuar con la base de datos
4. Proporciona funciones seguras para obtener conexiones a la base de datos
5. Incluye validación de configuración y manejo de errores

¿Qué es cada componente?

- ENGINE: Motor que maneja el pool de conexiones a PostgreSQL
- SESSION: Sesión transaccional para operaciones con la base de datos
- BASE: Clase base declarativa para todos los modelos ORM

Ventajas de PostgreSQL sobre SQLite:
- Soporte para múltiples usuarios concurrentes
- Transacciones ACID completas
- Tipos de datos avanzados (JSON, Arrays, etc.)
- Mejor rendimiento en aplicaciones de producción
- Funciones y procedimientos almacenados
- Replicación y alta disponibilidad
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv
import logging
from typing import Generator

# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS POSTGRESQL
# ============================================================================

# Cargar variables de entorno desde archivo .env (si existe)
load_dotenv()

# Configurar logging para debugging de base de datos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables de entorno para configuración de PostgreSQL
# Estas deben estar definidas en el archivo .env o en el sistema
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pqrsd_sistema")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Validar que las variables críticas estén configuradas
if not DB_PASSWORD:
    logger.warning("⚠️  DB_PASSWORD no está configurada. Usando valor por defecto (no recomendado para producción)")
    DB_PASSWORD = "postgres"

# Construir URL de conexión a PostgreSQL
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_base_datos
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración del motor de base de datos con pool de conexiones
# Pool de conexiones mejora el rendimiento reutilizando conexiones
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,          # Tipo de pool de conexiones
    pool_size=10,                 # Número de conexiones permanentes en el pool
    max_overflow=20,              # Conexiones adicionales permitidas
    pool_pre_ping=True,           # Verificar conexiones antes de usarlas
    pool_recycle=3600,            # Reciclar conexiones cada hora
    echo=os.getenv("DB_ECHO", "false").lower() == "true"  # Mostrar SQL en consola
)

# Crear una "fábrica" de sesiones
# Una sesión es como una "conversación" con la base de datos
# autocommit=False: Los cambios no se guardan automáticamente (más seguro)
# autoflush=False: Los cambios no se envían automáticamente a la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Crear la clase base para todos los modelos
# Todos los modelos de tablas heredarán de esta clase
Base = declarative_base()

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_database_session() -> Generator:
    """
    Generador de sesiones de base de datos PostgreSQL con manejo automático de recursos.
    
    Esta función es un generador que:
    1. Crea una nueva sesión de base de datos
    2. La entrega para su uso (yield)
    3. Automáticamente la cierra al finalizar
    4. Maneja errores y rollbacks automáticamente
    
    Uso típico en FastAPI:
    ```python
    def get_casos(db: Session = Depends(get_db)):
        return db.query(Caso).all()
    ```
    
    Yields:
        Session: Sesión de SQLAlchemy lista para usar
        
    Raises:
        SQLAlchemyError: Si hay problemas de conexión o transacción
    """
    db = SessionLocal()
    try:
        yield db
        # Si llegamos aquí, todo salió bien, hacer commit
        db.commit()
    except Exception as e:
        # Si hay error, hacer rollback para mantener consistencia
        db.rollback()
        logger.error(f"Error en sesión de base de datos: {e}")
        raise
    finally:
        # Siempre cerrar la sesión para liberar la conexión
        db.close()


# Alias para compatibilidad con FastAPI Depends
get_db = get_database_session


def get_database_session_old() -> Generator:
    """
    Obtiene una nueva sesión de base de datos PostgreSQL con manejo seguro de conexiones.
    
    ¿Qué es una sesión?
    Una sesión es como abrir un "canal de comunicación" transaccional con PostgreSQL.
    A través de la sesión puedes:
    - Hacer consultas (SELECT) con aislamiento transaccional
    - Insertar datos (INSERT) con validación de integridad
    - Actualizar datos (UPDATE) con bloqueos optimistas
    - Eliminar datos (DELETE) con verificación de restricciones
    
    ¿Por qué usar yield en lugar de return?
    yield convierte esta función en un "generador", lo que permite:
    - Abrir la sesión y iniciar una transacción
    - Entregar la sesión para que la uses
    - Automáticamente hacer commit/rollback según el resultado
    - Cerrar la sesión y liberar la conexión al pool
    
    Ventajas del patrón generador:
    - Garantiza liberación de recursos
    - Manejo automático de transacciones
    - Previene memory leaks
    - Integración con context managers
    
    Uso típico:
    ```python
    with get_database_session() as db:
        # Operaciones con la base de datos
        # Commit automático si no hay errores
    ```
    
    Returns:
        Generator: Generador que produce una sesión de SQLAlchemy
    
    Raises:
        SQLAlchemyError: Si hay problemas de conexión o transacción
    """
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión para usar
    except Exception as e:
        # En caso de error, hacer rollback de la transacción
        db.rollback()
        logger.error(f"Error en sesión de base de datos: {e}")
        raise
    finally:
        # Siempre cerrar la sesión para liberar la conexión
        db.close()

def create_tables():
    """
    Crea todas las tablas en la base de datos PostgreSQL.
    
    ¿Qué hace esta función?
    1. Conecta a PostgreSQL usando las credenciales configuradas
    2. Toma todos los modelos que heredan de Base (ORM models)
    3. Genera y ejecuta comandos CREATE TABLE en PostgreSQL
    4. Crea índices, restricciones y relaciones definidas en los modelos
    5. Si las tablas ya existen, las omite (idempotente)
    
    Ventajas de PostgreSQL:
    - Soporte para tipos de datos avanzados (JSONB, Arrays, UUID)
    - Restricciones de integridad referencial robustas
    - Índices parciales y funcionales
    - Secuencias automáticas para claves primarias
    
    Ejemplo:
    Si tienes un modelo llamado "Caso", esta función creará:
    - Tabla "casos" con todas las columnas definidas
    - Secuencia para el ID autoincremental
    - Índices en campos marcados como index=True
    - Restricciones de clave foránea
    
    Raises:
        SQLAlchemyError: Si hay problemas de conexión o permisos
    """
    try:
        # Importar todos los modelos aquí para que SQLAlchemy los conozca
        # Esto es necesario para que create_all() sepa qué tablas crear
        from db_models import Caso  # Importamos después para evitar imports circulares
        
        logger.info("🏗️  Creando tablas en PostgreSQL...")
        # Crear todas las tablas definidas en los modelos
        Base.metadata.create_all(bind=engine)
        logger.info(f"✅ Tablas creadas exitosamente en PostgreSQL: {DB_NAME}")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        raise

def drop_tables():
    """
    Elimina todas las tablas de la base de datos PostgreSQL.
    
    ⚠️ CUIDADO: Esta función elimina TODOS los datos y estructura.
    
    ¿Qué hace exactamente?
    1. Conecta a PostgreSQL
    2. Ejecuta DROP TABLE CASCADE para cada tabla
    3. Elimina secuencias, índices y restricciones asociadas
    4. Libera el espacio ocupado en el servidor
    
    Solo usar en desarrollo para resetear la base de datos.
    NUNCA usar en producción a menos que sepas exactamente lo que haces.
    
    En PostgreSQL, esta operación:
    - Es transaccional (se puede hacer rollback)
    - Respeta restricciones de clave foránea
    - Elimina automáticamente índices y secuencias
    
    Raises:
        SQLAlchemyError: Si hay problemas de conexión o permisos
    """
    try:
        logger.warning("⚠️ Eliminando todas las tablas de PostgreSQL...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("⚠️ Todas las tablas han sido eliminadas de PostgreSQL")
    except Exception as e:
        logger.error(f"❌ Error eliminando tablas: {e}")
        raise

def database_exists() -> bool:
    """
    Verifica si la base de datos PostgreSQL existe y es accesible.
    
    A diferencia de SQLite (que es un archivo), PostgreSQL es un servidor
    de base de datos, por lo que verificamos:
    1. Conectividad al servidor PostgreSQL
    2. Existencia de la base de datos específica
    3. Permisos de acceso
    
    Returns:
        bool: True si la base de datos existe y es accesible, False si no.
    """
    try:
        # Intentar conectar y hacer una consulta simple
        with engine.connect() as connection:
            # Verificar que podemos ejecutar una consulta básica
            result = connection.execute(text("SELECT 1"))
            return result.fetchone() is not None
    except Exception as e:
        logger.error(f"No se puede conectar a la base de datos PostgreSQL: {e}")
        return False

def get_database_info() -> dict:
    """
    Obtiene información detallada sobre la base de datos PostgreSQL.
    
    Recopila información del servidor PostgreSQL incluyendo:
    - Configuración de conexión
    - Estado de conectividad
    - Versión del servidor
    - Tamaño de la base de datos
    - Número de tablas
    
    Returns:
        dict: Información completa sobre la base de datos PostgreSQL
    """
    info = {
        "database_name": DB_NAME,
        "database_host": DB_HOST,
        "database_port": DB_PORT,
        "database_user": DB_USER,
        "database_url": DATABASE_URL.replace(DB_PASSWORD, "***"),  # Ocultar contraseña
        "exists": database_exists(),
        "server_version": None,
        "database_size_mb": 0,
        "table_count": 0,
        "connection_pool_size": engine.pool.size(),
        "connection_pool_overflow": engine.pool.overflow()
    }
    
    if info["exists"]:
        try:
            with engine.connect() as connection:
                # Obtener versión del servidor PostgreSQL
                version_result = connection.execute(text("SELECT version()"))
                info["server_version"] = version_result.fetchone()[0]
                
                # Obtener tamaño de la base de datos
                size_query = text(
                    "SELECT pg_size_pretty(pg_database_size(:db_name)) as size, "
                    "pg_database_size(:db_name) as size_bytes"
                )
                size_result = connection.execute(size_query, {"db_name": DB_NAME})
                size_row = size_result.fetchone()
                if size_row:
                    info["database_size_pretty"] = size_row[0]
                    info["database_size_mb"] = round(size_row[1] / (1024 * 1024), 2)
                
                # Contar número de tablas
                table_query = text(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = 'public'"
                )
                table_result = connection.execute(table_query)
                info["table_count"] = table_result.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Error obteniendo información de la base de datos: {e}")
            info["error"] = str(e)
    
    return info

# ============================================================================
# INFORMACIÓN PARA DEBUGGING
# ============================================================================

if __name__ == "__main__":
    # Este código solo se ejecuta si ejecutas este archivo directamente
    # python database.py
    
    print("🔧 Configuración de Base de Datos PostgreSQL")
    print(f"🏢 Servidor: {DB_HOST}:{DB_PORT}")
    print(f"🗄️ Base de datos: {DB_NAME}")
    print(f"👤 Usuario: {DB_USER}")
    print(f"🔗 URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")
    
    # Información detallada de la base de datos
    print("\n📊 Información de la base de datos:")
    db_info = get_database_info()
    for key, value in db_info.items():
        print(f"   {key}: {value}")
    
    # Ejemplo de cómo usar la sesión
    print("\n🧪 Probando conexión a PostgreSQL...")
    try:
        with next(get_database_session()) as db:
            print("✅ Conexión exitosa a PostgreSQL")
            # Probar una consulta simple
            result = db.execute(text("SELECT current_database(), current_user, version()"))
            row = result.fetchone()
            print(f"   📋 Base de datos actual: {row[0]}")
            print(f"   👤 Usuario actual: {row[1]}")
            print(f"   🔧 Versión: {row[2][:50]}...")
    except Exception as e:
        print(f"❌ Error de conexión a PostgreSQL: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verificar que PostgreSQL esté ejecutándose")
        print("   2. Verificar credenciales en el archivo .env")
        print("   3. Verificar que la base de datos exista")
        print("   4. Verificar permisos del usuario")