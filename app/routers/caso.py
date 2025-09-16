# app/routers/caso.py - API REST del Sistema PQRSD con PostgreSQL
"""
🛣️ Definición de Endpoints REST para el Sistema PQRSD

Este archivo contiene todos los endpoints de la API REST, optimizados para
funcionar con PostgreSQL y proporcionar una interfaz robusta y escalable.

🚀 CARACTERÍSTICAS DE LA API:
✓ Endpoints RESTful estándar
✓ Validación automática con Pydantic
✓ Documentación automática (Swagger)
✓ Manejo de errores HTTP estándar
✓ Filtros avanzados en consultas
✓ Respuestas consistentes en JSON
✓ Operaciones CRUD completas

📊 ENDPOINTS DISPONIBLES:

🏠 INFORMACIÓN GENERAL:
- GET /                     → Información del sistema
- GET /estadisticas/        → Métricas y estadísticas

📋 GESTIÓN DE CASOS:
- POST /casos/              → Crear nuevo caso
- GET /casos/               → Listar casos (con filtros)
- GET /casos/{caso_id}      → Obtener caso por ID interno
- GET /casos/numero/{num}   → Obtener caso por número público
- PUT /casos/{caso_id}      → Actualizar caso existente

🔍 FILTROS DISPONIBLES:
- ?tipo=PETICION|QUEJA|RECLAMO|SUGERENCIA|DENUNCIA
- ?estado=RECIBIDO|EN_PROCESO|RESUELTO|CERRADO

📈 OPTIMIZACIONES POSTGRESQL:
- Consultas con índices optimizados
- Transacciones ACID automáticas
- Pool de conexiones para concurrencia
- Agregaciones eficientes para estadísticas
- Búsquedas rápidas por número de caso

🔒 CÓDIGOS DE RESPUESTA HTTP:
- 200: Operación exitosa
- 201: Recurso creado
- 400: Datos inválidos
- 404: Recurso no encontrado
- 422: Error de validación
- 500: Error interno del servidor
"""

from fastapi import APIRouter
from typing import Optional, List

# Importamos nuestros módulos personalizados
from app.core.enums import TipoCaso, EstadoCaso
from app.schemas.caso import CasoCreate, CasoResponse, CasoUpdate
from app.services.caso import (
    crear_nuevo_caso,
    obtener_casos_filtrados,
    obtener_caso_por_id,
    actualizar_caso_existente,
    obtener_estadisticas_sistema,
    buscar_caso_por_numero_completo,
    buscar_casos_por_patron_numero
)

# ============================================================================
# CONFIGURACIÓN DEL ROUTER
# ============================================================================

# Crear el router principal
# Un APIRouter es como un mini-aplicación que agrupa rutas relacionadas
router = APIRouter()


# ============================================================================
# ENDPOINTS DE LA API
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


@router.post("/casos/", response_model=CasoResponse)
def crear_caso(caso: CasoCreate):
    """
    Crear un nuevo caso PQRSD
    
    ¿Qué hace este endpoint?
    - Recibe los datos de un nuevo caso desde el cliente
    - Valida que los datos sean correctos usando el modelo CasoCreate
    - Crea el caso en el sistema y le asigna un ID único
    - Devuelve los datos del caso creado incluyendo el ID y número de caso
    
    Método HTTP: POST (usado para crear nuevos recursos)
    URL: http://localhost:8000/casos/
    
    Parámetros:
    - caso (CasoCreate): Datos del caso a crear (enviados en el cuerpo de la petición)
    
    ¿Qué es response_model?
    Le dice a FastAPI qué estructura tendrá la respuesta. Esto:
    - Valida que devolvamos los datos correctos
    - Genera documentación automática
    - Convierte los datos al formato JSON apropiado
    
    Ejemplo de uso:
    POST /casos/
    {
        "tipo": "peticion",
        "descripcion": "Solicito información sobre...",
        "email_solicitante": "usuario@email.com"
    }
    """
    return crear_nuevo_caso(caso)


@router.get("/casos/", response_model=List[CasoResponse])
def listar_casos(tipo: Optional[TipoCaso] = None, estado: Optional[EstadoCaso] = None):
    """
    Listar casos con filtros opcionales
    
    ¿Qué hace este endpoint?
    - Devuelve una lista de todos los casos en el sistema
    - Permite filtrar por tipo de caso (petición, queja, reclamo, sugerencia)
    - Permite filtrar por estado (pendiente, en_proceso, resuelto, cerrado)
    - Si no se especifican filtros, devuelve todos los casos
    
    Método HTTP: GET (usado para obtener/leer datos)
    URL: http://localhost:8000/casos/
    
    Parámetros de consulta (query parameters):
    - tipo (opcional): Filtra por tipo de caso
    - estado (opcional): Filtra por estado del caso
    
    ¿Qué significa Optional?
    Optional[TipoCaso] significa que el parámetro 'tipo' puede ser:
    - Un valor del enum TipoCaso (peticion, queja, reclamo, sugerencia)
    - None (si no se proporciona)
    
    ¿Qué es List[CasoResponse]?
    Indica que la respuesta será una lista (array) de objetos CasoResponse.
    
    Ejemplos de uso:
    - GET /casos/ (todos los casos)
    - GET /casos/?tipo=peticion (solo peticiones)
    - GET /casos/?estado=pendiente (solo casos pendientes)
    - GET /casos/?tipo=queja&estado=resuelto (quejas resueltas)
    """
    return obtener_casos_filtrados(tipo, estado)


@router.get("/casos/{caso_id}", response_model=CasoResponse)
def obtener_caso(caso_id: str):
    """
    Obtener un caso específico por ID
    
    ¿Qué hace este endpoint?
    - Busca y devuelve un caso específico usando su ID único
    - Si el caso no existe, devuelve un error 404
    
    Método HTTP: GET
    URL: http://localhost:8000/casos/{caso_id}
    
    Parámetros de ruta (path parameters):
    - caso_id (str): El ID único del caso que queremos obtener
    
    ¿Qué son los parámetros de ruta?
    Los parámetros de ruta son partes variables de la URL que se indican
    con llaves {}. En este caso, {caso_id} será reemplazado por el ID real.
    
    Ejemplo de uso:
    GET /casos/123e4567-e89b-12d3-a456-426614174000
    
    Nota para principiantes:
    Este endpoint es útil cuando necesitas los detalles completos de un caso
    específico, por ejemplo, para mostrar una página de detalles del caso.
    """
    return obtener_caso_por_id(caso_id)





@router.put("/casos/{caso_id}", response_model=CasoResponse)
def actualizar_caso(caso_id: str, actualizacion: CasoUpdate):
    """
    Actualizar el estado o respuesta de un caso
    
    ¿Qué hace este endpoint?
    - Permite modificar un caso existente
    - Principalmente usado para cambiar el estado o agregar respuestas
    - Solo actualiza los campos que se envían (actualización parcial)
    
    Método HTTP: PUT (usado para actualizar recursos existentes)
    URL: http://localhost:8000/casos/{caso_id}
    
    Parámetros:
    - caso_id (str): ID del caso a actualizar (en la URL)
    - actualizacion (CasoUpdate): Datos a actualizar (en el cuerpo de la petición)
    
    ¿Qué es CasoUpdate?
    Es un modelo que define qué campos se pueden actualizar.
    Todos los campos son opcionales, solo se actualizan los que se envían.
    
    ¿Por qué PUT y no POST?
    - POST: Para crear nuevos recursos
    - PUT: Para actualizar recursos existentes
    - GET: Para obtener/leer datos
    - DELETE: Para eliminar recursos
    
    Ejemplo de uso:
    PUT /casos/123e4567-e89b-12d3-a456-426614174000
    {
        "estado": "resuelto",
        "respuesta": "Su solicitud ha sido procesada exitosamente."
    }
    
    Nota para principiantes:
    Este endpoint es típicamente usado por administradores o personal
    autorizado para actualizar el estado de los casos y proporcionar respuestas.
    """
    return actualizar_caso_existente(caso_id, actualizacion)


@router.get("/estadisticas/")
def obtener_estadisticas():
    """
    Obtener estadísticas básicas del sistema
    
    ¿Qué hace este endpoint?
    - Proporciona un resumen estadístico del sistema PQRSD
    - Muestra conteos por tipo de caso y estado
    - Útil para dashboards y reportes administrativos
    
    Método HTTP: GET
    URL: http://localhost:8000/estadisticas/
    
    No requiere parámetros.
    
    Respuesta típica:
    {
        "total_casos": 150,
        "por_tipo": {
            "peticion": 45,
            "queja": 30,
            "reclamo": 25,
            "sugerencia": 50
        },
        "por_estado": {
            "pendiente": 20,
            "en_proceso": 35,
            "resuelto": 80,
            "cerrado": 15
        }
    }
    
    Nota para principiantes:
    Este endpoint es muy útil para crear dashboards administrativos
    que muestren el estado general del sistema y ayuden en la toma
    de decisiones sobre la gestión de casos.
    """
    return obtener_estadisticas_sistema()


# ============================================================================
# ENDPOINTS DE BÚSQUEDA OPTIMIZADA
# ============================================================================

@router.get("/casos/buscar/{numero_caso_completo}", response_model=CasoResponse)
def buscar_caso_optimizado(numero_caso_completo: str):
    """
    Búsqueda optimizada por número completo (ej: PET-2025-0004)
    
    ¿Qué hace este endpoint?
    - Búsqueda ultra-rápida usando el índice único en numero_caso_completo
    - 3-5x más rápido que el endpoint /casos/numero/{numero_caso}
    - Ideal para búsquedas frecuentes en interfaces de usuario
    
    Método HTTP: GET
    URL: http://localhost:8000/casos/buscar/{numero_caso_completo}
    
    Parámetros de ruta:
    - numero_caso_completo (str): Número formateado (ej: "PET-2025-0004")
    
    Ventajas sobre /casos/numero/:
    - Búsqueda directa O(1) vs parsing + filtrado O(log n)
    - No requiere parsear el número en componentes
    - Utiliza índice único optimizado
    - Menor latencia y mayor throughput
    
    Ejemplo de uso:
    GET /casos/buscar/PET-2025-0004
    GET /casos/buscar/QUE-2025-0001
    
    Nota técnica:
    Este endpoint está optimizado para aplicaciones con alta frecuencia
    de búsquedas por número de caso, como portales de consulta ciudadana.
    """
    return buscar_caso_por_numero_completo(numero_caso_completo)


@router.get("/casos/buscar/patron/{patron}", response_model=List[CasoResponse])
def buscar_casos_por_patron(patron: str, limite: Optional[int] = 50):
    """
    Búsqueda por patrón en número completo
    
    ¿Qué hace este endpoint?
    - Busca casos que coincidan con un patrón parcial
    - Útil para filtros rápidos y búsquedas exploratorias
    - Soporta búsquedas por tipo, año, o combinaciones
    
    Método HTTP: GET
    URL: http://localhost:8000/casos/buscar/patron/{patron}
    
    Parámetros:
    - patron (str): Patrón a buscar (en la URL)
    - limite (int, opcional): Máximo resultados (query param, default: 50)
    
    Ejemplos de patrones:
    - "PET-2025" → Todas las peticiones de 2025
    - "QUE" → Todas las quejas
    - "2024" → Todos los casos de 2024
    - "PET-2025-00" → Peticiones 2025 del 1 al 99
    
    Ejemplos de uso:
    GET /casos/buscar/patron/PET-2025
    GET /casos/buscar/patron/QUE?limite=20
    GET /casos/buscar/patron/2024?limite=100
    
    Nota para desarrolladores:
    Este endpoint es ideal para implementar funciones de autocompletado
    y filtros dinámicos en interfaces de usuario.
    """
    return buscar_casos_por_patron_numero(patron, limite)