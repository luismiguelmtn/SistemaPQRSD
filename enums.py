# -*- coding: utf-8 -*-
"""
🏷️ Enumeraciones para Sistema PQRSD con PostgreSQL

Este archivo define los valores constantes permitidos para campos específicos,
optimizado para trabajar con PostgreSQL y enums nativos.

🔧 ARQUITECTURA DE ENUMS:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Python    │───▶│  Pydantic   │───▶│ PostgreSQL  │
│   Enum      │    │ Validation  │    │ Native Enum │
└─────────────┘    └─────────────┘    └─────────────┘

🚀 VENTAJAS DE ESTA IMPLEMENTACIÓN:
✓ Prevención de errores de tipeo
✓ Autocompletado inteligente en IDE
✓ Validación automática en API
✓ Enums nativos en PostgreSQL
✓ Índices optimizados en BD
✓ Integridad referencial garantizada
✓ Consultas más eficientes
✓ Documentación automática en Swagger

🐘 OPTIMIZACIONES POSTGRESQL:
- Enums nativos para mejor rendimiento
- Índices automáticos en columnas enum
- Validación a nivel de base de datos
- Menor uso de espacio de almacenamiento
- Consultas más rápidas con comparaciones directas

📊 ENUMS DEFINIDOS:
- TipoCaso: Categorías PQRSD (Petición, Queja, Reclamo, Sugerencia, Denuncia)
- EstadoCaso: Flujo de estados (Recibido → En Proceso → Resuelto → Cerrado)
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