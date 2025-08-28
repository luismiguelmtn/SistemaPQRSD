# routes.py - Rutas y endpoints del Sistema PQRSD
"""
Este archivo define todas las rutas (endpoints) de la API REST del Sistema PQRSD.

¿Qué es una API REST?
Una API REST es una forma de comunicación entre aplicaciones usando HTTP.
Cada endpoint es una URL específica que acepta ciertos tipos de peticiones (GET, POST, PUT, etc.)
y devuelve datos en formato JSON.

¿Qué es un Router?
Un Router en FastAPI es como un organizador de rutas. Agrupa endpoints relacionados
y permite modularizar la aplicación. En lugar de tener todas las rutas en main.py,
las organizamos aquí y luego las incluimos en la aplicación principal.

Estructura de endpoints en este sistema:
- GET /: Página de bienvenida
- POST /casos/: Crear un nuevo caso
- GET /casos/: Listar todos los casos (con filtros opcionales)
- GET /casos/{caso_id}: Obtener un caso específico por su ID
- GET /casos/numero/{numero_caso}: Obtener un caso por su número público
- PUT /casos/{caso_id}: Actualizar un caso existente
- GET /estadisticas/: Obtener estadísticas del sistema
"""

from fastapi import APIRouter
from typing import Optional, List

# Importamos nuestros módulos personalizados
from enums import TipoCaso, EstadoCaso
from models import CasoCreate, CasoResponse, CasoUpdate
from services import (
    crear_nuevo_caso,
    obtener_casos_filtrados,
    obtener_caso_por_id,
    obtener_caso_por_numero,
    actualizar_caso_existente,
    obtener_estadisticas_sistema
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


@router.get("/casos/numero/{numero_caso}", response_model=CasoResponse) 
def obtener_caso_por_numero_endpoint(numero_caso: str):
    """
    Obtener un caso por su número (para consulta pública)
    
    ¿Qué hace este endpoint?
    - Permite buscar un caso usando su número público (ej: "CASO-001")
    - Es más amigable para usuarios finales que el ID interno
    - Útil para que los ciudadanos consulten el estado de sus casos
    
    Método HTTP: GET
    URL: http://localhost:8000/casos/numero/{numero_caso}
    
    Parámetros de ruta:
    - numero_caso (str): El número público del caso (ej: "CASO-001")
    
    ¿Por qué dos formas de buscar casos?
    - Por ID: Para uso interno del sistema (más eficiente)
    - Por número: Para uso público (más fácil de recordar y compartir)
    
    Ejemplo de uso:
    GET /casos/numero/CASO-001
    
    Nota para principiantes:
    Este endpoint es especialmente útil para crear una página de consulta
    pública donde los ciudadanos pueden verificar el estado de sus casos
    sin necesidad de recordar un ID complejo.
    """
    return obtener_caso_por_numero(numero_caso)


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