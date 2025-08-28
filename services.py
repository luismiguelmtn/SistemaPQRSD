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
import uuid
from fastapi import HTTPException

from enums import TipoCaso, EstadoCaso
from models import CasoCreate, CasoUpdate


# ============================================================================
# BASE DE DATOS EN MEMORIA
# ============================================================================

# IMPORTANTE: Esta es una "base de datos" temporal en memoria
# En un sistema real, esto sería una base de datos como PostgreSQL, MySQL, etc.
# Los datos se pierden cuando se reinicia el servidor
casos_db: List[Dict[str, Any]] = []  # Lista que almacena todos los casos


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_numero_caso(tipo: TipoCaso) -> str:
    """
    Genera un número único y legible para identificar un caso basado en su tipo.
    
    Formato: "XXX-NNNN" donde:
    - XXX: Prefijo según el tipo de caso
    - NNNN: Número secuencial con 4 dígitos (0001, 0002, 0003...)
    
    Prefijos por tipo:
    - PET: Peticiones
    - QUE: Quejas
    - REC: Reclamos
    - SUG: Sugerencias
    - DEN: Denuncias
    
    Ejemplos:
    - PET-0001 (Primera petición)
    - QUE-0005 (Quinta queja)
    - REC-0012 (Reclamo número 12)
    
    Args:
        tipo (TipoCaso): Tipo de caso para determinar el prefijo
        
    Returns:
        str: Número de caso único con formato tipo-específico
        
    Nota:
        En un sistema real, podrías incluir:
        - Año actual (ej: PET-2024-0001)
        - Código de la entidad (ej: ALCALDIA-PET-0001)
        - Sede o dependencia (ej: PET-BOG-0001)
    """
    # Mapeo de tipos de caso a prefijos legibles
    prefijos = {
        TipoCaso.PETICION: "PET",
        TipoCaso.QUEJA: "QUE", 
        TipoCaso.RECLAMO: "REC",
        TipoCaso.SUGERENCIA: "SUG",
        TipoCaso.DENUNCIA: "DEN"
    }
    
    # Contar cuántos casos del mismo tipo ya existen
    contador = len([c for c in casos_db if c["tipo"] == tipo]) + 1
    
    # Generar número con formato: PREFIJO-NNNN
    return f"{prefijos[tipo]}-{contador:04d}"


# ============================================================================
# OPERACIONES PRINCIPALES (CRUD)
# ============================================================================

def crear_nuevo_caso(caso_data: CasoCreate) -> Dict[str, Any]:
    """
    Crea un nuevo caso PQRSD en el sistema.
    
    Esta función:
    1. Genera un ID único (entero secuencial) para el caso
    2. Genera un número de caso legible basado en el tipo
    3. Asigna el estado inicial "RECIBIDO"
    4. Establece las fechas de creación y actualización
    5. Almacena el caso en la "base de datos"
    6. Retorna el caso creado completo
    
    Args:
        caso_data (CasoCreate): Datos del caso proporcionados por el usuario
        
    Returns:
        Dict[str, Any]: El caso creado con todos los campos completos
        
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
    # Generar ID secuencial (el siguiente número disponible)
    nuevo_id = len(casos_db) + 1
    
    # Crear diccionario con todos los datos del caso
    nuevo_caso = {
        "id": nuevo_id,                             # ID único interno (entero secuencial)
        "numero_caso": generar_numero_caso(caso_data.tipo),  # Número legible para usuarios
        "tipo": caso_data.tipo,                     # Tipo de caso (enum)
        "asunto": caso_data.asunto,                 # Título del caso
        "descripcion": caso_data.descripcion,       # Descripción detallada
        "nombre_solicitante": caso_data.nombre_solicitante,
        "email_solicitante": caso_data.email_solicitante,
        "telefono_solicitante": caso_data.telefono_solicitante,
        "estado": EstadoCaso.RECIBIDO,              # Estado inicial siempre "RECIBIDO"
        "fecha_creacion": datetime.now(),          # Cuándo se creó
        "fecha_actualizacion": datetime.now(),     # Última modificación (igual a creación)
        "respuesta": None                           # Sin respuesta inicial
    }
    
    # Guardar en la "base de datos" (lista en memoria)
    casos_db.append(nuevo_caso)
    
    return nuevo_caso


def obtener_casos_filtrados(tipo: Optional[TipoCaso] = None, estado: Optional[EstadoCaso] = None) -> List[Dict[str, Any]]:
    """
    Obtiene una lista de casos con filtros opcionales.
    
    Esta función permite:
    - Obtener todos los casos (sin filtros)
    - Filtrar por tipo de caso (peticiones, quejas, etc.)
    - Filtrar por estado (recibido, en proceso, etc.)
    - Combinar ambos filtros
    
    Args:
        tipo (Optional[TipoCaso]): Filtrar por tipo de caso (opcional)
        estado (Optional[EstadoCaso]): Filtrar por estado (opcional)
        
    Returns:
        List[Dict[str, Any]]: Lista de casos que cumplen los filtros
        
    Ejemplos:
        >>> # Obtener todos los casos
        >>> todos = obtener_casos_filtrados()
        
        >>> # Obtener solo peticiones
        >>> peticiones = obtener_casos_filtrados(tipo=TipoCaso.PETICION)
        
        >>> # Obtener casos en proceso
        >>> en_proceso = obtener_casos_filtrados(estado=EstadoCaso.EN_PROCESO)
        
        >>> # Obtener quejas resueltas
        >>> quejas_resueltas = obtener_casos_filtrados(
        ...     tipo=TipoCaso.QUEJA, 
        ...     estado=EstadoCaso.RESUELTO
        ... )
    """
    # Empezar con todos los casos
    casos_filtrados = casos_db.copy()
    
    # Aplicar filtro por tipo si se proporciona
    if tipo:
        casos_filtrados = [c for c in casos_filtrados if c["tipo"] == tipo]
    
    # Aplicar filtro por estado si se proporciona
    if estado:
        casos_filtrados = [c for c in casos_filtrados if c["estado"] == estado]
    
    return casos_filtrados


def obtener_caso_por_id(caso_id: str) -> Dict[str, Any]:
    """
    Busca un caso específico por su ID único (UUID).
    
    El ID es un identificador único universal (UUID) que se genera automáticamente
    cuando se crea un caso. Es principalmente para uso interno del sistema.
    
    Args:
        caso_id (str): ID único del caso a buscar (UUID)
        
    Returns:
        Dict[str, Any]: El caso encontrado
        
    Raises:
        HTTPException: Si el caso no existe (404)
        
    Ejemplo:
        >>> try:
        ...     caso = obtener_caso_por_id("123e4567-e89b-12d3-a456-426614174000")
        ...     print(f"Caso encontrado: {caso['numero_caso']}")
        ... except HTTPException:
        ...     print("Caso no encontrado")
    """
    # Buscar el caso en la "base de datos"
    caso = next((c for c in casos_db if c["id"] == caso_id), None)
    
    # Si no se encuentra, lanzar excepción HTTP 404
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    return caso


def obtener_caso_por_numero(numero_caso: str) -> Dict[str, Any]:
    """
    Busca un caso específico por su número legible.
    
    El número de caso es el identificador que se muestra a los usuarios
    (ej: "PET-0001", "QUE-0005"). Es más fácil de recordar y comunicar que el UUID.
    
    Args:
        numero_caso (str): Número de caso a buscar (ej: "PET-0001")
        
    Returns:
        Dict[str, Any]: El caso encontrado
        
    Raises:
        HTTPException: Si el caso no existe (404)
        
    Ejemplo:
        >>> try:
        ...     caso = obtener_caso_por_numero("PET-0001")
        ...     print(f"Estado: {caso['estado']}")
        ... except HTTPException:
        ...     print("Número de caso inválido")
    """
    # Buscar el caso en la "base de datos"
    caso = next((c for c in casos_db if c["numero_caso"] == numero_caso), None)
    
    # Si no se encuentra, lanzar excepción HTTP 404
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    return caso


def actualizar_caso_existente(caso_id: str, actualizacion: CasoUpdate) -> Dict[str, Any]:
    """
    Actualiza un caso existente con nueva información.
    
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
        HTTPException: Si el caso no existe (404)
        
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
    # Buscar el caso en la "base de datos"
    caso = next((c for c in casos_db if c["id"] == caso_id), None)
    
    # Si no se encuentra, lanzar excepción HTTP 404
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    # Actualizar solo los campos proporcionados (no None)
    if actualizacion.estado:
        caso["estado"] = actualizacion.estado
    
    if actualizacion.respuesta:
        caso["respuesta"] = actualizacion.respuesta
    
    # SIEMPRE actualizar la fecha de modificación
    caso["fecha_actualizacion"] = datetime.now()
    
    return caso


# ============================================================================
# ESTADÍSTICAS Y REPORTES
# ============================================================================

def obtener_estadisticas_sistema() -> Dict[str, Any]:
    """
    Genera estadísticas completas del sistema PQRSD.
    
    Calcula y retorna información útil para:
    - Administradores: Ver carga de trabajo y distribución de casos
    - Gerentes: Tomar decisiones basadas en datos
    - Reportes: Generar informes periódicos
    - Ciudadanos: Transparencia en la gestión
    
    Returns:
        Dict[str, Any]: Diccionario con estadísticas del sistema
        
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
    total_casos = len(casos_db)
    
    # Contar casos por tipo
    casos_por_tipo = {}
    for tipo in TipoCaso:
        # Contar cuántos casos hay de cada tipo
        casos_por_tipo[tipo.value] = len([c for c in casos_db if c["tipo"] == tipo])
    
    # Contar casos por estado  
    casos_por_estado = {}
    for estado in EstadoCaso:
        # Contar cuántos casos hay en cada estado
        casos_por_estado[estado.value] = len([c for c in casos_db if c["estado"] == estado])
    
    return {
        "total_casos": total_casos,
        "casos_por_tipo": casos_por_tipo,
        "casos_por_estado": casos_por_estado,
        "ultimo_numero": casos_db[-1]["numero_caso"] if casos_db else "Ninguno"
    }


# ============================================================================
# NOTAS PARA PRINCIPIANTES
# ============================================================================

# 1. ¿Por qué usar una lista en lugar de una base de datos real?
#    - Simplicidad: No requiere configurar PostgreSQL, MySQL, etc.
#    - Educativo: Fácil de entender cómo funcionan las operaciones
#    - Prototipado: Rápido para probar ideas
#    - Limitaciones: Los datos se pierden al reiniciar

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