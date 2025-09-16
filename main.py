# main.py - Sistema PQRSD con PostgreSQL
"""
🏢 Sistema PQRSD

Este es el archivo principal de la aplicación FastAPI del Sistema PQRSD,
optimizado para funcionar con PostgreSQL como base de datos empresarial.

🚀 CARACTERÍSTICAS PRINCIPALES:
✓ API REST moderna con FastAPI
✓ Base de datos PostgreSQL con pool de conexiones
✓ Documentación automática (Swagger/OpenAPI)
✓ Validación de datos con Pydantic
✓ Manejo robusto de errores
✓ Logging detallado para auditoría
✓ Configuración por variables de entorno

🏗️ ARQUITECTURA DEL SISTEMA:
┌─────────────────┐    ┌─────────────────┐    ┌────────────────────────┐
│   Frontend      │───▶│   FastAPI       │───▶│       PostgreSQL       │
│   (Web/Mobile)  │    │   (main.py)     │    │ (app/core/database.py) │
└─────────────────┘    └─────────────────┘    └────────────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Services      │
                       │   (Lógica)      │
                       └─────────────────┘

📁 ESTRUCTURA DEL PROYECTO:
- main.py: 🎯 Configuración principal y punto de entrada
- routes.py: 🛣️ Definición de endpoints REST
- models.py: 📋 Esquemas Pydantic para validación
- services.py: ⚙️ Lógica de negocio y operaciones CRUD
- app/core/database.py: 🐘 Configuración PostgreSQL y conexiones
- db_models.py: 🗃️ Modelos SQLAlchemy para ORM
- enums.py: 📝 Enumeraciones y constantes
- alembic.ini: 🔧 Configuración de migraciones
- app/migrations/: 📂 Historial de migraciones de BD

🔧 CONFIGURACIÓN REQUERIDA:
1. PostgreSQL instalado y corriendo (Docker recomendado)
2. Variables de entorno configuradas (.env)
3. Dependencias Python instaladas (requirements.txt)
4. Migraciones aplicadas (alembic upgrade head)

📚 DOCUMENTACIÓN AUTOMÁTICA:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================

from fastapi import FastAPI
from app.routers.caso import router  # Importamos todas las rutas definidas en routes.py

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================

# Inicializar la aplicación FastAPI
# FastAPI() crea una instancia de la aplicación web
app = FastAPI(
    # Título que aparece en la documentación automática
    title="Sistema PQRSD",
    
    # Descripción detallada del sistema
    description="Sistema de Peticiones, Quejas, Reclamos, Sugerencias y Denuncias",
    
    # Versión de la API (útil para versionado)
    version="1.0.0",
    
    # Configuraciones adicionales que se pueden agregar:
    # docs_url="/docs",          # URL de la documentación Swagger (por defecto /docs)
    # redoc_url="/redoc",        # URL de la documentación ReDoc (por defecto /redoc)
    # openapi_url="/openapi.json" # URL del esquema OpenAPI (por defecto /openapi.json)
)

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================

# Incluir las rutas definidas en routes.py
# include_router() toma todas las rutas del router y las agrega a la aplicación principal
# Esto nos permite organizar las rutas en archivos separados para mejor mantenimiento
app.include_router(router)

# ============================================================================
# CONFIGURACIONES ADICIONALES (OPCIONAL)
# ============================================================================

# Aquí se pueden agregar configuraciones adicionales como:
# - Middleware para CORS (Cross-Origin Resource Sharing)
# - Middleware de autenticación
# - Configuración de base de datos
# - Manejo de errores globales
# - Configuración de logging

# Ejemplo de middleware CORS (comentado porque no es necesario para este ejemplo):
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # En producción, especificar dominios específicos
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ============================================================================
# INFORMACIÓN PARA EJECUTAR LA APLICACIÓN
# ============================================================================

"""
Para ejecutar esta aplicación:

1. Desde la terminal, en el directorio del proyecto:
   uvicorn main:app --reload
   
   Explicación del comando:
   - uvicorn: Servidor ASGI para aplicaciones Python
   - main: Nombre del archivo (main.py)
   - app: Nombre de la variable FastAPI en main.py
   - --reload: Reinicia automáticamente cuando detecta cambios en el código

2. La aplicación estará disponible en:
   - http://localhost:8000 (aplicación principal)
   - http://localhost:8000/docs (documentación Swagger)
   - http://localhost:8000/redoc (documentación ReDoc)
   - http://localhost:8000/openapi.json (esquema OpenAPI)

3. Para producción (sin --reload):
   uvicorn main:app --host 0.0.0.0 --port 8000

Notas para principiantes:
- Swagger y ReDoc son interfaces web automáticas para probar la API
- OpenAPI es un estándar para describir APIs REST
- ASGI es un estándar para aplicaciones web asíncronas en Python
- El flag --reload es solo para desarrollo, no usar en producción
"""