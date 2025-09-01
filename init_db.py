#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialización de Base de Datos

Este script se encarga de:
1. Crear la base de datos SQLite
2. Crear todas las tablas necesarias
3. Opcionalmente insertar datos de prueba

¿Cuándo usar este script?
- La primera vez que configuras el proyecto
- Cuando quieres resetear la base de datos en desarrollo
- Para crear una base de datos limpia para testing

¿Cómo ejecutar este script?
Desde la terminal/consola:
```
python init_db.py
```

O con opciones:
```
python init_db.py --reset          # Elimina y recrea la base de datos
python init_db.py --sample-data    # Crea datos de ejemplo
python init_db.py --reset --sample-data  # Resetea y agrega datos de ejemplo
```
"""

import argparse
import sys
from datetime import datetime

# Importar nuestros módulos
from database import (
    create_tables, 
    drop_tables, 
    database_exists, 
    get_database_info,
    get_database_session
)
from db_models import Caso
from enums import TipoCaso, EstadoCaso

def crear_base_de_datos():
    """
    Crea la base de datos y todas las tablas.
    """
    print("🔧 Creando base de datos...")
    
    try:
        create_tables()
        print("✅ Base de datos creada exitosamente")
        
        # Mostrar información de la base de datos
        info = get_database_info()
        print(f"📁 Archivo: {info['database_file']}")
        print(f"📊 Tamaño: {info.get('size_mb', 0)} MB")
        
    except Exception as e:
        print(f"❌ Error creando la base de datos: {e}")
        sys.exit(1)

def resetear_base_de_datos():
    """
    Elimina y recrea la base de datos (¡CUIDADO: Elimina todos los datos!).
    """
    print("⚠️ RESETEAR BASE DE DATOS")
    print("Esto eliminará TODOS los datos existentes.")
    
    # Pedir confirmación en modo interactivo
    if sys.stdin.isatty():  # Solo si estamos en terminal interactiva
        respuesta = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
        if respuesta != "SI":
            print("❌ Operación cancelada")
            return
    
    try:
        print("🗑️ Eliminando tablas existentes...")
        drop_tables()
        
        print("🔧 Recreando tablas...")
        create_tables()
        
        print("✅ Base de datos reseteada exitosamente")
        
    except Exception as e:
        print(f"❌ Error reseteando la base de datos: {e}")
        sys.exit(1)

def crear_datos_de_ejemplo():
    """
    Inserta algunos casos de ejemplo para probar el sistema.
    """
    print("📝 Creando datos de ejemplo...")
    
    # Datos de ejemplo
    casos_ejemplo = [
        {
            "numero_caso": "PET-001",
            "tipo": TipoCaso.PETICION,
            "asunto": "Solicitud de información sobre licencias",
            "descripcion": "Necesito conocer los requisitos para obtener una licencia de funcionamiento para mi negocio de panadería.",
            "nombre_solicitante": "María García López",
            "email_solicitante": "maria.garcia@email.com",
            "telefono_solicitante": "3001234567",
            "estado": EstadoCaso.RECIBIDO
        },
        {
            "numero_caso": "QUE-001",
            "tipo": TipoCaso.QUEJA,
            "asunto": "Demora en atención al público",
            "descripcion": "El tiempo de espera en la oficina de atención al ciudadano fue de más de 2 horas para un trámite simple.",
            "nombre_solicitante": "Carlos Rodríguez",
            "email_solicitante": "carlos.rodriguez@email.com",
            "telefono_solicitante": "3009876543",
            "estado": EstadoCaso.EN_PROCESO
        },
        {
            "numero_caso": "REC-001",
            "tipo": TipoCaso.RECLAMO,
            "asunto": "Cobro indebido en factura",
            "descripcion": "Se me cobró un valor adicional que no corresponde según la tarifa oficial publicada.",
            "nombre_solicitante": "Ana Martínez",
            "email_solicitante": "ana.martinez@email.com",
            "telefono_solicitante": None,
            "estado": EstadoCaso.RESUELTO,
            "respuesta": "Se ha verificado el cobro y se procederá con el reembolso correspondiente. El valor será devuelto en los próximos 5 días hábiles."
        },
        {
            "numero_caso": "SUG-001",
            "tipo": TipoCaso.SUGERENCIA,
            "asunto": "Implementar sistema de citas online",
            "descripcion": "Propongo implementar un sistema de citas por internet para evitar las largas filas y optimizar la atención.",
            "nombre_solicitante": "Luis Hernández",
            "email_solicitante": "luis.hernandez@email.com",
            "telefono_solicitante": "3005555555",
            "estado": EstadoCaso.CERRADO,
            "respuesta": "Agradecemos su sugerencia. Hemos evaluado la propuesta y está siendo considerada para implementación en el próximo año."
        },
        {
            "numero_caso": "DEN-2024-001",
            "tipo": TipoCaso.DENUNCIA,
            "asunto": "Irregularidad en proceso de contratación",
            "descripcion": "Reporto posibles irregularidades en el proceso de contratación del proyecto de infraestructura municipal.",
            "nombre_solicitante": "Ciudadano Anónimo",
            "email_solicitante": "anonimo@email.com",
            "telefono_solicitante": None,
            "estado": EstadoCaso.EN_PROCESO
        }
    ]
    
    try:
        # Obtener una sesión de base de datos
        with next(get_database_session()) as db:
            # Verificar si ya existen datos
            casos_existentes = db.query(Caso).count()
            if casos_existentes > 0:
                print(f"⚠️ Ya existen {casos_existentes} casos en la base de datos")
                respuesta = input("¿Agregar datos de ejemplo de todas formas? (s/n): ")
                if respuesta.lower() != 's':
                    print("❌ Operación cancelada")
                    return
            
            # Insertar cada caso de ejemplo
            for caso_data in casos_ejemplo:
                caso = Caso(**caso_data)
                db.add(caso)
            
            # Guardar todos los cambios
            db.commit()
            
            print(f"✅ Se crearon {len(casos_ejemplo)} casos de ejemplo")
            
            # Mostrar resumen
            total_casos = db.query(Caso).count()
            print(f"📊 Total de casos en la base de datos: {total_casos}")
            
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        sys.exit(1)

def mostrar_estado_base_de_datos():
    """
    Muestra información sobre el estado actual de la base de datos.
    """
    print("📊 ESTADO DE LA BASE DE DATOS")
    print("=" * 50)
    
    # Información básica
    info = get_database_info()
    print(f"📁 Archivo: {info['database_file']}")
    print(f"🔗 URL: {info['database_url']}")
    print(f"📦 Existe: {'✅ Sí' if info['exists'] else '❌ No'}")
    
    if info['exists']:
        print(f"📊 Tamaño: {info.get('size_mb', 0)} MB")
        
        # Contar registros si la base de datos existe
        try:
            with next(get_database_session()) as db:
                total_casos = db.query(Caso).count()
                print(f"📋 Total de casos: {total_casos}")
                
                if total_casos > 0:
                    # Estadísticas por tipo
                    print("\n📈 Casos por tipo:")
                    for tipo in TipoCaso:
                        count = db.query(Caso).filter(Caso.tipo == tipo).count()
                        print(f"  - {tipo.value}: {count}")
                    
                    # Estadísticas por estado
                    print("\n📊 Casos por estado:")
                    for estado in EstadoCaso:
                        count = db.query(Caso).filter(Caso.estado == estado).count()
                        print(f"  - {estado.value}: {count}")
                        
        except Exception as e:
            print(f"⚠️ Error consultando la base de datos: {e}")
    
    print("=" * 50)

def main():
    """
    Función principal que maneja los argumentos de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Script de inicialización de base de datos para Sistema PQRSD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python init_db.py                    # Crear base de datos si no existe
  python init_db.py --reset            # Resetear base de datos
  python init_db.py --sample-data      # Agregar datos de ejemplo
  python init_db.py --reset --sample-data  # Resetear y agregar datos
  python init_db.py --status           # Solo mostrar estado
        """
    )
    
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Eliminar y recrear la base de datos (¡ELIMINA TODOS LOS DATOS!)"
    )
    
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="Crear datos de ejemplo para probar el sistema"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Solo mostrar el estado actual de la base de datos"
    )
    
    args = parser.parse_args()
    
    print("🚀 INICIALIZADOR DE BASE DE DATOS - Sistema PQRSD")
    print("=" * 60)
    
    # Solo mostrar estado
    if args.status:
        mostrar_estado_base_de_datos()
        return
    
    # Resetear base de datos
    if args.reset:
        resetear_base_de_datos()
    else:
        # Crear base de datos solo si no existe
        if not database_exists():
            crear_base_de_datos()
        else:
            print("ℹ️ La base de datos ya existe")
    
    # Crear datos de ejemplo
    if args.sample_data:
        crear_datos_de_ejemplo()
    
    # Mostrar estado final
    print("\n" + "=" * 60)
    mostrar_estado_base_de_datos()
    
    print("\n🎉 ¡Inicialización completada!")
    print("\n💡 Próximos pasos:")
    print("   1. Ejecuta: python main.py")
    print("   2. Abre: http://localhost:8000/docs")
    print("   3. ¡Prueba la API!")

if __name__ == "__main__":
    main()