# -*- coding: utf-8 -*-
"""
Modelos de Base de Datos para el Sistema PQRSD

Este archivo define las tablas de la base de datos usando SQLAlchemy.

¿Cuál es la diferencia entre models.py y db_models.py?

- models.py (Pydantic): Define la estructura de datos para la API
  - Validación de entrada/salida
  - Serialización JSON
  - Documentación automática

- db_models.py (SQLAlchemy): Define la estructura de las tablas en la base de datos
  - Columnas y tipos de datos
  - Relaciones entre tablas
  - Índices y restricciones

¿Por qué dos archivos separados?
- Separación de responsabilidades
- La API puede tener campos diferentes a la base de datos
- Flexibilidad para cambios independientes
- Mejor organización del código

Analogia:
- Pydantic = El formulario que llena el usuario
- SQLAlchemy = La tabla donde se guardan los datos
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime

# Importar la configuración de base de datos
from database import Base
from enums import TipoCaso, EstadoCaso

# ============================================================================
# MODELO DE TABLA: CASOS
# ============================================================================

class Caso(Base):
    """
    Modelo de base de datos para la tabla 'casos'.
    
    Esta clase define cómo se estructura la tabla en la base de datos.
    Cada atributo representa una columna en la tabla.
    
    ¿Qué significa cada parte?
    
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
    # MÉTODOS DE LA CLASE
    # ========================================================================
    
    def __repr__(self):
        """
        Representación en string del objeto para debugging.
        
        Esto es lo que verás cuando imprimas un objeto Caso:
        print(caso) -> <Caso(id=1, numero='CASO-2024-001', tipo='peticion')>
        """
        return f"<Caso(id={self.id}, numero='{self.numero_caso}', tipo='{self.tipo}')>"
    
    def to_dict(self):
        """
        Convierte el objeto SQLAlchemy a un diccionario.
        
        Esto es útil para:
        - Convertir a JSON
        - Pasar datos a los modelos Pydantic
        - Debugging y logging
        
        Returns:
            dict: Diccionario con todos los campos del caso
        """
        return {
            "id": self.id,
            "numero_caso": self.numero_caso,
            "tipo": self.tipo,
            "asunto": self.asunto,
            "descripcion": self.descripcion,
            "nombre_solicitante": self.nombre_solicitante,
            "email_solicitante": self.email_solicitante,
            "telefono_solicitante": self.telefono_solicitante,
            "estado": self.estado,
            "respuesta": self.respuesta,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }
    
    @classmethod
    def from_pydantic(cls, caso_data, numero_caso: str):
        """
        Crea un objeto Caso desde un modelo Pydantic CasoCreate.
        
        Args:
            caso_data: Objeto CasoCreate de Pydantic
            numero_caso: Número único generado para el caso
            
        Returns:
            Caso: Nueva instancia de Caso para guardar en la base de datos
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