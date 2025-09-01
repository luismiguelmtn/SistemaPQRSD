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
from fastapi import HTTPException
from sqlalchemy import extract
from enums import TipoCaso, EstadoCaso
from models import CasoCreate, CasoUpdate
from database import get_database_session
from db_models import Caso


# ============================================================================
# BASE DE DATOS REAL CON SQLALCHEMY
# ============================================================================

# IMPORTANTE: Ahora usamos una base de datos real (SQLite)
# Los datos se guardan permanentemente en el archivo pqrsd_sistema.db
# Ya no necesitamos la lista en memoria casos_db


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_numero_caso(tipo: TipoCaso) -> str:
    """
    Genera un número único y legible para identificar un caso basado en su tipo.
    
    Formato: "XXX-YYYY-NNN" donde:
    - XXX: Prefijo según el tipo de caso
    - YYYY: Año actual
    - NNN: Número secuencial con 3 dígitos (001, 002, 003...)
    
    Prefijos por tipo:
    - PET: Peticiones
    - QUE: Quejas
    - REC: Reclamos
    - SUG: Sugerencias
    - DEN: Denuncias
    
    Ejemplos:
    - PET-2025-001 (Primera petición del 2025)
    - QUE-2025-005 (Quinta queja del 2025)
    - REC-2026-001 (Primer reclamo del 2026, reinicia contador)
    
    Args:
        tipo (TipoCaso): Tipo de caso para determinar el prefijo
        
    Returns:
        str: Número de caso único con formato tipo-año-secuencial
        
    Nota:
        El contador se reinicia cada año, permitiendo una mejor organización
        y evitando números excesivamente largos con el tiempo.
    """
    # Obtener el año actual para incluirlo en el número de caso
    año_actual = datetime.now().year

    # Mapeo de tipos de caso a prefijos legibles
    prefijos = {
        TipoCaso.PETICION: "PET",
        TipoCaso.QUEJA: "QUE", 
        TipoCaso.RECLAMO: "REC",
        TipoCaso.SUGERENCIA: "SUG",
        TipoCaso.DENUNCIA: "DEN"
    }
    
    # Obtener una sesión de base de datos para contar casos del mismo tipo
    with next(get_database_session()) as db:
        # Filtrar por tipo y año actual
        contador = db.query(Caso).filter(
            Caso.tipo == tipo,
            extract('year', Caso.fecha_creacion) == año_actual
        ).count() + 1
    
    # Generar número con formato: PREFIJO-AÑO-NNN
    return f"{prefijos[tipo]}-{año_actual}-{contador:03d}"


# ============================================================================
# OPERACIONES PRINCIPALES (CRUD)
# ============================================================================

def crear_nuevo_caso(caso_data: CasoCreate) -> Dict[str, Any]:
    """
    Crea un nuevo caso PQRSD en la base de datos.
    
    Esta función:
    1. Genera un número de caso legible basado en el tipo
    2. Crea un nuevo registro en la base de datos
    3. Asigna automáticamente el estado inicial "recibido"
    4. Las fechas se establecen automáticamente por la base de datos
    5. Retorna el caso creado convertido a diccionario
    
    Args:
        caso_data (CasoCreate): Datos del caso proporcionados por el usuario
        
    Returns:
        Dict[str, Any]: El caso creado con todos los campos completados
        
    Raises:
        HTTPException: Si hay un error al guardar en la base de datos
        
    Ejemplo:
        >>> caso_nuevo = CasoCreate(
        ...     tipo=TipoCaso.PETICION,
        ...     asunto="Solicitud de información",
        ...     descripcion="Necesito información sobre...",
        ...     nombre_solicitante="Juan Pérez",
        ...     email_solicitante="juan@email.com"
        ... )
        >>> caso_creado = crear_nuevo_caso(caso_nuevo)
        >>> print(caso_creado["numero_caso"])  # "PET-0001"
    """
    
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Generar número de caso público
            numero_caso = generar_numero_caso(caso_data.tipo)
            
            # Crear el objeto Caso usando el método from_pydantic
            nuevo_caso_db = Caso.from_pydantic(caso_data, numero_caso)
            
            # Agregar a la sesión y guardar en la base de datos
            db.add(nuevo_caso_db)
            db.commit()  # Confirmar los cambios
            db.refresh(nuevo_caso_db)  # Actualizar el objeto con datos de la DB (como el ID)
            
            # Convertir a diccionario para retornar
            return nuevo_caso_db.to_dict()
            
    except Exception as e:
        # Si hay cualquier error, lanzar una excepción HTTP
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear el caso: {str(e)}"
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
            
            # Convertir cada caso a diccionario
            return [caso.to_dict() for caso in casos_db]
            
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
            
            return caso.to_dict()
            
    except HTTPException:
        # Re-lanzar excepciones HTTP (como 404)
        raise
    except Exception as e:
        # Si hay cualquier otro error, lanzar una excepción HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar el caso: {str(e)}"
        )


def obtener_caso_por_numero(numero_caso: str) -> Dict[str, Any]:
    """
    Busca un caso específico por su número legible en la base de datos.
    
    El número de caso es el identificador que se muestra a los usuarios
    (ej: "PET-0001", "QUE-0005"). Es más fácil de recordar y comunicar que el UUID.
    
    Args:
        numero_caso (str): Número de caso a buscar (ej: "PET-0001")
        
    Returns:
        Dict[str, Any]: El caso encontrado
        
    Raises:
        HTTPException: Si el caso no existe (404) o hay error en la consulta
        
    Ejemplo:
        >>> try:
        ...     caso = obtener_caso_por_numero("PET-0001")
        ...     print(f"Estado: {caso['estado']}")
        ... except HTTPException:
        ...     print("Número de caso inválido")
    """
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Buscar el caso por número
            caso = db.query(Caso).filter(Caso.numero_caso == numero_caso).first()
            
            # Si no se encuentra, lanzar excepción HTTP 404
            if not caso:
                raise HTTPException(status_code=404, detail="Caso no encontrado")
            
            return caso.to_dict()
            
    except HTTPException:
        # Re-lanzar excepciones HTTP (como 404)
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
            
            return caso.to_dict()
            
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
            ultimo_numero = ultimo_caso.numero_caso if ultimo_caso else "Ninguno"
            
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
# NOTAS PARA PRINCIPIANTES
# ============================================================================

# 1. ¿Por qué usar SQLite como base de datos?
#    - Simplicidad: No requiere servidor separado como PostgreSQL, MySQL
#    - Persistencia: Los datos se guardan permanentemente en archivo
#    - Educativo: Fácil de entender SQL y operaciones de base de datos
#    - Portabilidad: Un solo archivo contiene toda la base de datos

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

# 5. En un sistema real, este archivo tendría:
#    - Conexión a base de datos (SQLAlchemy, Django ORM, etc.)
#    - Manejo de transacciones para operaciones atómicas
#    - Validaciones de negocio más complejas
#    - Logging de todas las operaciones
#    - Manejo de errores más robusto
#    - Paginación para listas grandes
#    - Índices para búsquedas rápidas
#    - Cache para consultas frecuentes
#    - Auditoría de cambios (quién, cuándo, qué cambió)