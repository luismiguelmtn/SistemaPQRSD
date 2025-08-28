# main.py - Sistema PQRSD Básico
"""
Este es el archivo principal de la aplicación FastAPI del Sistema PQRSD.

¿Qué hace este archivo?
Este archivo es el punto de entrada de nuestra aplicación. Aquí:
1. Creamos la instancia principal de FastAPI
2. Configuramos los metadatos de la aplicación (título, descripción, versión)
3. Incluimos todas las rutas definidas en otros módulos
4. Configuramos cualquier middleware o configuración global

¿Qué es FastAPI?
FastAPI es un framework web moderno y rápido para construir APIs con Python.
Sus principales características son:
- Muy rápido (comparable a NodeJS y Go)
- Fácil de usar y aprender
- Genera documentación automática
- Validación automática de datos
- Soporte nativo para async/await
- Basado en estándares como OpenAPI y JSON Schema

¿Qué es una API?
Una API (Application Programming Interface) es un conjunto de reglas y protocolos
que permite que diferentes aplicaciones se comuniquen entre sí. En nuestro caso,
creamos una API REST que puede ser consumida por:
- Aplicaciones web (frontend)
- Aplicaciones móviles
- Otros sistemas
- Herramientas de testing

Estructura del proyecto:
- main.py: Configuración principal de la aplicación
- routes.py: Definición de endpoints/rutas
- models.py: Modelos de datos (esquemas)
- services.py: Lógica de negocio
- enums.py: Enumeraciones y constantes
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================

from fastapi import FastAPI
from routes import router  # Importamos todas las rutas definidas en routes.py

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