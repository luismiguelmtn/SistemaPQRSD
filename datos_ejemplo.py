# -*- coding: utf-8 -*-
"""
Generador de datos de ejemplo para el sistema PQRSD.

Este módulo contiene 100 casos de ejemplo con datos falsos realistas
para simular un entorno de producción y facilitar las pruebas del sistema.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
from enums import TipoCaso, EstadoCaso


def generar_casos_ejemplo() -> List[Dict[str, Any]]:
    """
    Genera 100 casos de ejemplo con datos falsos realistas.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los datos de los casos
    """
    
    # Listas de datos falsos para generar casos realistas
    nombres = [
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
    
    asuntos_peticion = [
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
    ]
    
    asuntos_queja = [
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
    ]
    
    asuntos_reclamo = [
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
    ]
    
    asuntos_sugerencia = [
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
    ]
    
    asuntos_denuncia = [
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
    
    descripciones_base = {
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
    
    dominios_email = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "email.com", "correo.com"]
    
    casos_ejemplo = []
    
    for i in range(1, 101):  # Generar 100 casos
        # Seleccionar tipo de caso aleatoriamente
        tipo = random.choice(list(TipoCaso))
        
        # Seleccionar asunto según el tipo
        if tipo == TipoCaso.PETICION:
            asunto = random.choice(asuntos_peticion)
        elif tipo == TipoCaso.QUEJA:
            asunto = random.choice(asuntos_queja)
        elif tipo == TipoCaso.RECLAMO:
            asunto = random.choice(asuntos_reclamo)
        elif tipo == TipoCaso.SUGERENCIA:
            asunto = random.choice(asuntos_sugerencia)
        else:  # DENUNCIA
            asunto = random.choice(asuntos_denuncia)
        
        # Generar nombre y email
        nombre = random.choice(nombres)
        if random.random() < 0.1:  # 10% de casos anónimos
            nombre = "Ciudadano Anónimo"
            email = "anonimo@email.com"
        else:
            # Generar email basado en el nombre
            nombre_parts = nombre.lower().split()
            email_user = f"{nombre_parts[0]}.{nombre_parts[-1]}"
            email = f"{email_user}@{random.choice(dominios_email)}"
        
        # Generar teléfono (80% tienen teléfono)
        telefono = None
        if random.random() < 0.8:
            telefono = f"300{random.randint(1000000, 9999999)}"
        
        # Generar descripción
        descripcion_base = random.choice(descripciones_base[tipo])
        descripcion = f"{asunto}. {descripcion_base}"
        
        # Generar estado (distribución realista)
        estado_prob = random.random()
        if estado_prob < 0.3:  # 30% recibidos
            estado = EstadoCaso.RECIBIDO
        elif estado_prob < 0.6:  # 30% en proceso
            estado = EstadoCaso.EN_PROCESO
        elif estado_prob < 0.85:  # 25% resueltos
            estado = EstadoCaso.RESUELTO
        else:  # 15% cerrados
            estado = EstadoCaso.CERRADO
        
        # Generar fechas realistas (últimos 60 días)
        dias_atras = random.randint(1, 60)
        fecha_creacion = datetime.now() - timedelta(days=dias_atras)
        
        # Crear caso base
        caso = {
            "numero_caso": i,
            "anio": 2025,
            "tipo": tipo,
            "asunto": asunto,
            "descripcion": descripcion,
            "nombre_solicitante": nombre,
            "email_solicitante": email,
            "telefono_solicitante": telefono,
            "estado": estado,
            "fecha_creacion": fecha_creacion
        }
        
        # Agregar respuesta y fecha de actualización para casos resueltos/cerrados
        if estado in [EstadoCaso.RESUELTO, EstadoCaso.CERRADO]:
            respuestas = [
                "Su solicitud ha sido procesada exitosamente. Se han tomado las medidas correspondientes.",
                "Hemos revisado su caso y se ha dado solución satisfactoria al mismo.",
                "Su trámite ha sido completado. Puede consultar el resultado en nuestras oficinas.",
                "Se ha dado respuesta a su solicitud según los procedimientos establecidos.",
                "Su caso ha sido resuelto. Agradecemos su paciencia durante el proceso.",
                "Hemos atendido su solicitud y se han implementado las correcciones necesarias.",
                "Su consulta ha sido resuelta. El proceso se ha completado satisfactoriamente.",
                "Se ha dado trámite a su solicitud según la normatividad vigente."
            ]
            caso["respuesta"] = random.choice(respuestas)
            
            # Fecha de actualización entre 1 y 30 días después de la creación
            dias_actualizacion = random.randint(1, min(30, dias_atras))
            caso["fecha_actualizacion"] = fecha_creacion + timedelta(days=dias_actualizacion)
        
        casos_ejemplo.append(caso)
    
    return casos_ejemplo


def obtener_casos_ejemplo() -> List[Dict[str, Any]]:
    """
    Función pública para obtener los casos de ejemplo.
    
    Returns:
        List[Dict[str, Any]]: Lista de casos de ejemplo generados
    """
    return generar_casos_ejemplo()


if __name__ == "__main__":
    # Código para pruebas del módulo
    casos = generar_casos_ejemplo()
    print(f"Generados {len(casos)} casos de ejemplo")
    
    # Mostrar estadísticas
    tipos_count = {}
    estados_count = {}
    
    for caso in casos:
        tipo = caso['tipo']
        estado = caso['estado']
        
        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
        estados_count[estado] = estados_count.get(estado, 0) + 1
    
    print("\nEstadísticas por tipo:")
    for tipo, count in tipos_count.items():
        print(f"  {tipo.value}: {count}")
    
    print("\nEstadísticas por estado:")
    for estado, count in estados_count.items():
        print(f"  {estado.value}: {count}")