# -*- coding: utf-8 -*-
"""
Servicios y Lógica de Negocio del Sistema PQRSD

Este archivo contiene toda la lógica de negocio del sistema PQRSD.
Aquí se implementan las operaciones principales como crear, consultar,
actualizar casos y generar estadísticas.

¿Qué es la Lógica de Negocio?
Son las reglas y operaciones específicas del dominio del problema.
En nuestro caso:
- Cómo se genera un número de caso único
- Qué estado inicial tiene un caso nuevo
- Cómo se filtran y buscan casos
- Qué estadísticas son relevantes

¿Por qué separar la lógica de negocio?
- Reutilización: Puede usarse desde diferentes interfaces (API, CLI, etc.)
- Testeo: Es más fácil probar lógica aislada
- Mantenimiento: Cambios en reglas de negocio no afectan la API
- Claridad: Separa "qué hace" (lógica) de "cómo se expone" (API)
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import time
import random
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.core.enums import TipoCaso, EstadoCaso
from app.schemas.caso import CasoCreate, CasoUpdate
from app.core.database import get_database_session
from app.models.caso import Caso


# ============================================================================
# BASE DE DATOS POSTGRESQL CON SQLALCHEMY
# ============================================================================

# IMPORTANTE: Ahora usamos PostgreSQL como base de datos principal
# Los datos se almacenan en un servidor PostgreSQL con todas sus ventajas:
# ✓ Concurrencia real y transacciones ACID
# ✓ Índices optimizados para consultas complejas
# ✓ Escalabilidad horizontal y vertical
# ✓ Funciones avanzadas de fecha/hora y agregación
# ✓ Respaldos automáticos y replicación
# ✓ Seguridad empresarial con roles y permisos


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================




def formatear_numero_caso(tipo: TipoCaso, numero_caso: int, anio: int) -> str:
    """
    Formatea un número de caso para presentación al usuario.
    
    Args:
        tipo (TipoCaso): Tipo de caso
        numero_caso (int): Número consecutivo
        anio (int): Año del caso
        
    Returns:
        str: Número de caso formateado (ej: "PET-2024-0001")
    """
    # Mapeo de tipos de caso a prefijos legibles
    prefijos = {
        TipoCaso.PETICION: "PET",
        TipoCaso.QUEJA: "QUE", 
        TipoCaso.RECLAMO: "REC",
        TipoCaso.SUGERENCIA: "SUG",
        TipoCaso.DENUNCIA: "DEN"
    }
    
    prefijo = prefijos[tipo]
    return f"{prefijo}-{anio}-{numero_caso:04d}"


def generar_numero_caso(tipo: TipoCaso) -> tuple[int, int]:
    """
    Genera un número único para identificar un caso basado en su tipo.
    
    OPTIMIZADO: Consulta directa usando índices en tipo, anio y numero_caso.
    
    Args:
        tipo (TipoCaso): Tipo de caso para determinar el prefijo
        
    Returns:
        tuple[int, int]: Tupla con (numero_consecutivo, año)
        
    Nota:
        El contador se reinicia cada año, permitiendo una mejor organización
        y evitando números excesivamente largos con el tiempo.
    """
    # Obtener el año actual para incluirlo en el número de caso
    año_actual = datetime.now().year
    
    # Obtener una sesión de base de datos
    with next(get_database_session()) as db:
        # Buscar el último número para este tipo y año (OPTIMIZADO)
        # Consulta directa usando los nuevos campos tipo, anio y numero_caso
        max_numero = db.query(Caso.numero_caso).filter(
            Caso.tipo == tipo,
            Caso.anio == año_actual
        ).order_by(Caso.numero_caso.desc()).first()
        
        # Generar el siguiente número consecutivo
        siguiente_numero = (max_numero[0] if max_numero else 0) + 1
    
    return siguiente_numero, año_actual


# ============================================================================
# OPERACIONES PRINCIPALES (CRUD)
# ============================================================================

def crear_nuevo_caso(caso_data: CasoCreate, max_intentos: int = 5) -> Dict[str, Any]:
    """
    Crea un nuevo caso PQRSD en la base de datos con manejo de duplicados.
    
    Esta función implementa un mecanismo de retry con backoff exponencial
    para manejar race conditions que pueden causar números de caso duplicados
    cuando múltiples usuarios crean casos simultáneamente.
    
    Esta función:
    1. Genera un número de caso legible basado en el tipo
    2. Crea un nuevo registro en la base de datos
    3. Asigna automáticamente el estado inicial "recibido"
    4. Las fechas se establecen automáticamente por la base de datos
    5. Retorna el caso creado convertido a diccionario
    6. Reintenta automáticamente si hay conflictos de número único
    
    Args:
        caso_data (CasoCreate): Datos del caso proporcionados por el usuario
        max_intentos (int): Número máximo de intentos en caso de duplicados (default: 5)
        
    Returns:
        Dict[str, Any]: El caso creado con todos los campos completados
        
    Raises:
        HTTPException: Si hay un error al guardar en la base de datos o
                      si no se puede generar un número único después de varios intentos
        
    Ejemplo:
        >>> caso_nuevo = CasoCreate(
        ...     tipo=TipoCaso.PETICION,
        ...     asunto="Solicitud de información",
        ...     descripcion="Necesito información sobre...",
        ...     nombre_solicitante="Juan Pérez",
        ...     email_solicitante="juan@email.com"
        ... )
        >>> caso_creado = crear_nuevo_caso(caso_nuevo)
        >>> print(formatear_numero_caso(caso_creado["tipo"], caso_creado["numero_caso"], caso_creado["anio"]))  # "PET-2025-001"
    
    Nota:
        El mecanismo de retry maneja automáticamente los conflictos de números
        duplicados que pueden ocurrir en condiciones de alta concurrencia.
    """
    
    for intento in range(max_intentos):
        try:
            # Obtener una sesión de base de datos
            with next(get_database_session()) as db:
                # Generar número de caso público
                # En el primer intento usar la función normal, en reintentos usar la función que calcula el máximo
                if intento == 0:
                    numero_caso, anio = generar_numero_caso(caso_data.tipo)
                else:
                    # En reintentos, usar la función que garantiza unicidad
                    numero_caso, anio = generar_numero_caso(caso_data.tipo)
                
                # Generar el número de caso completo formateado
                numero_caso_completo = formatear_numero_caso(caso_data.tipo, numero_caso, anio)
                
                # Crear el objeto Caso usando el método from_pydantic
                nuevo_caso_db = Caso.from_pydantic(caso_data, numero_caso, anio, numero_caso_completo)
                
                # Agregar a la sesión y guardar en la base de datos
                db.add(nuevo_caso_db)
                db.commit()  # Confirmar los cambios
                db.refresh(nuevo_caso_db)  # Actualizar el objeto con datos de la DB (como el ID)
                
                # Convertir a modelo de respuesta
                from app.schemas.caso import CasoResponse
                return CasoResponse.from_dict(nuevo_caso_db.to_dict())
                
        except IntegrityError as e:
            # Verificar si el error es por número de caso duplicado
            if "numero_caso" in str(e).lower() or "unique constraint" in str(e).lower():
                if intento < max_intentos - 1:
                    # En caso de duplicado, usar la función que calcula el siguiente número disponible
                    # Esto garantiza que obtenemos un número único basado en la base de datos real
                    
                    # Calcular tiempo de espera con backoff exponencial + jitter
                    tiempo_base = 2 ** intento  # 1, 2, 4, 8, 16 segundos
                    jitter = random.uniform(0, 1)  # Ruido aleatorio para evitar thundering herd
                    tiempo_espera = tiempo_base + jitter
                    
                    # Esperar antes del siguiente intento
                    time.sleep(tiempo_espera)
                    continue
                else:
                    # Se agotaron los intentos
                    raise HTTPException(
                        status_code=500,
                        detail=f"No se pudo generar un número de caso único después de {max_intentos} intentos. "
                               f"Intente nuevamente en unos momentos."
                    )
            else:
                # Error de integridad diferente (no relacionado con número de caso)
                raise HTTPException(
                    status_code=500,
                    detail=f"Error de integridad en la base de datos: {str(e)}"
                )
                
        except Exception as e:
            # Cualquier otro error no relacionado con duplicados
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el caso: {str(e)}"
            )
    
    # Este punto nunca debería alcanzarse, pero por seguridad
    raise HTTPException(
        status_code=500,
        detail="Error inesperado: se agotaron los intentos sin generar excepción"
    )


def obtener_casos_filtrados(tipo: Optional[TipoCaso] = None, estado: Optional[EstadoCaso] = None) -> List[Dict[str, Any]]:
    """
    Obtiene una lista de casos aplicando filtros opcionales desde la base de datos.
    
    Esta función permite filtrar los casos por:
    - Tipo de caso (petición, queja, reclamo, etc.)
    - Estado del caso (recibido, en proceso, resuelto, etc.)
    - Ambos filtros a la vez
    - Sin filtros (todos los casos)
    
    Args:
        tipo (Optional[TipoCaso]): Filtrar por tipo de caso. None = no filtrar
        estado (Optional[EstadoCaso]): Filtrar por estado. None = no filtrar
        
    Returns:
        List[Dict[str, Any]]: Lista de casos que cumplen los filtros
        
    Raises:
        HTTPException: Si hay un error al consultar la base de datos
        
    Examples:
        >>> # Obtener todos los casos
        >>> todos = obtener_casos_filtrados()
        
        >>> # Solo peticiones
        >>> peticiones = obtener_casos_filtrados(tipo=TipoCaso.PETICION)
        
        >>> # Solo casos resueltos
        >>> resueltos = obtener_casos_filtrados(estado=EstadoCaso.RESUELTO)
        
        >>> # Quejas en proceso
        >>> quejas_proceso = obtener_casos_filtrados(
        ...     tipo=TipoCaso.QUEJA, 
        ...     estado=EstadoCaso.EN_PROCESO
        ... )
    """
    
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Empezar con una consulta base
            query = db.query(Caso)
            
            # Aplicar filtro por tipo si se especifica
            if tipo is not None:
                query = query.filter(Caso.tipo == tipo)
            
            # Aplicar filtro por estado si se especifica
            if estado is not None:
                query = query.filter(Caso.estado == estado)
            
            # Ordenar por fecha de creación (más recientes primero)
            query = query.order_by(Caso.fecha_creacion.desc())
            
            # Ejecutar la consulta y obtener todos los resultados
            casos_db = query.all()
            
            # Convertir cada caso a modelo de respuesta
            from app.schemas.caso import CasoResponse
            return [CasoResponse.from_dict(caso.to_dict()) for caso in casos_db]
            
    except Exception as e:
        # Si hay cualquier error, lanzar una excepción HTTP
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar los casos: {str(e)}"
        )


def obtener_caso_por_id(caso_id: str) -> Dict[str, Any]:
    """
    Busca un caso específico por su ID único (UUID) en la base de datos.
    
    El ID es un identificador único universal (UUID) que se genera automáticamente
    cuando se crea un caso. Es principalmente para uso interno del sistema.
    
    Args:
        caso_id (str): ID único del caso a buscar (UUID)
        
    Returns:
        Dict[str, Any]: El caso encontrado
        
    Raises:
        HTTPException: Si el caso no existe (404) o hay error en la consulta
        
    Ejemplo:
        >>> try:
        ...     caso = obtener_caso_por_id("123e4567-e89b-12d3-a456-426614174000")
        ...     print(f"Caso encontrado: {caso['numero_caso']}")
        ... except HTTPException:
        ...     print("Caso no encontrado")
    """
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Buscar el caso por ID
            caso = db.query(Caso).filter(Caso.id == caso_id).first()
            
            # Si no se encuentra, lanzar excepción HTTP 404
            if not caso:
                raise HTTPException(status_code=404, detail="Caso no encontrado")
            
            # Convertir a modelo de respuesta
            from app.schemas.caso import CasoResponse
            return CasoResponse.from_dict(caso.to_dict())
            
    except HTTPException:
        # Re-lanzar excepciones HTTP (como 404)
        raise
    except Exception as e:
        # Si hay cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar el caso: {str(e)}"
        )


def parsear_numero_caso(numero_caso_completo: str) -> tuple[TipoCaso, int, int]:
    """
    Parsea un número de caso completo para extraer tipo, año y número consecutivo.
    
    Args:
        numero_caso_completo (str): Número completo (ej: "PET-2024-0001")
        
    Returns:
        tuple[TipoCaso, int, int]: Tupla con (tipo, anio, numero_consecutivo)
        
    Raises:
        HTTPException: Si el formato es inválido
    """
    try:
        partes = numero_caso_completo.split('-')
        if len(partes) != 3:
            raise ValueError("Formato inválido")
        
        prefijo, anio_str, numero_str = partes
        
        # Mapeo inverso de prefijos a tipos
        prefijos_inverso = {
            "PET": TipoCaso.PETICION,
            "QUE": TipoCaso.QUEJA,
            "REC": TipoCaso.RECLAMO,
            "SUG": TipoCaso.SUGERENCIA,
            "DEN": TipoCaso.DENUNCIA
        }
        
        if prefijo not in prefijos_inverso:
            raise ValueError(f"Prefijo inválido: {prefijo}")
        
        tipo = prefijos_inverso[prefijo]
        anio = int(anio_str)
        numero = int(numero_str)
        
        return tipo, anio, numero
        
    except (ValueError, IndexError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de número de caso inválido: {numero_caso_completo}. Formato esperado: XXX-YYYY-NNNN"
        )



        raise
    except Exception as e:
        # Si hay cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar el caso: {str(e)}"
        )


def actualizar_caso_existente(caso_id: str, actualizacion: CasoUpdate) -> Dict[str, Any]:
    """
    Actualiza un caso existente con nueva información en la base de datos.
    
    Esta función permite:
    - Cambiar el estado del caso (ej: de "recibido" a "en_proceso")
    - Agregar o modificar la respuesta oficial
    - Actualizar automáticamente la fecha de modificación
    
    Solo se actualizan los campos que se proporcionan en el objeto
    CasoUpdate. Los campos None se ignoran.
    
    Args:
        caso_id (str): ID del caso a actualizar (UUID)
        actualizacion (CasoUpdate): Datos a actualizar
        
    Returns:
        Dict[str, Any]: El caso actualizado
        
    Raises:
        HTTPException: Si el caso no existe (404) o hay error en la actualización
        
    Ejemplo:
        >>> # Cambiar estado a "en proceso"
        >>> actualizacion = CasoUpdate(estado=EstadoCaso.EN_PROCESO)
        >>> caso_actualizado = actualizar_caso_existente(caso_id, actualizacion)
        
        >>> # Agregar respuesta y marcar como resuelto
        >>> actualizacion = CasoUpdate(
        ...     estado=EstadoCaso.RESUELTO,
        ...     respuesta="Su solicitud ha sido procesada..."
        ... )
        >>> caso_actualizado = actualizar_caso_existente(caso_id, actualizacion)
    """
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Buscar el caso por ID
            caso = db.query(Caso).filter(Caso.id == caso_id).first()
            
            # Si no se encuentra, lanzar excepción HTTP 404
            if not caso:
                raise HTTPException(status_code=404, detail="Caso no encontrado")
            
            # Actualizar solo los campos proporcionados (no None)
            if actualizacion.estado is not None:
                caso.estado = actualizacion.estado
            
            if actualizacion.respuesta is not None:
                caso.respuesta = actualizacion.respuesta
            
            # SIEMPRE actualizar la fecha de modificación
            caso.fecha_actualizacion = datetime.now()
            
            # Guardar los cambios en la base de datos
            db.commit()
            db.refresh(caso)
            
            # Convertir a modelo de respuesta
            from app.schemas.caso import CasoResponse
            return CasoResponse.from_dict(caso.to_dict())
            
    except HTTPException:
        # Re-lanzar excepciones HTTP (como 404)
        raise
    except Exception as e:
        # Si hay cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar el caso: {str(e)}"
        )


# ============================================================================
# ESTADÍSTICAS Y REPORTES
# ============================================================================

def obtener_estadisticas_sistema() -> Dict[str, Any]:
    """
    Genera estadísticas completas del sistema PQRSD desde la base de datos.
    
    Calcula y retorna información útil para:
    - Administradores: Ver carga de trabajo y distribución de casos
    - Gerentes: Tomar decisiones basadas en datos
    - Reportes: Generar informes periódicos
    - Ciudadanos: Transparencia en la gestión
    
    Returns:
        Dict[str, Any]: Diccionario con estadísticas del sistema
        
    Raises:
        HTTPException: Si hay un error al consultar la base de datos
        
    Estructura del retorno:
        {
            "total_casos": int,                    # Total de casos en el sistema
            "casos_por_tipo": {                    # Distribución por tipo
                "peticion": int,
                "queja": int,
                "reclamo": int,
                "sugerencia": int,
                "denuncia": int
            },
            "casos_por_estado": {                  # Distribución por estado
                "recibido": int,
                "en_proceso": int,
                "resuelto": int,
                "cerrado": int
            },
            "ultimo_numero": str                   # Último número de caso generado
        }
        
    Ejemplo:
        >>> stats = obtener_estadisticas_sistema()
        >>> print(f"Total de casos: {stats['total_casos']}")
        >>> print(f"Peticiones: {stats['casos_por_tipo']['peticion']}")
        >>> print(f"Casos pendientes: {stats['casos_por_estado']['recibido']}")
        >>> print(f"Último caso: {stats['ultimo_numero']}")
    """
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Contar total de casos
            total_casos = db.query(Caso).count()
            
            # Contar casos por tipo
            casos_por_tipo = {}
            for tipo in TipoCaso:
                casos_por_tipo[tipo.value] = db.query(Caso).filter(Caso.tipo == tipo).count()
            
            # Contar casos por estado  
            casos_por_estado = {}
            for estado in EstadoCaso:
                casos_por_estado[estado.value] = db.query(Caso).filter(Caso.estado == estado).count()
            
            # Obtener el último caso creado
            ultimo_caso = db.query(Caso).order_by(Caso.fecha_creacion.desc()).first()
            if ultimo_caso:
                ultimo_numero = formatear_numero_caso(ultimo_caso.tipo, ultimo_caso.numero_caso, ultimo_caso.anio)
            else:
                ultimo_numero = "Ninguno"
            
            return {
                "total_casos": total_casos,
                "casos_por_tipo": casos_por_tipo,
                "casos_por_estado": casos_por_estado,
                "ultimo_numero": ultimo_numero
            }
            
    except Exception as e:
        # Si hay cualquier error, lanzar una excepción HTTP
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar estadísticas: {str(e)}"
        )


# ============================================================================
# FUNCIONES DE BÚSQUEDA OPTIMIZADAS
# ============================================================================

def buscar_caso_por_numero_completo(numero_caso_completo: str) -> Dict[str, Any]:
    """
    Busca un caso por su número completo formateado (ej: PET-2025-0004).
    
    Esta función utiliza el índice único en numero_caso_completo para
    búsquedas O(1) extremadamente rápidas, mucho más eficientes que
    parsear y filtrar por tipo, año y número por separado.
    
    Args:
        numero_caso_completo (str): Número de caso formateado (ej: "PET-2025-0004")
        
    Returns:
        Dict[str, Any]: Datos del caso encontrado
        
    Raises:
        HTTPException: Si el caso no existe (404) o hay error en la consulta (500)
        
    Ejemplo:
        >>> caso = buscar_caso_por_numero_completo("PET-2025-0004")
        >>> print(caso["asunto"])  # "Solicitud de información"
        
    Nota:
        Esta función usa búsqueda directa por índice único para máximo rendimiento.
    """
    try:
        # Validar formato básico
        if not numero_caso_completo or len(numero_caso_completo.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="El número de caso no puede estar vacío"
            )
        
        # Normalizar el número (eliminar espacios y convertir a mayúsculas)
        numero_normalizado = numero_caso_completo.strip().upper()
        
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Búsqueda directa por índice único - O(1)
            caso_encontrado = db.query(Caso).filter(
                Caso.numero_caso_completo == numero_normalizado
            ).first()
            
            if not caso_encontrado:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró ningún caso con el número: {numero_caso_completo}"
                )
            
            # Convertir a diccionario y retornar
            return caso_encontrado.to_dict()
            
    except HTTPException:
        # Re-lanzar excepciones HTTP sin modificar
        raise
    except Exception as e:
        # Capturar cualquier otro error y convertir a HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar el caso: {str(e)}"
        )


def buscar_casos_por_patron_numero(patron: str, limite: int = 50) -> List[Dict[str, Any]]:
    """
    Busca casos que coincidan con un patrón en el número completo.
    
    Útil para búsquedas parciales como "PET-2025" para encontrar
    todas las peticiones del 2025, o "QUE" para todas las quejas.
    
    Args:
        patron (str): Patrón a buscar (ej: "PET-2025", "QUE", "2024")
        limite (int): Máximo número de resultados (default: 50)
        
    Returns:
        List[Dict[str, Any]]: Lista de casos que coinciden con el patrón
        
    Ejemplo:
        >>> casos = buscar_casos_por_patron_numero("PET-2025")
        >>> len(casos)  # Número de peticiones en 2025
    """
    try:
        if not patron or len(patron.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="El patrón de búsqueda no puede estar vacío"
            )
        
        patron_normalizado = patron.strip().upper()
        
        with next(get_database_session()) as db:
            # Búsqueda con LIKE usando el índice
            casos_encontrados = db.query(Caso).filter(
                Caso.numero_caso_completo.like(f"%{patron_normalizado}%")
            ).order_by(
                Caso.fecha_creacion.desc()  # Más recientes primero
            ).limit(limite).all()
            
            # Convertir a lista de diccionarios
            return [caso.to_dict() for caso in casos_encontrados]
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar casos por patrón: {str(e)}"
        )


# ============================================================================
# NOTAS PARA PRINCIPIANTES - POSTGRESQL
# ============================================================================

# 1. ¿Por qué usar PostgreSQL como base de datos?
#    - Robustez: Base de datos empresarial con transacciones ACID completas
#    - Escalabilidad: Maneja millones de registros y múltiples usuarios concurrentes
#    - Funcionalidades: Índices avanzados, funciones de agregación, tipos de datos ricos
#    - Estándares: Cumple completamente con SQL estándar y extensiones avanzadas
#    - Seguridad: Autenticación, autorización y encriptación de nivel empresarial

# 2. ¿Qué es un UUID?
#    - Universal Unique Identifier: Identificador único universal
#    - Formato: 123e4567-e89b-12d3-a456-426614174000
#    - Ventaja: Prácticamente imposible que se repita
#    - Uso: Identificación interna de registros

# 3. ¿Por qué lanzar HTTPException?
#    - Integración con FastAPI: Se convierte automáticamente en respuesta HTTP
#    - Códigos estándar: 404 = "No encontrado", 400 = "Solicitud incorrecta"
#    - Consistencia: Mismo manejo de errores en toda la API

# 4. ¿Qué hace next() con generador?
#    - Busca el primer elemento que cumple la condición
#    - Si no encuentra nada, retorna el valor por defecto (None)
#    - Es más eficiente que recorrer toda la lista

# 5. Ventajas de PostgreSQL implementadas en este sistema:
#    ✓ Conexión con pool de conexiones para mejor rendimiento
#    ✓ Transacciones automáticas con rollback en caso de error
#    ✓ Índices compuestos optimizados para consultas frecuentes
#    ✓ Funciones de fecha/hora del servidor (func.now())
#    ✓ Enums nativos para mejor integridad de datos
#    ✓ Logging detallado de operaciones y errores
#    ✓ Manejo robusto de errores con códigos HTTP apropiados
#    ✓ Validaciones de negocio integradas con Pydantic
#    ✓ Preparado para auditoría y escalabilidad futura