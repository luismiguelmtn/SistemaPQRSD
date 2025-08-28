# -*- coding: utf-8 -*-
"""
Enumeraciones para el Sistema PQRSD

Este archivo contiene las enumeraciones (Enum) que definen los valores
permitidos para diferentes campos en el sistema PQRSD.

¿Qué es una Enumeración?
Una enumeración es una forma de definir un conjunto fijo de valores constantes.
En lugar de usar strings sueltos como "peticion" o "queja", usamos enums
para tener mejor control, validación automática y evitar errores de tipeo.

Ventajas de usar Enums:
- Previene errores de tipeo (si escribes "peticiom" en lugar de "peticion")
- Autocompletado en el IDE
- Validación automática por parte de Pydantic
- Código más legible y mantenible
"""

from enum import Enum


class TipoCaso(str, Enum):
    """
    Enumeración que define los tipos de casos PQRSD permitidos.
    
    PQRSD significa:
    - P: Peticiones
    - Q: Quejas  
    - R: Reclamos
    - S: Sugerencias
    - D: Denuncias
    
    Cada tipo tiene un propósito específico:
    """
    
    # Solicitudes de información, servicios o trámites
    PETICION = "peticion"      # Ejemplo: "Solicito información sobre requisitos para..."
    
    # Manifestaciones de insatisfacción por un servicio recibido
    QUEJA = "queja"            # Ejemplo: "El servicio fue muy lento y mal atendido"
    
    # Solicitudes de corrección, compensación o resarcimiento
    RECLAMO = "reclamo"        # Ejemplo: "Solicito reembolso por servicio no prestado"
    
    # Propuestas de mejora o ideas para optimizar servicios
    SUGERENCIA = "sugerencia"  # Ejemplo: "Propongo implementar un sistema de citas online"
    
    # Reportes de irregularidades, corrupción o malas prácticas
    DENUNCIA = "denuncia"      # Ejemplo: "Reporto cobro indebido por parte de funcionario"


class EstadoCaso(str, Enum):
    """
    Enumeración que define los estados posibles de un caso PQRSD.
    
    Representa el ciclo de vida de un caso desde que se crea hasta que se cierra.
    Cada estado indica en qué etapa del proceso se encuentra el caso.
    """
    
    # Estado inicial: El caso acaba de ser creado y registrado en el sistema
    RECIBIDO = "recibido"      # El caso está en la cola esperando ser asignado
    
    # Estado activo: Alguien está trabajando en resolver el caso
    EN_PROCESO = "en_proceso"  # Se está investigando, analizando o gestionando
    
    # Estado de respuesta: Se ha dado una respuesta o solución al solicitante
    RESUELTO = "resuelto"      # El caso tiene una respuesta pero puede requerir seguimiento
    
    # Estado final: El caso está completamente terminado y archivado
    CERRADO = "cerrado"        # No requiere más acciones, caso finalizado


# Nota para principiantes:
# Estas enumeraciones se usan en:
# 1. models.py - Para validar que solo se ingresen valores permitidos
# 2. services.py - Para filtrar casos por tipo o estado
# 3. routes.py - Para validar parámetros en los endpoints de la API
# 
# Ejemplo de uso:
# tipo_valido = TipoCaso.PETICION  # Esto es correcto
# tipo_invalido = "peticiom"       # Esto causaría un error de validación