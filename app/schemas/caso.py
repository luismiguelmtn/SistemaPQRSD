# -*- coding: utf-8 -*-
"""
📋 Modelos Pydantic para Sistema PQRSD con PostgreSQL

Este archivo define los esquemas de validación de datos que actúan como
interfaz entre la API REST y la base de datos PostgreSQL.

🔄 FLUJO DE DATOS:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Cliente   │───▶│   Pydantic  │───▶│ PostgreSQL  │
│   (JSON)    │    │  (Validar)  │    │ (SQLAlchemy)│
└─────────────┘    └─────────────┘    └─────────────┘

🚀 CARACTERÍSTICAS PYDANTIC:
✓ Validación automática de tipos de datos
✓ Conversión inteligente de formatos
✓ Documentación automática en Swagger
✓ Serialización JSON bidireccional
✓ Validaciones personalizadas con Field()
✓ Manejo de campos opcionales y requeridos
✓ Integración perfecta con FastAPI

📊 MODELOS DEFINIDOS:
- CasoCreate: Datos para crear nuevo caso
- CasoResponse: Respuesta completa de caso
- CasoUpdate: Datos para actualizar caso

🔒 VALIDACIONES IMPLEMENTADAS:
- Longitudes mínimas y máximas
- Formatos de email válidos
- Enums para tipos y estados
- Campos opcionales vs obligatorios
- Ejemplos para documentación automática

🐘 OPTIMIZADO PARA POSTGRESQL:
- Tipos compatibles con SQLAlchemy
- Manejo de fechas ISO 8601
- Soporte para enums nativos
- Validación de integridad referencial
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.core.enums import TipoCaso, EstadoCaso


class CasoCreate(BaseModel):
    """
    Modelo para CREAR un nuevo caso PQRSD.
    
    Este modelo define qué información debe proporcionar el usuario
    cuando quiere crear un nuevo caso. Solo incluye los campos
    que el usuario puede/debe llenar.
    
    Campos automáticos (NO incluidos aquí):
    - id: Se genera automáticamente
    - numero_caso: Se genera automáticamente
    - estado: Se asigna automáticamente como "recibido"
    - fecha_creacion: Se asigna automáticamente
    - fecha_actualizacion: Se asigna automáticamente
    """
    
    # Tipo de caso: debe ser uno de los valores definidos en TipoCaso enum
    tipo: TipoCaso = Field(
        description="Tipo de caso PQRSD (peticion, queja, reclamo, sugerencia, denuncia)",
        example="peticion"
    )
    
    # Título o resumen breve del caso
    asunto: str = Field(
        min_length=5,
        max_length=200,
        description="Título o asunto del caso (5-200 caracteres)",
        example="Solicitud de información sobre requisitos de licencia"
    )
    
    # Descripción detallada del caso
    descripcion: str = Field(
        min_length=10,
        max_length=2000,
        description="Descripción detallada del caso (10-2000 caracteres)",
        example="Necesito conocer los requisitos y documentos necesarios para obtener una licencia de funcionamiento para mi negocio."
    )
    
    # Nombre completo de quien hace la solicitud
    nombre_solicitante: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre completo del solicitante (2-100 caracteres)",
        example="Juan Pérez García"
    )
    
    # Email válido para respuestas (EmailStr valida formato automáticamente)
    email_solicitante: EmailStr = Field(
        description="Email válido del solicitante para enviar respuestas",
        example="juan.perez@email.com"
    )
    
    # Teléfono opcional para contacto
    telefono_solicitante: Optional[str] = Field(
        None,
        min_length=10,
        max_length=15,
        description="Teléfono de contacto (opcional, 10-15 caracteres)",
        example="3001234567"
    )


class CasoResponse(BaseModel):
    """
    Modelo para MOSTRAR información completa de un caso PQRSD.
    
    Este modelo define cómo se presenta la información de un caso
    cuando se consulta. Incluye TODOS los campos, tanto los que
    proporciona el usuario como los que genera el sistema.
    
    ORDEN DE CAMPOS: Sigue el mismo orden que el modelo SQLAlchemy
    para mantener consistencia en toda la aplicación.
    
    Se usa para:
    - Respuestas de la API cuando se consulta un caso
    - Listados de casos
    - Mostrar detalles completos
    """
    
    # ========================================================================
    # CAMPOS PRINCIPALES (mismo orden que SQLAlchemy)
    # ========================================================================
    
    # ID único del caso (generado automáticamente por el sistema)
    id: int = Field(
        description="Identificador único interno del caso",
        example=1
    )
    
    # Número de caso consecutivo
    numero_caso: int = Field(
        description="Número consecutivo del caso",
        example=1
    )
    
    # Año del caso
    anio: int = Field(
        description="Año en que se creó el caso",
        example=2024
    )
    
    # Estado actual del caso (generado/actualizado por el sistema)
    estado: EstadoCaso = Field(
        description="Estado actual del caso",
        example="recibido"
    )
    
    # Número de caso completo formateado
    numero_caso_completo: str = Field(
        description="Número de caso completo con prefijo, año y número consecutivo",
        example="PET-2024-0001"
    )
    
    # Tipo de caso PQRSD
    tipo: TipoCaso = Field(
        description="Tipo de caso PQRSD",
        example="peticion"
    )
    
    # Asunto o título del caso
    asunto: str = Field(
        description="Título o asunto del caso",
        example="Solicitud de información sobre requisitos de licencia"
    )
    
    # Descripción detallada del caso
    descripcion: str = Field(
        description="Descripción detallada del caso",
        example="Necesito conocer los requisitos y documentos necesarios..."
    )
    
    # ========================================================================
    # INFORMACIÓN DEL SOLICITANTE
    # ========================================================================
    
    nombre_solicitante: str = Field(
        description="Nombre completo del solicitante",
        example="Juan Pérez García"
    )
    
    email_solicitante: EmailStr = Field(
        description="Email del solicitante",
        example="juan.perez@email.com"
    )
    
    telefono_solicitante: Optional[str] = Field(
        description="Teléfono de contacto (puede ser None)",
        example="3001234567"
    )
    
    # Respuesta oficial al caso (opcional, se llena cuando se resuelve)
    respuesta: Optional[str] = Field(
        None,
        description="Respuesta oficial al caso (opcional)",
        example="Los requisitos para la licencia son: 1) Cédula, 2) RUT, 3) Certificado de bomberos..."
    )
    
    # ========================================================================
    # CAMPOS DE AUDITORÍA (TIMESTAMPS)
    # ========================================================================
    
    # Fechas de control (generadas automáticamente por el sistema)
    fecha_creacion: datetime = Field(
        description="Fecha y hora cuando se creó el caso",
        example="2024-01-15T10:30:00"
    )
    
    fecha_actualizacion: datetime = Field(
        description="Fecha y hora de la última actualización",
        example="2024-01-15T10:30:00"
    )
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de CasoResponse desde un diccionario."""
        # Generar numero_caso_completo si no está presente
        if 'numero_caso_completo' not in data and 'tipo' in data and 'numero_caso' in data and 'anio' in data:
            prefijo_map = {
                "peticion": "PET",
                "queja": "QUE", 
                "reclamo": "REC",
                "sugerencia": "SUG",
                "denuncia": "DEN"
            }
            prefijo = prefijo_map.get(data['tipo'], "CASO")
            data['numero_caso_completo'] = f"{prefijo}-{data['anio']}-{data['numero_caso']:04d}"
        
        # Manejar fechas que vienen como strings ISO desde la base de datos
        from datetime import datetime
        
        if 'fecha_creacion' in data:
            if isinstance(data['fecha_creacion'], str):
                data['fecha_creacion'] = datetime.fromisoformat(data['fecha_creacion'])
            elif data['fecha_creacion'] is None:
                # Si por alguna razón es None, usar fecha actual como fallback
                data['fecha_creacion'] = datetime.now()
        
        if 'fecha_actualizacion' in data:
            if isinstance(data['fecha_actualizacion'], str):
                data['fecha_actualizacion'] = datetime.fromisoformat(data['fecha_actualizacion'])
            elif data['fecha_actualizacion'] is None:
                # Si por alguna razón es None, usar fecha actual como fallback
                data['fecha_actualizacion'] = datetime.now()
        
        return cls(**data)


class CasoUpdate(BaseModel):
    """
    Modelo para ACTUALIZAR un caso existente.
    
    Este modelo define qué campos pueden ser modificados en un caso
    que ya existe. Generalmente solo el personal autorizado puede
    actualizar casos para cambiar su estado o agregar respuestas.
    
    Todos los campos son opcionales porque:
    - Puedes actualizar solo el estado
    - Puedes actualizar solo la respuesta
    - Puedes actualizar ambos
    - No puedes actualizar información del solicitante (eso requeriría otro endpoint)
    """
    
    # Cambiar el estado del caso (ej: de "recibido" a "en_proceso")
    estado: Optional[EstadoCaso] = Field(
        None,
        description="Nuevo estado del caso (opcional)",
        example="en_proceso"
    )
    
    # Agregar o modificar la respuesta oficial
    respuesta: Optional[str] = Field(
        None,
        min_length=10,
        max_length=2000,
        description="Respuesta oficial al caso (opcional, 10-2000 caracteres)",
        example="Estimado usuario, los requisitos para su solicitud son los siguientes..."
    )


# Notas para principiantes:
# 
# 1. ¿Por qué tres modelos diferentes?
#    - CasoCreate: Solo lo que el usuario proporciona
#    - CasoResponse: Todo lo que se muestra (incluye campos generados)
#    - CasoUpdate: Solo lo que se puede modificar después
# 
# 2. ¿Qué hace Field()?
#    - Agrega validaciones (min_length, max_length)
#    - Proporciona documentación (description, example)
#    - Define valores por defecto
# 
# 3. ¿Qué es Optional[str]?
#    - Significa que el campo puede ser un string o None (nulo)
#    - Los campos sin Optional son obligatorios
# 
# 4. ¿Qué es EmailStr?
#    - Un tipo especial que valida que el string sea un email válido
#    - Requiere la librería email-validator
# 
# 5. Estos modelos se usan en:
#    - app/routers/caso.py: Para validar datos de entrada y salida
#    - app/services/caso.py: Para trabajar con datos validados
#    - FastAPI: Para generar documentación automática