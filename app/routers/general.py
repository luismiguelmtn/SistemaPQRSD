# app/routers/general.py - Endpoints generales del Sistema PQRSD
"""
🏠 Endpoints Generales del Sistema PQRSD

Este archivo contiene los endpoints generales que no están específicamente
relacionados con la gestión de casos, como información del sistema y estadísticas.

📊 ENDPOINTS DISPONIBLES:

🏠 INFORMACIÓN GENERAL:
- GET /                     → Información del sistema
- GET /estadisticas/        → Métricas y estadísticas
"""

from fastapi import APIRouter
from app.services.caso import obtener_estadisticas_sistema

# ============================================================================
# CONFIGURACIÓN DEL ROUTER GENERAL
# ============================================================================

router = APIRouter(
    tags=["General"],
    responses={404: {"description": "No encontrado"}}
)

# ============================================================================
# ENDPOINTS GENERALES
# ============================================================================

@router.get("/")
def root():
    """
    Endpoint raíz - Página de bienvenida de la API
    
    ¿Qué hace este endpoint?
    - Proporciona información básica sobre la API
    - Es útil para verificar que el servidor está funcionando
    - Indica dónde encontrar la documentación automática
    
    Método HTTP: GET
    URL: http://localhost:8000/
    
    Respuesta:
    {
        "mensaje": "Bienvenido al Sistema PQRSD",
        "version": "1.0.0", 
        "documentacion": "/docs"
    }
    """
    return {
        "mensaje": "Bienvenido al Sistema PQRSD", 
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@router.get("/estadisticas/")
def obtener_estadisticas():
    """
    Obtener estadísticas del sistema
    
    ¿Qué hace este endpoint?
    - Calcula y devuelve métricas importantes del sistema
    - Muestra conteos por tipo de caso y estado
    - Útil para dashboards y reportes administrativos
    
    Método HTTP: GET
    URL: http://localhost:8000/estadisticas/
    
    Respuesta típica:
    {
        "total_casos": 150,
        "casos_por_tipo": {
            "peticion": 45,
            "queja": 30,
            "reclamo": 25,
            "sugerencia": 35,
            "denuncia": 15
        },
        "casos_por_estado": {
            "recibido": 20,
            "en_proceso": 45,
            "resuelto": 70,
            "cerrado": 15
        }
    }
    
    Nota para principiantes:
    Este endpoint es muy útil para crear dashboards administrativos
    que muestren el estado general del sistema PQRSD.
    """
    return obtener_estadisticas_sistema()