# -*- coding: utf-8 -*-
"""
Configuración de Base de Datos para el Sistema PQRSD

Este archivo configura la conexión a la base de datos usando SQLAlchemy.

¿Qué hace este archivo?
1. Configura la conexión a la base de datos (SQLite en este caso)
2. Crea el "motor" de base de datos (engine)
3. Configura las sesiones para interactuar con la base de datos
4. Proporciona funciones para obtener conexiones a la base de datos

¿Qué es cada componente?

- ENGINE: Es como el "motor" que maneja la conexión a la base de datos
- SESSION: Es como una "conversación" con la base de datos donde puedes hacer consultas
- BASE: Es la clase base de la que heredan todos los modelos de tablas

Analogia:
- Engine = El motor de un carro
- Session = Un viaje específico que haces con el carro
- Base = El plano/diseño base para construir todos los carros
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================================

# Nombre del archivo de base de datos SQLite
# SQLite guarda toda la base de datos en un solo archivo
DATABASE_FILE = "pqrsd_sistema.db"

# URL de conexión a la base de datos
# Para SQLite, la URL tiene el formato: sqlite:///ruta_al_archivo.db
# Los tres /// indican que es un archivo local
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Crear el "motor" de la base de datos
# El motor es responsable de manejar las conexiones
# connect_args={"check_same_thread": False} es específico para SQLite
# y permite usar la base de datos desde múltiples hilos (threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Solo necesario para SQLite
    echo=False  # Cambia a True si quieres ver las consultas SQL en la consola
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

def get_database_session():
    """
    Obtiene una nueva sesión de base de datos.
    
    ¿Qué es una sesión?
    Una sesión es como abrir un "canal de comunicación" con la base de datos.
    A través de la sesión puedes:
    - Hacer consultas (SELECT)
    - Insertar datos (INSERT)
    - Actualizar datos (UPDATE)
    - Eliminar datos (DELETE)
    
    ¿Por qué usar yield en lugar de return?
    yield convierte esta función en un "generador", lo que permite:
    - Abrir la sesión
    - Entregar la sesión para que la uses
    - Automáticamente cerrar la sesión cuando termines
    
    Esto garantiza que las conexiones se cierren correctamente.
    
    Uso típico:
    ```python
    with get_database_session() as db:
        # Usar la base de datos
        casos = db.query(Caso).all()
    # La sesión se cierra automáticamente aquí
    ```
    """
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión para usar
    finally:
        db.close()  # Siempre cierra la sesión, incluso si hay errores

def create_tables():
    """
    Crea todas las tablas en la base de datos.
    
    Esta función debe llamarse una vez para crear la estructura
    de la base de datos (las tablas) basada en los modelos definidos.
    
    ¿Cuándo usar esta función?
    - La primera vez que ejecutas la aplicación
    - Cuando agregas nuevos modelos/tablas
    - Para resetear la base de datos en desarrollo
    
    Nota: En producción, es mejor usar migraciones (Alembic)
    para cambios más controlados.
    """
    # Importar todos los modelos aquí para que SQLAlchemy los conozca
    # Esto es necesario para que create_all() sepa qué tablas crear
    from db_models import Caso  # Importamos después para evitar imports circulares
    
    # Crear todas las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)
    print(f"✅ Tablas creadas exitosamente en: {DATABASE_FILE}")

def drop_tables():
    """
    Elimina todas las tablas de la base de datos.
    
    ⚠️ CUIDADO: Esta función elimina TODOS los datos.
    Solo usar en desarrollo para resetear la base de datos.
    
    NUNCA usar en producción a menos que sepas exactamente lo que haces.
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas han sido eliminadas")

def database_exists() -> bool:
    """
    Verifica si el archivo de base de datos existe.
    
    Returns:
        bool: True si la base de datos existe, False si no.
    """
    return os.path.exists(DATABASE_FILE)

def get_database_info() -> dict:
    """
    Obtiene información sobre la base de datos.
    
    Returns:
        dict: Información sobre la base de datos (archivo, tamaño, etc.)
    """
    info = {
        "database_file": DATABASE_FILE,
        "database_url": DATABASE_URL,
        "exists": database_exists(),
        "size_bytes": 0
    }
    
    if info["exists"]:
        info["size_bytes"] = os.path.getsize(DATABASE_FILE)
        info["size_mb"] = round(info["size_bytes"] / (1024 * 1024), 2)
    
    return info

# ============================================================================
# INFORMACIÓN PARA DEBUGGING
# ============================================================================

if __name__ == "__main__":
    # Este código solo se ejecuta si ejecutas este archivo directamente
    # python database.py
    
    print("🔧 Configuración de Base de Datos")
    print(f"📁 Archivo: {DATABASE_FILE}")
    print(f"🔗 URL: {DATABASE_URL}")
    print(f"📊 Info: {get_database_info()}")
    
    # Ejemplo de cómo usar la sesión
    print("\n🧪 Probando conexión...")
    try:
        with next(get_database_session()) as db:
            print("✅ Conexión exitosa a la base de datos")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")