# -*- coding: utf-8 -*-
"""
Generador de Casos de Ejemplo para Sistema PQRSD

Este módulo proporciona funcionalidades para generar e insertar casos de ejemplo
realistas en la base de datos del sistema PQRSD. Incluye datos falsos pero
verosímiles para facilitar las pruebas y desarrollo del sistema.

Uso:
    Como script:
        python -m tests.fixtures.insertar_casos_ejemplo [número_de_casos]
    
    Como módulo:
        from tests.fixtures.insertar_casos_ejemplo import generar_casos_ejemplo
        casos = generar_casos_ejemplo(100)
    
Ejemplos:
    python -m tests.fixtures.insertar_casos_ejemplo        # 100 casos (por defecto)
    python -m tests.fixtures.insertar_casos_ejemplo 50     # 50 casos
    python -m tests.fixtures.insertar_casos_ejemplo 500    # 500 casos

Autor: Sistema PQRSD
Fecha: 2025
Versión: 2.0
"""

import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import random
from pathlib import Path

# Configuración del path para importaciones
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.enums import TipoCaso, EstadoCaso


# ============================================================================
# CONSTANTES Y DATOS DE EJEMPLO
# ============================================================================

# Configuración por defecto
DEFAULT_CASOS_COUNT = 100
MAX_DIAS_ATRAS = 60
PORCENTAJE_ANONIMOS = 0.1
PORCENTAJE_CON_TELEFONO = 0.8
ANIO_ACTUAL = 2025

# Distribución de estados (probabilidades acumulativas)
DISTRIBUCION_ESTADOS = {
    EstadoCaso.RECIBIDO: 0.3,      # 30%
    EstadoCaso.EN_PROCESO: 0.6,    # 30% (0.6 - 0.3)
    EstadoCaso.RESUELTO: 0.85,     # 25% (0.85 - 0.6)
    EstadoCaso.CERRADO: 1.0        # 15% (1.0 - 0.85)
}

# Datos de ejemplo para generación de casos
NOMBRES_EJEMPLO = [
    "María Elena García López", "Carlos Alberto Rodríguez", "Ana Patricia Martínez",
    "Luis Fernando Hernández", "Carmen Rosa Jiménez", "José Miguel Torres",
    "Laura Beatriz Morales", "Diego Alejandro Vargas", "Sofía Isabel Ramírez",
    "Roberto Carlos Mendoza", "Valentina Andrea Castillo", "Andrés Felipe Ruiz",
    "Gabriela Lucía Herrera", "Sebastián David Ortega", "Isabella María Guerrero",
    "Nicolás Esteban Silva", "Camila Alejandra Peña", "Mateo Santiago Vega",
    "Daniela Fernanda Cruz", "Alejandro José Romero", "Natalia Carolina Soto",
    "Juan Pablo Aguilar", "Mariana Valentina Díaz", "Santiago Nicolás Restrepo",
    "Valeria Sofía Gómez", "Emilio Andrés Cardona", "Lucía Esperanza Molina",
    "Tomás Alejandro Parra", "Antonia Isabel Navarro", "Maximiliano David Ríos"
]

ASUNTOS_POR_TIPO = {
    TipoCaso.PETICION: [
        "Solicitud de información sobre licencias comerciales",
        "Consulta sobre trámites de construcción",
        "Información sobre subsidios de vivienda",
        "Solicitud de certificado de estratificación",
        "Consulta sobre impuesto predial",
        "Información sobre programas sociales",
        "Solicitud de permiso para evento público",
        "Consulta sobre licencia de funcionamiento",
        "Información sobre becas estudiantiles",
        "Solicitud de certificado de residencia"
    ],
    TipoCaso.QUEJA: [
        "Demora excesiva en atención al público",
        "Mal servicio en oficina de atención",
        "Falta de información clara en trámites",
        "Personal poco capacitado en ventanilla",
        "Horarios de atención inadecuados",
        "Falta de señalización en las oficinas",
        "Demora en respuesta a solicitudes",
        "Trato inadecuado por parte del funcionario",
        "Falta de sillas en sala de espera",
        "Sistema informático lento y deficiente"
    ],
    TipoCaso.RECLAMO: [
        "Cobro indebido en factura de servicios",
        "Error en liquidación de impuestos",
        "Multa aplicada incorrectamente",
        "Cobro duplicado en trámite",
        "Tarifa incorrecta aplicada",
        "Error en cálculo de valorización",
        "Cobro por servicio no prestado",
        "Facturación errónea de multa de tránsito",
        "Error en avalúo catastral",
        "Cobro indebido de intereses"
    ],
    TipoCaso.SUGERENCIA: [
        "Implementar sistema de citas online",
        "Mejorar señalización en edificios públicos",
        "Crear aplicación móvil para trámites",
        "Ampliar horarios de atención",
        "Instalar pantallas informativas",
        "Crear sistema de turnos digitales",
        "Implementar pago electrónico",
        "Mejorar iluminación en oficinas",
        "Crear chat en línea para consultas",
        "Instalar aire acondicionado en salas"
    ],
    TipoCaso.DENUNCIA: [
        "Irregularidad en proceso de contratación",
        "Posible corrupción en licitación",
        "Mal manejo de recursos públicos",
        "Nepotismo en contratación de personal",
        "Uso indebido de vehículos oficiales",
        "Irregularidades en manejo de inventarios",
        "Conflicto de intereses en contrato",
        "Favoritismo en adjudicación",
        "Malversación de fondos públicos",
        "Abuso de autoridad por funcionario"
    ]
}

DESCRIPCIONES_BASE_POR_TIPO = {
    TipoCaso.PETICION: [
        "Necesito conocer los requisitos y documentos necesarios para realizar este trámite, así como los tiempos de respuesta estimados.",
        "Solicito información detallada sobre el proceso, costos involucrados y oficinas donde puedo realizar la gestión.",
        "Requiero orientación sobre los pasos a seguir y la documentación que debo presentar para completar mi solicitud.",
        "Necesito conocer el estado actual de mi trámite y los próximos pasos a seguir en el proceso.",
        "Solicito información sobre los horarios de atención y los requisitos específicos para mi caso particular."
    ],
    TipoCaso.QUEJA: [
        "El servicio recibido no cumple con los estándares esperados y solicito que se tomen las medidas correctivas necesarias.",
        "La atención brindada fue deficiente y no se resolvió mi consulta de manera satisfactoria.",
        "Experimento dificultades constantes con este servicio y requiero una solución inmediata.",
        "El tiempo de espera fue excesivo y no se justifica para un trámite de esta naturaleza.",
        "La información proporcionada fue incorrecta y me causó inconvenientes adicionales."
    ],
    TipoCaso.RECLAMO: [
        "Se me ha cobrado un valor que no corresponde según las tarifas oficiales publicadas. Solicito revisión y corrección.",
        "Existe un error en la liquidación que debe ser corregido inmediatamente. Adjunto la documentación de soporte.",
        "El cobro realizado no está justificado según mi situación particular. Requiero explicación y ajuste.",
        "Se aplicó una tarifa incorrecta en mi caso. Solicito la devolución del valor cobrado en exceso.",
        "Hay inconsistencias en la facturación que deben ser aclaradas y corregidas a la brevedad."
    ],
    TipoCaso.SUGERENCIA: [
        "Propongo esta mejora para optimizar el servicio y beneficiar a todos los ciudadanos que utilizan estos servicios.",
        "Esta implementación podría reducir significativamente los tiempos de espera y mejorar la experiencia del usuario.",
        "Sugiero esta alternativa que podría ser más eficiente y económica para la administración.",
        "Esta propuesta busca modernizar los procesos y hacerlos más accesibles para la ciudadanía.",
        "Recomiendo evaluar esta opción que podría mejorar la calidad del servicio prestado."
    ],
    TipoCaso.DENUNCIA: [
        "Reporto esta situación que considero irregular y que requiere investigación inmediata por parte de las autoridades competentes.",
        "He observado comportamientos que van contra la ética pública y deben ser investigados.",
        "Existe una situación que compromete la transparencia y debe ser atendida con urgencia.",
        "Denuncio estas irregularidades que afectan el buen uso de los recursos públicos.",
        "Reporto esta situación que va contra los principios de la administración pública."
    ]
}

RESPUESTAS_EJEMPLO = [
    "Su solicitud ha sido procesada exitosamente. Se han tomado las medidas correspondientes.",
    "Hemos revisado su caso y se ha dado solución satisfactoria al mismo.",
    "Su trámite ha sido completado. Puede consultar el resultado en nuestras oficinas.",
    "Se ha dado respuesta a su solicitud según los procedimientos establecidos.",
    "Su caso ha sido resuelto. Agradecemos su paciencia durante el proceso.",
    "Hemos atendido su solicitud y se han implementado las correcciones necesarias.",
    "Su consulta ha sido resuelta. El proceso se ha completado satisfactoriamente.",
    "Se ha dado trámite a su solicitud según la normatividad vigente."
]

DOMINIOS_EMAIL = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "email.com", "correo.com"]


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_tipo_caso_aleatorio() -> TipoCaso:
    """Genera un tipo de caso aleatorio.
    
    Returns:
        TipoCaso: Tipo de caso seleccionado aleatoriamente
    """
    return random.choice(list(TipoCaso))


def generar_estado_caso_realista() -> EstadoCaso:
    """Genera un estado de caso con distribución realista.
    
    Returns:
        EstadoCaso: Estado generado según distribución de probabilidades
    """
    probabilidad = random.random()
    
    for estado, limite in DISTRIBUCION_ESTADOS.items():
        if probabilidad < limite:
            return estado
    
    return EstadoCaso.CERRADO  # Fallback


def generar_datos_solicitante() -> Tuple[str, str, str]:
    """Genera datos del solicitante (nombre, email, teléfono).
    
    Returns:
        Tuple[str, str, str]: Tupla con (nombre, email, telefono)
    """
    # Determinar si es anónimo
    if random.random() < PORCENTAJE_ANONIMOS:
        return "Ciudadano Anónimo", "anonimo@email.com", None
    
    # Generar nombre y email
    nombre = random.choice(NOMBRES_EJEMPLO)
    nombre_parts = nombre.lower().split()
    email_user = f"{nombre_parts[0]}.{nombre_parts[-1]}"
    email = f"{email_user}@{random.choice(DOMINIOS_EMAIL)}"
    
    # Generar teléfono (opcional)
    telefono = None
    if random.random() < PORCENTAJE_CON_TELEFONO:
        telefono = f"300{random.randint(1000000, 9999999)}"
    
    return nombre, email, telefono


def generar_fechas_caso(dias_max_atras: int = MAX_DIAS_ATRAS) -> Tuple[datetime, datetime]:
    """Genera fechas realistas para un caso.
    
    Args:
        dias_max_atras (int): Máximo número de días hacia atrás para la fecha de creación
    
    Returns:
        Tuple[datetime, datetime]: Tupla con (fecha_creacion, fecha_actualizacion)
    """
    dias_atras = random.randint(1, dias_max_atras)
    fecha_creacion = datetime.now() - timedelta(days=dias_atras)
    
    # Fecha de actualización entre 1 y 30 días después de la creación
    dias_actualizacion = random.randint(1, min(30, dias_atras))
    fecha_actualizacion = fecha_creacion + timedelta(days=dias_actualizacion)
    
    return fecha_creacion, fecha_actualizacion


def construir_descripcion_caso(tipo: TipoCaso, asunto: str) -> str:
    """Construye una descripción completa para un caso.
    
    Args:
        tipo (TipoCaso): Tipo del caso
        asunto (str): Asunto del caso
    
    Returns:
        str: Descripción completa del caso
    """
    descripcion_base = random.choice(DESCRIPCIONES_BASE_POR_TIPO[tipo])
    return f"{asunto}. {descripcion_base}"


# ============================================================================
# FUNCIONES PRINCIPALES DE GENERACIÓN
# ============================================================================

def generar_caso_individual(tipo: TipoCaso, numero_caso: int) -> Dict[str, Any]:
    """Genera un caso individual con datos aleatorios realistas.
    
    Args:
        tipo (TipoCaso): Tipo específico del caso
        numero_caso (int): Número secuencial del caso para este tipo
    
    Returns:
        Dict[str, Any]: Diccionario con los datos del caso generado
    """
    # Generar asunto específico para el tipo
    asunto = random.choice(ASUNTOS_POR_TIPO[tipo])
    
    # Generar datos del solicitante
    nombre, email, telefono = generar_datos_solicitante()
    
    # Generar estado y fechas
    estado = generar_estado_caso_realista()
    fecha_creacion, fecha_actualizacion = generar_fechas_caso()
    
    # Generar número de caso completo formateado
    # Mapeo de tipos de caso a prefijos legibles (igual que en el servicio)
    prefijos = {
        TipoCaso.PETICION: "PET",
        TipoCaso.QUEJA: "QUE", 
        TipoCaso.RECLAMO: "REC",
        TipoCaso.SUGERENCIA: "SUG",
        TipoCaso.DENUNCIA: "DEN"
    }
    
    prefijo = prefijos[tipo]
    numero_caso_completo = f"{prefijo}-{ANIO_ACTUAL}-{numero_caso:04d}"
    
    # Construir caso base
    caso = {
        "numero_caso": numero_caso,
        "anio": ANIO_ACTUAL,
        "numero_caso_completo": numero_caso_completo,
        "tipo": tipo,
        "asunto": asunto,
        "descripcion": construir_descripcion_caso(tipo, asunto),
        "nombre_solicitante": nombre,
        "email_solicitante": email,
        "telefono_solicitante": telefono,
        "estado": estado,
        "fecha_creacion": fecha_creacion
    }
    
    # Agregar respuesta para casos resueltos/cerrados
    if estado in [EstadoCaso.RESUELTO, EstadoCaso.CERRADO]:
        caso["respuesta"] = random.choice(RESPUESTAS_EJEMPLO)
        caso["fecha_actualizacion"] = fecha_actualizacion
    
    return caso


def generar_casos_ejemplo(cantidad: int = DEFAULT_CASOS_COUNT) -> List[Dict[str, Any]]:
    """Genera una lista de casos de ejemplo con datos falsos realistas.
    Cada tipo de caso tendrá su propia numeración comenzando desde 1.
    
    Args:
        cantidad (int): Número de casos a generar. Por defecto 100.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los datos de los casos
    
    Raises:
        ValueError: Si la cantidad es menor o igual a 0
    """
    if cantidad <= 0:
        raise ValueError("La cantidad de casos debe ser mayor que 0")
    
    casos = []
    tipos_disponibles = list(TipoCaso)
    
    # Contadores para cada tipo de caso (numeración independiente)
    contadores_por_tipo = {tipo: 1 for tipo in tipos_disponibles}
    
    for i in range(cantidad):
        # Seleccionar tipo de caso aleatoriamente
        tipo = generar_tipo_caso_aleatorio()
        
        # Generar caso con numeración específica para este tipo
        caso = generar_caso_individual(tipo, contadores_por_tipo[tipo])
        casos.append(caso)
        
        # Incrementar contador para este tipo
        contadores_por_tipo[tipo] += 1
    
    return casos


def calcular_estadisticas_casos(casos: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Calcula estadísticas de los casos generados.
    
    Args:
        casos (List[Dict[str, Any]]): Lista de casos
    
    Returns:
        Dict[str, Dict[str, int]]: Diccionario con estadísticas por tipo y estado
    """
    tipos_count = {}
    estados_count = {}
    
    for caso in casos:
        tipo = caso['tipo']
        estado = caso['estado']
        
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
        estados_count[estado] = estados_count.get(estado, 0) + 1
    
    return {
        "tipos": tipos_count,
        "estados": estados_count
    }


def mostrar_estadisticas(estadisticas: Dict[str, Dict[str, int]]) -> None:
    """Muestra las estadísticas de casos en consola.
    
    Args:
        estadisticas (Dict[str, Dict[str, int]]): Estadísticas calculadas
    """
    print("\nEstadísticas por tipo:")
    for tipo, count in estadisticas["tipos"].items():
        print(f"  {tipo.value}: {count}")
    
    print("\nEstadísticas por estado:")
    for estado, count in estadisticas["estados"].items():
        print(f"  {estado.value}: {count}")


# ============================================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================================

def insertar_casos_en_bd(casos: List[Dict[str, Any]]) -> bool:
    """Inserta los casos generados en la base de datos.
    
    Args:
        casos (List[Dict[str, Any]]): Lista de casos a insertar
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    try:
        from sqlalchemy.orm import sessionmaker
        from app.core.database import engine
        from app.models.caso import Caso
        
        # Crear sesión de base de datos
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Insertar casos
            casos_insertados = 0
            for caso_data in casos:
                caso = Caso(
                    numero_caso=caso_data['numero_caso'],
                    anio=caso_data['anio'],
                    numero_caso_completo=caso_data['numero_caso_completo'],
                    tipo=caso_data['tipo'],
                    asunto=caso_data['asunto'],
                    descripcion=caso_data['descripcion'],
                    nombre_solicitante=caso_data['nombre_solicitante'],
                    email_solicitante=caso_data['email_solicitante'],
                    telefono_solicitante=caso_data['telefono_solicitante'],
                    estado=caso_data['estado'],
                    fecha_creacion=caso_data['fecha_creacion'],
                    respuesta=caso_data.get('respuesta'),
                    fecha_actualizacion=caso_data.get('fecha_actualizacion')
                )
                db.add(caso)
                casos_insertados += 1
            
            # Confirmar cambios
            db.commit()
            print(f"[OK] {casos_insertados} casos insertados exitosamente en la base de datos")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Error al insertar casos: {e}")
            return False
        finally:
            db.close()
            
    except ImportError as e:
        print(f"[ERROR] Error al importar dependencias de base de datos: {e}")
        return False


# ============================================================================
# FUNCIONES DE UTILIDAD Y VALIDACIÓN
# ============================================================================

def validar_argumentos_cli() -> int:
    """Valida y procesa los argumentos de línea de comandos.
    
    Returns:
        int: Número de casos a generar
    
    Raises:
        SystemExit: Si los argumentos son inválidos
    """
    if len(sys.argv) <= 1:
        return DEFAULT_CASOS_COUNT
    
    try:
        cantidad = int(sys.argv[1])
        if cantidad <= 0:
            print("Error: El número de casos debe ser mayor que 0")
            sys.exit(1)
        return cantidad
    except ValueError:
        print("Error: El argumento debe ser un número entero")
        print(f"Uso: python -m tests.fixtures.insertar_casos_ejemplo [número_de_casos]")
        sys.exit(1)


# ============================================================================
# FUNCIÓN PÚBLICA PARA USO COMO MÓDULO
# ============================================================================

def obtener_casos_ejemplo(cantidad: int = DEFAULT_CASOS_COUNT) -> List[Dict[str, Any]]:
    """Función pública para obtener casos de ejemplo (alias de generar_casos_ejemplo).
    
    Args:
        cantidad (int): Número de casos a generar. Por defecto 100.
    
    Returns:
        List[Dict[str, Any]]: Lista de casos de ejemplo generados
    """
    return generar_casos_ejemplo(cantidad)


# ============================================================================
# FUNCIÓN PRINCIPAL (SCRIPT)
# ============================================================================

def main() -> None:
    """Función principal del script."""
    # Validar argumentos
    cantidad_casos = validar_argumentos_cli()
    
    # Generar casos
    print(f"Generando {cantidad_casos} casos de ejemplo...")
    casos = generar_casos_ejemplo(cantidad_casos)
    print(f"[OK] Generados {len(casos)} casos de ejemplo")
    
    # Insertar en base de datos
    print("\nInsertando casos en la base de datos...")
    exito_insercion = insertar_casos_en_bd(casos)
    
    # Mostrar estadísticas
    if exito_insercion:
        estadisticas = calcular_estadisticas_casos(casos)
        mostrar_estadisticas(estadisticas)
    else:
        print("\n[ADVERTENCIA] Los casos se generaron pero no se pudieron insertar en la base de datos")
        print("   Verifica que la base de datos esté corriendo y las migraciones aplicadas")


if __name__ == "__main__":
    main()