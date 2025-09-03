#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialización de Base de Datos PostgreSQL
Sistema PQRSD - Peticiones, Quejas, Reclamos, Sugerencias y Denuncias

Este script se encarga de:
1. Verificar conectividad a PostgreSQL
2. Crear todas las tablas necesarias en PostgreSQL
3. Configurar índices y restricciones
4. Opcionalmente insertar datos de prueba realistas
5. Validar la integridad de la base de datos

¿Cuándo usar este script?
- La primera vez que configuras el proyecto con PostgreSQL
- Cuando quieres resetear la base de datos en desarrollo
- Para crear una base de datos limpia para testing
- Después de cambios en los modelos de datos

¿Cómo ejecutar este script?
Desde la terminal/consola:

Configuración inicial:
```bash
python init_db.py
```

Opciones avanzadas:
```bash
python init_db.py --reset          # Elimina y recrea todas las tablas
python init_db.py --sample-data    # Crea datos de ejemplo realistas
python init_db.py --reset --sample-data  # Resetea completamente con datos
python init_db.py --check          # Solo verifica el estado de la BD
python init_db.py --info           # Muestra información detallada
```

Requisitos previos:
1. PostgreSQL debe estar ejecutándose
2. La base de datos debe existir (createdb pqrsd_sistema)
3. El usuario debe tener permisos CREATE/DROP
4. Variables de entorno configuradas (.env)
"""

import argparse
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Importar nuestros módulos
from database import (
    create_tables, 
    drop_tables, 
    database_exists, 
    get_database_info,
    get_database_session,
    engine
)
from db_models import Caso
from enums import TipoCaso, EstadoCaso
from sqlalchemy import text

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verificar_conectividad() -> bool:
    """
    Verifica la conectividad a PostgreSQL y muestra información del servidor.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    logger.info("🔍 Verificando conectividad a PostgreSQL...")
    
    try:
        with engine.connect() as connection:
            # Verificar conexión básica
            result = connection.execute(text("SELECT 1"))
            if not result.fetchone():
                return False
            
            # Obtener información del servidor
            version_result = connection.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]
            
            # Obtener información de la base de datos actual
            db_info_result = connection.execute(text(
                "SELECT current_database(), current_user, inet_server_addr(), inet_server_port()"
            ))
            db_info = db_info_result.fetchone()
            
            logger.info("✅ Conectividad exitosa a PostgreSQL")
            logger.info(f"   📋 Base de datos: {db_info[0]}")
            logger.info(f"   👤 Usuario: {db_info[1]}")
            logger.info(f"   🌐 Servidor: {db_info[2] or 'localhost'}:{db_info[3] or 'N/A'}")
            logger.info(f"   🔧 Versión: {version.split(',')[0]}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error de conectividad a PostgreSQL: {e}")
        logger.error("💡 Posibles soluciones:")
        logger.error("   1. Verificar que PostgreSQL esté ejecutándose")
        logger.error("   2. Verificar credenciales en el archivo .env")
        logger.error("   3. Verificar que la base de datos exista")
        logger.error("   4. Verificar permisos del usuario")
        return False

def crear_base_de_datos() -> bool:
    """
    Crea todas las tablas necesarias en PostgreSQL.
    
    Returns:
        bool: True si la creación fue exitosa, False en caso contrario
    """
    logger.info("🔧 Inicializando base de datos PostgreSQL...")
    
    # Verificar conectividad primero
    if not verificar_conectividad():
        return False
    
    # Verificar si las tablas ya existen
    try:
        with engine.connect() as connection:
            result = connection.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            table_count = result.fetchone()[0]
            
            if table_count > 0:
                logger.info(f"ℹ️  La base de datos ya tiene {table_count} tabla(s)")
                mostrar_estado_base_de_datos()
                return True
    
    except Exception as e:
        logger.error(f"Error verificando tablas existentes: {e}")
        return False
    
    # Crear las tablas
    try:
        create_tables()
        logger.info("✅ Tablas creadas exitosamente en PostgreSQL")
        
        # Verificar creación
        mostrar_estado_base_de_datos()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        return False

def resetear_base_de_datos() -> bool:
    """
    Elimina todas las tablas existentes y crea nuevas en PostgreSQL.
    
    ⚠️ CUIDADO: Esto elimina TODOS los datos y estructura.
    
    Returns:
        bool: True si el reseteo fue exitoso, False en caso contrario
    """
    logger.warning("⚠️ RESETEAR BASE DE DATOS POSTGRESQL")
    logger.warning("Esto eliminará TODOS los datos y tablas existentes.")
    
    # Verificar conectividad primero
    if not verificar_conectividad():
        return False
    
    # Pedir confirmación
    try:
        respuesta = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
        if respuesta != "SI":
            logger.info("❌ Operación cancelada por el usuario")
            return False
    except KeyboardInterrupt:
        logger.info("\n❌ Operación cancelada por el usuario")
        return False
    
    try:
        logger.info("🗑️ Eliminando todas las tablas de PostgreSQL...")
        
        # Eliminar tablas si existen
        drop_tables()
        
        # Crear nuevas tablas
        logger.info("🔧 Creando nuevas tablas en PostgreSQL...")
        create_tables()
        
        logger.info("✅ Base de datos reseteada exitosamente")
        mostrar_estado_base_de_datos()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante el reseteo: {e}")
        return False

def crear_datos_de_ejemplo() -> bool:
    """
    Inserta datos de ejemplo realistas en PostgreSQL.
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    logger.info("📝 Insertando datos de ejemplo en PostgreSQL...")
    
    # Datos de ejemplo más realistas y variados
    casos_ejemplo = [
        {
            "numero_caso": "PET-2025-001",
            "tipo": TipoCaso.PETICION,
            "asunto": "Solicitud de información sobre licencias",
            "descripcion": "Necesito conocer los requisitos para obtener una licencia de funcionamiento para mi negocio de panadería y los tiempos de respuesta estimados.",
            "nombre_solicitante": "María Elena García López",
            "email_solicitante": "maria.garcia@email.com",
            "telefono_solicitante": "3001234567",
            "estado": EstadoCaso.RECIBIDO,
            "fecha_creacion": datetime.now() - timedelta(days=2)
        },
        {
            "numero_caso": "QUE-2025-002",
            "tipo": TipoCaso.QUEJA,
            "asunto": "Demora en atención al público",
            "descripcion": "El tiempo de espera en la oficina de atención al ciudadano fue de más de 2 horas para un trámite simple. Solicito mejorar el servicio.",
            "nombre_solicitante": "Carlos Alberto Rodríguez",
            "email_solicitante": "carlos.rodriguez@email.com",
            "telefono_solicitante": "3009876543",
            "estado": EstadoCaso.EN_PROCESO,
            "fecha_creacion": datetime.now() - timedelta(days=5)
        },
        {
            "numero_caso": "REC-2025-003",
            "tipo": TipoCaso.RECLAMO,
            "asunto": "Cobro indebido en factura",
            "descripcion": "Se me cobró un valor adicional que no corresponde según la tarifa oficial publicada. Solicito revisión y reembolso.",
            "nombre_solicitante": "Ana Patricia Martínez",
            "email_solicitante": "ana.martinez@email.com",
            "telefono_solicitante": None,
            "estado": EstadoCaso.RESUELTO,
            "respuesta": "Se ha verificado el cobro y se procederá con el reembolso correspondiente. El valor será devuelto en los próximos 5 días hábiles.",
            "fecha_creacion": datetime.now() - timedelta(days=10),
            "fecha_actualizacion": datetime.now() - timedelta(days=1)
        },
        {
            "numero_caso": "SUG-2025-004",
            "tipo": TipoCaso.SUGERENCIA,
            "asunto": "Implementar sistema de citas online",
            "descripcion": "Propongo implementar un sistema de citas por internet para evitar las largas filas y optimizar la atención al ciudadano.",
            "nombre_solicitante": "Luis Fernando Hernández",
            "email_solicitante": "luis.hernandez@email.com",
            "telefono_solicitante": "3005555555",
            "estado": EstadoCaso.CERRADO,
            "respuesta": "Agradecemos su sugerencia. Hemos evaluado la propuesta y está siendo considerada para implementación en el próximo año.",
            "fecha_creacion": datetime.now() - timedelta(days=7),
            "fecha_actualizacion": datetime.now() - timedelta(days=2)
        },
        {
            "numero_caso": "DEN-2025-005",
            "tipo": TipoCaso.DENUNCIA,
            "asunto": "Irregularidad en proceso de contratación",
            "descripcion": "Reporto posibles irregularidades en el proceso de contratación del proyecto de infraestructura municipal. Solicito investigación.",
            "nombre_solicitante": "Ciudadano Anónimo",
            "email_solicitante": "anonimo@email.com",
            "telefono_solicitante": None,
            "estado": EstadoCaso.EN_PROCESO,
            "fecha_creacion": datetime.now() - timedelta(days=3)
        }
    ]
    
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Verificar si ya existen datos
            casos_existentes = db.query(Caso).count()
            if casos_existentes > 0:
                logger.info(f"⚠️ Ya existen {casos_existentes} casos en la base de datos")
                try:
                    respuesta = input("¿Agregar datos de ejemplo de todas formas? (s/n): ")
                    if respuesta.lower() != 's':
                        logger.info("❌ Operación cancelada por el usuario")
                        return True
                except KeyboardInterrupt:
                    logger.info("\n❌ Operación cancelada por el usuario")
                    return True
            
            # Insertar casos con manejo de errores individual
            casos_insertados = 0
            for i, caso_data in enumerate(casos_ejemplo, 1):
                try:
                    caso = Caso(**caso_data)
                    db.add(caso)
                    casos_insertados += 1
                    logger.debug(f"   ✓ Caso {i}/{len(casos_ejemplo)}: {caso_data['numero_caso']}")
                except Exception as e:
                    logger.warning(f"   ⚠️ Error insertando caso {i}: {e}")
                    continue
            
            # Guardar todos los cambios
            db.commit()
            
            logger.info(f"✅ Se crearon {casos_insertados} casos de ejemplo exitosamente")
            
            # Mostrar resumen detallado
            total_casos = db.query(Caso).count()
            logger.info(f"📊 Total de casos en la base de datos: {total_casos}")
            
            # Mostrar estadísticas por tipo
            for tipo in TipoCaso:
                count = db.query(Caso).filter(Caso.tipo == tipo).count()
                if count > 0:
                    logger.info(f"   📋 {tipo.value}: {count} caso(s)")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Error creando datos de ejemplo: {e}")
        return False

def mostrar_estado_base_de_datos() -> Dict[str, Any]:
    """
    Muestra información detallada sobre el estado actual de PostgreSQL.
    
    Returns:
        Dict[str, Any]: Diccionario con estadísticas de la base de datos
    """
    logger.info("\n📊 ESTADO DE LA BASE DE DATOS POSTGRESQL")
    logger.info("=" * 60)
    
    estadisticas = {
        "conectividad": False,
        "total_casos": 0,
        "casos_por_tipo": {},
        "casos_por_estado": {},
        "casos_recientes": [],
        "info_servidor": {}
    }
    
    try:
        # Verificar conectividad y obtener información del servidor
        with engine.connect() as connection:
            # Información básica del servidor PostgreSQL
            version_result = connection.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]
            
            db_info_result = connection.execute(text(
                "SELECT current_database(), current_user, "
                "pg_size_pretty(pg_database_size(current_database())), "
                "inet_server_addr(), inet_server_port()"
            ))
            db_info = db_info_result.fetchone()
            
            # Información de tablas
            tables_result = connection.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            table_count = tables_result.fetchone()[0]
            
            estadisticas["conectividad"] = True
            estadisticas["info_servidor"] = {
                "version": version.split(',')[0],
                "database": db_info[0],
                "user": db_info[1],
                "size": db_info[2],
                "host": db_info[3] or 'localhost',
                "port": db_info[4] or 'N/A',
                "tables": table_count
            }
            
            logger.info(f"🔧 Versión PostgreSQL: {estadisticas['info_servidor']['version']}")
            logger.info(f"📋 Base de datos: {estadisticas['info_servidor']['database']}")
            logger.info(f"👤 Usuario: {estadisticas['info_servidor']['user']}")
            logger.info(f"📏 Tamaño: {estadisticas['info_servidor']['size']}")
            logger.info(f"🌐 Servidor: {estadisticas['info_servidor']['host']}:{estadisticas['info_servidor']['port']}")
            logger.info(f"📊 Tablas: {estadisticas['info_servidor']['tables']}")
        
        # Obtener sesión para consultas de datos
        db = next(get_database_session())
        
        try:
            # Contar casos por tipo
            logger.info("\n📋 CASOS POR TIPO:")
            for tipo in TipoCaso:
                count = db.query(Caso).filter(Caso.tipo == tipo).count()
                estadisticas["casos_por_tipo"][tipo.value] = count
                if count > 0:
                    logger.info(f"  📌 {tipo.value}: {count}")
            
            # Contar casos por estado
            logger.info("\n🔄 CASOS POR ESTADO:")
            for estado in EstadoCaso:
                count = db.query(Caso).filter(Caso.estado == estado).count()
                estadisticas["casos_por_estado"][estado.value] = count
                if count > 0:
                    logger.info(f"  🔸 {estado.value}: {count}")
            
            # Total de casos
            total_casos = db.query(Caso).count()
            estadisticas["total_casos"] = total_casos
            logger.info(f"\n📊 TOTAL DE CASOS: {total_casos}")
            
            # Casos recientes (últimos 5)
            if total_casos > 0:
                logger.info("\n🕒 CASOS RECIENTES:")
                casos_recientes = (
                    db.query(Caso)
                    .order_by(Caso.fecha_creacion.desc())
                    .limit(5)
                    .all()
                )
                
                for caso in casos_recientes:
                    fecha_str = caso.fecha_creacion.strftime("%Y-%m-%d %H:%M")
                    caso_info = {
                        "numero": caso.numero_caso,
                        "tipo": caso.tipo.value,
                        "estado": caso.estado.value,
                        "fecha": fecha_str
                    }
                    estadisticas["casos_recientes"].append(caso_info)
                    logger.info(f"  🔹 {caso.numero_caso} - {caso.tipo.value} - {caso.estado.value} - {fecha_str}")
            
            # Estadísticas adicionales de rendimiento
            if total_casos > 0:
                logger.info("\n⚡ ESTADÍSTICAS ADICIONALES:")
                
                # Casos por mes actual
                casos_mes_actual = db.query(Caso).filter(
                    Caso.fecha_creacion >= datetime.now().replace(day=1)
                ).count()
                logger.info(f"  📅 Casos este mes: {casos_mes_actual}")
                
                # Casos resueltos vs pendientes
                casos_resueltos = db.query(Caso).filter(
                    Caso.estado.in_([EstadoCaso.RESUELTO, EstadoCaso.CERRADO])
                ).count()
                casos_pendientes = total_casos - casos_resueltos
                logger.info(f"  ✅ Casos resueltos: {casos_resueltos}")
                logger.info(f"  ⏳ Casos pendientes: {casos_pendientes}")
                
                if total_casos > 0:
                    porcentaje_resueltos = (casos_resueltos / total_casos) * 100
                    logger.info(f"  📈 Tasa de resolución: {porcentaje_resueltos:.1f}%")
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"❌ Error obteniendo información de la base de datos: {e}")
        estadisticas["error"] = str(e)
    
    logger.info("=" * 60)
    return estadisticas

def main():
    """
    Función principal que maneja los argumentos de línea de comandos para PostgreSQL.
    """
    parser = argparse.ArgumentParser(
        description="Inicializador de Base de Datos PostgreSQL - Sistema PQRSD ESO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🔧 PREREQUISITOS PARA POSTGRESQL:
  1. PostgreSQL instalado y ejecutándose
  2. Base de datos creada (ej: pqrsd_eso)
  3. Usuario con permisos de escritura
  4. Archivo .env configurado con credenciales

📋 EJEMPLOS DE USO:
  python init_db.py                     # Crear tablas en PostgreSQL
  python init_db.py --check              # Verificar conectividad
  python init_db.py --reset              # Resetear todas las tablas
  python init_db.py --examples           # Insertar datos de ejemplo
  python init_db.py --info               # Mostrar información detallada
  python init_db.py --reset --examples   # Resetear e insertar ejemplos
  python init_db.py --check --info       # Verificar y mostrar estado

🔒 SEGURIDAD:
  - Las credenciales se leen desde variables de entorno
  - Nunca hardcodear passwords en el código
  - Usar conexiones SSL en producción
        """
    )
    
    parser.add_argument(
        "--reset",
        action="store_true",
        help="⚠️ Resetear todas las tablas de PostgreSQL (elimina TODOS los datos)"
    )
    
    parser.add_argument(
        "--examples",
        action="store_true",
        help="📝 Insertar datos de ejemplo realistas en PostgreSQL"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="📊 Mostrar información detallada de la base de datos PostgreSQL"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="🔍 Verificar conectividad a PostgreSQL y mostrar información del servidor"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="🔊 Mostrar información detallada durante la ejecución"
    )
    
    args = parser.parse_args()
    
    # Configurar nivel de logging según verbosidad
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("🔊 Modo verbose activado")
    
    logger.info("🚀 INICIALIZADOR DE POSTGRESQL - Sistema PQRSD ESO")
    logger.info("=" * 70)
    
    # Variables para tracking de éxito
    operaciones_exitosas = 0
    operaciones_totales = 0
    
    try:
        if args.check:
            # Verificar conectividad
            logger.info("🔍 Verificando conectividad a PostgreSQL...")
            operaciones_totales += 1
            if verificar_conectividad():
                operaciones_exitosas += 1
            else:
                logger.error("❌ Fallo en la verificación de conectividad")
                return False
        
        if args.info:
            # Solo mostrar información detallada
            logger.info("📊 Obteniendo información de la base de datos...")
            operaciones_totales += 1
            try:
                estadisticas = mostrar_estado_base_de_datos()
                if estadisticas.get("conectividad", False):
                    operaciones_exitosas += 1
                else:
                    logger.error("❌ No se pudo obtener información completa")
            except Exception as e:
                logger.error(f"❌ Error obteniendo información: {e}")
                
        elif args.reset:
            # Resetear base de datos
            logger.info("🔄 Iniciando proceso de reseteo de PostgreSQL...")
            operaciones_totales += 1
            if resetear_base_de_datos():
                operaciones_exitosas += 1
                
                # Agregar ejemplos si se solicita
                if args.examples:
                    logger.info("\n📝 Insertando datos de ejemplo...")
                    operaciones_totales += 1
                    if crear_datos_de_ejemplo():
                        operaciones_exitosas += 1
                    else:
                        logger.error("❌ Fallo insertando datos de ejemplo")
            else:
                logger.error("❌ Fallo en el reseteo de la base de datos")
                
        else:
            # Crear/verificar base de datos normal
            logger.info("🔧 Inicializando base de datos PostgreSQL...")
            operaciones_totales += 1
            if crear_base_de_datos():
                operaciones_exitosas += 1
                
                # Agregar ejemplos si se solicita
                if args.examples:
                    logger.info("\n📝 Insertando datos de ejemplo...")
                    operaciones_totales += 1
                    if crear_datos_de_ejemplo():
                        operaciones_exitosas += 1
                    else:
                        logger.error("❌ Fallo insertando datos de ejemplo")
            else:
                logger.error("❌ Fallo en la inicialización de la base de datos")
        
        # Mostrar estado final si no es solo verificación
        if not args.check and not args.info:
            logger.info("\n📊 Estado final de la base de datos:")
            try:
                mostrar_estado_base_de_datos()
            except Exception as e:
                logger.warning(f"⚠️ No se pudo mostrar el estado final: {e}")
        
        # Resumen de operaciones
        logger.info("\n" + "=" * 70)
        if operaciones_exitosas == operaciones_totales and operaciones_totales > 0:
            logger.info(f"✅ Proceso completado exitosamente ({operaciones_exitosas}/{operaciones_totales} operaciones)")
            logger.info("💡 La base de datos PostgreSQL está lista para usar")
            return True
        else:
            logger.warning(f"⚠️ Proceso completado con advertencias ({operaciones_exitosas}/{operaciones_totales} operaciones exitosas)")
            return False
        
    except KeyboardInterrupt:
        logger.info("\n❌ Proceso interrumpido por el usuario")
        return False
    except Exception as e:
        logger.error(f"\n❌ Error crítico durante la ejecución: {e}")
        logger.error("💡 Verificar:")
        logger.error("   1. PostgreSQL está ejecutándose")
        logger.error("   2. Credenciales en .env son correctas")
        logger.error("   3. Base de datos existe y usuario tiene permisos")
        return False

if __name__ == "__main__":
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Ejecutar función principal
    success = main()
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)