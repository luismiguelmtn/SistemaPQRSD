# -*- coding: utf-8 -*-
"""
Modelos de Base de Datos PostgreSQL para el Sistema PQRSD ESO

Este archivo define las tablas de PostgreSQL usando SQLAlchemy ORM.
Optimizado para PostgreSQL con índices, restricciones y tipos de datos específicos.

🏗️ ARQUITECTURA DE MODELOS:

📋 models.py (Pydantic): Modelos de API y validación
  ✓ Validación de entrada/salida HTTP
  ✓ Serialización/deserialización JSON
  ✓ Documentación automática OpenAPI
  ✓ Esquemas de respuesta de la API

🗄️ db_models.py (SQLAlchemy): Modelos de base de datos PostgreSQL
  ✓ Definición de tablas y columnas
  ✓ Índices optimizados para consultas
  ✓ Restricciones de integridad
  ✓ Relaciones entre entidades
  ✓ Triggers y funciones PostgreSQL

🔄 FLUJO DE DATOS:
  API Request → Pydantic (validación) → SQLAlchemy (persistencia) → PostgreSQL
  PostgreSQL → SQLAlchemy (consulta) → Pydantic (serialización) → API Response

💡 VENTAJAS DE ESTA SEPARACIÓN:
  - Separación clara de responsabilidades
  - Flexibilidad para cambios independientes
  - Mejor testabilidad y mantenimiento
  - Optimización específica por capa
  - Reutilización de modelos en diferentes contextos

🚀 OPTIMIZACIONES POSTGRESQL:
  - Índices estratégicos para consultas frecuentes
  - Tipos de datos nativos de PostgreSQL
  - Restricciones de integridad referencial
  - Funciones de fecha/hora del servidor
  - Comentarios en columnas para documentación
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any, Optional

# Importar la configuración de base de datos PostgreSQL
from database import Base
from enums import TipoCaso, EstadoCaso

# ============================================================================
# MODELO DE TABLA POSTGRESQL: CASOS PQRSD
# ============================================================================

class Caso(Base):
    """
    Modelo de base de datos PostgreSQL para la tabla 'casos'.
    
    Esta clase define la estructura de la tabla principal del sistema PQRSD,
    optimizada para PostgreSQL con índices estratégicos y restricciones de integridad.
    
    🏗️ CARACTERÍSTICAS POSTGRESQL:
    ✓ Índices compuestos para consultas frecuentes
    ✓ Enums nativos de PostgreSQL para tipos y estados
    ✓ Funciones de fecha/hora del servidor (func.now())
    ✓ Comentarios en columnas para documentación
    ✓ Restricciones de integridad y unicidad
    
    📊 ÍNDICES OPTIMIZADOS:
    - Primary key: id (automático)
    - Unique: numero_caso (búsquedas por número)
    - Index: tipo (filtros por tipo de caso)
    - Index: estado (filtros por estado)
    - Index: email_solicitante (búsquedas por solicitante)
    - Composite: (tipo, estado) para consultas combinadas
    - Composite: (fecha_creacion, estado) para reportes temporales
    
    🔄 FLUJO DE ESTADOS:
    RECIBIDO → EN_PROCESO → RESUELTO/CERRADO
    
    📋 CAMPOS OBLIGATORIOS vs OPCIONALES:
    ✓ Obligatorios: numero_caso, tipo, asunto, descripcion, nombre_solicitante, email_solicitante, estado
    ⚪ Opcionales: telefono_solicitante, respuesta
    🤖 Automáticos: id, fecha_creacion, fecha_actualizacion
    
    - __tablename__: Nombre de la tabla en la base de datos
    - Column: Define una columna en la tabla
    - Integer, String, Text: Tipos de datos
    - primary_key: Clave primaria (identificador único)
    - nullable: Si puede ser NULL (vacío) o no
    - index: Si se debe crear un índice para búsquedas rápidas
    - unique: Si el valor debe ser único en toda la tabla
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = "casos"
    
    # ========================================================================
    # COLUMNAS DE LA TABLA
    # ========================================================================
    
    # ID único interno (clave primaria)
    # Se auto-incrementa automáticamente: 1, 2, 3, 4...
    id = Column(
        Integer,
        primary_key=True,  # Es la clave primaria
        index=True,        # Crear índice para búsquedas rápidas
        comment="Identificador único interno del caso"
    )
    
    # Número de caso público (legible para humanos)
    # Ejemplo: "CASO-2024-001", "PET-2024-001"
    numero_caso = Column(
        String(50),        # Máximo 50 caracteres
        unique=True,       # Debe ser único en toda la tabla
        nullable=False,    # No puede ser NULL (obligatorio)
        index=True,        # Índice para búsquedas rápidas
        comment="Número de caso único y legible para el público"
    )
    
    # Tipo de caso (petición, queja, reclamo, sugerencia, denuncia)
    # Usamos SQLEnum para restringir a valores específicos
    tipo = Column(
        SQLEnum(TipoCaso),  # Solo acepta valores del enum TipoCaso
        nullable=False,     # Obligatorio
        index=True,         # Índice para filtrar por tipo
        comment="Tipo de caso PQRSD"
    )
    
    # Asunto o título del caso
    # String(200) = máximo 200 caracteres
    asunto = Column(
        String(200),
        nullable=False,
        comment="Título o asunto del caso"
    )
    
    # Descripción detallada del caso
    # Text = texto largo sin límite específico
    descripcion = Column(
        Text,
        nullable=False,
        comment="Descripción detallada del caso"
    )
    
    # Información del solicitante
    nombre_solicitante = Column(
        String(100),
        nullable=False,
        comment="Nombre completo del solicitante"
    )
    
    email_solicitante = Column(
        String(255),        # Los emails pueden ser largos
        nullable=False,
        index=True,         # Índice para buscar por email
        comment="Email del solicitante"
    )
    
    telefono_solicitante = Column(
        String(15),
        nullable=True,      # Es opcional (puede ser NULL)
        comment="Teléfono de contacto del solicitante"
    )
    
    # Estado del caso
    estado = Column(
        SQLEnum(EstadoCaso),
        nullable=False,
        default=EstadoCaso.RECIBIDO,  # Valor por defecto
        index=True,                   # Índice para filtrar por estado
        comment="Estado actual del caso"
    )
    
    # Respuesta oficial (opcional)
    respuesta = Column(
        Text,
        nullable=True,      # Opcional hasta que se responda
        comment="Respuesta oficial al caso"
    )
    
    # ========================================================================
    # CAMPOS DE AUDITORÍA (TIMESTAMPS)
    # ========================================================================
    
    # Fecha de creación
    # func.now() = función SQL que obtiene la fecha/hora actual
    # server_default = se ejecuta en el servidor de base de datos
    fecha_creacion = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),  # Se asigna automáticamente al crear
        comment="Fecha y hora de creación del caso"
    )
    
    # Fecha de última actualización
    # Se actualiza automáticamente cada vez que se modifica el registro
    fecha_actualizacion = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),  # Valor inicial
        onupdate=func.now(),        # Se actualiza automáticamente
        comment="Fecha y hora de la última actualización"
    )
    
    # ========================================================================
    # ÍNDICES COMPUESTOS OPTIMIZADOS PARA POSTGRESQL
    # ========================================================================
    
    # Estos índices mejoran significativamente el rendimiento de consultas frecuentes
    __table_args__ = (
        # Índice compuesto para consultas por tipo y estado (muy común en dashboards)
        Index('idx_caso_tipo_estado', 'tipo', 'estado'),
        
        # Índice compuesto para reportes temporales por fecha y estado
        Index('idx_caso_fecha_estado', 'fecha_creacion', 'estado'),
        
        # Índice compuesto para búsquedas por solicitante y estado
        Index('idx_caso_email_estado', 'email_solicitante', 'estado'),
        
        # Índice para consultas de casos recientes (ordenamiento por fecha)
        Index('idx_caso_fecha_desc', 'fecha_creacion'),
        
        # Comentario de la tabla para documentación en PostgreSQL
        {'comment': 'Tabla principal para almacenar casos PQRSD del sistema ESO. '
                   'Optimizada para PostgreSQL con índices estratégicos para consultas frecuentes.'}
    )
    
    # ========================================================================
    # MÉTODOS DE INSTANCIA Y UTILIDADES
    # ========================================================================
    
    def __repr__(self) -> str:
        """
        Representación legible del objeto Caso para debugging y logs.
        
        🔍 UTILIDAD:
        - Debugging en desarrollo
        - Logs de aplicación
        - Inspección en consola interactiva
        
        Returns:
            str: Representación compacta con información clave del caso
        
        Example:
            >>> caso = Caso(id=1, numero_caso='ESO-2024-001', tipo=TipoCaso.PETICION)
            >>> print(caso)
            <Caso(id=1, numero='ESO-2024-001', tipo='PETICION', estado='RECIBIDO')>
        """
        return f"<Caso(id={self.id}, numero='{self.numero_caso}', tipo='{self.tipo}', estado='{self.estado}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia de Caso a diccionario Python.
        
        🚀 OPTIMIZADO PARA POSTGRESQL:
        - Manejo seguro de enums (convierte a .value)
        - Serialización ISO de fechas para compatibilidad JSON
        - Manejo de valores None para campos opcionales
        - Formato estándar para APIs REST
        
        Returns:
            Dict[str, Any]: Diccionario con todos los campos del caso
        
        Example:
            >>> caso.to_dict()
            {
                'id': 1,
                'numero_caso': 'ESO-2024-001',
                'tipo': 'PETICION',
                'estado': 'RECIBIDO',
                'fecha_creacion': '2024-01-15T10:30:00',
                ...
            }
        """
        return {
            'id': self.id,
            'numero_caso': self.numero_caso,
            'tipo': self.tipo.value if self.tipo else None,
            'asunto': self.asunto,
            'descripcion': self.descripcion,
            'nombre_solicitante': self.nombre_solicitante,
            'email_solicitante': self.email_solicitante,
            'telefono_solicitante': self.telefono_solicitante,
            'estado': self.estado.value if self.estado else None,
            'respuesta': self.respuesta,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    @classmethod
    def from_pydantic(cls, caso_data, numero_caso: str) -> 'Caso':
        """
        Factory method para crear instancia de Caso desde objeto Pydantic.
        
        🔄 FLUJO DE CONVERSIÓN:
        Pydantic Model (validación) → SQLAlchemy Model (persistencia)
        
        ⚡ CARACTERÍSTICAS:
        - Mapeo automático de campos
        - Manejo seguro de campos opcionales
        - Preservación de tipos enum
        - Estado inicial automático (RECIBIDO)
        
        Args:
            caso_data: Objeto CasoCreate de Pydantic con datos validados
            numero_caso: Número único generado para el caso
            
        Returns:
            Caso: Nueva instancia lista para persistir en PostgreSQL
        
        Example:
            >>> from pydantic_models import CasoCreate
            >>> pydantic_caso = CasoCreate(tipo='PETICION', asunto='...', ...)
            >>> db_caso = Caso.from_pydantic(pydantic_caso, 'ESO-2024-001')
            >>> session.add(db_caso)
        
        Note:
            Los campos fecha_creacion y fecha_actualizacion se generan automáticamente
            por PostgreSQL usando func.now(), no necesitan ser especificados.
        """
        return cls(
            numero_caso=numero_caso,
            tipo=caso_data.tipo,
            asunto=caso_data.asunto,
            descripcion=caso_data.descripcion,
            nombre_solicitante=caso_data.nombre_solicitante,
            email_solicitante=caso_data.email_solicitante,
            telefono_solicitante=caso_data.telefono_solicitante,
            estado=EstadoCaso.RECIBIDO  # Estado inicial
        )

# ============================================================================
# INFORMACIÓN PARA DEBUGGING
# ============================================================================

if __name__ == "__main__":
    # Este código solo se ejecuta si ejecutas este archivo directamente
    # python db_models.py
    
    print("🗄️ Modelos de Base de Datos")
    print(f"📋 Tabla: {Caso.__tablename__}")
    print(f"🔑 Columnas: {list(Caso.__table__.columns.keys())}")
    
    # Mostrar información de cada columna
    print("\n📊 Detalles de columnas:")
    for column in Caso.__table__.columns:
        print(f"  - {column.name}: {column.type} (nullable={column.nullable})")