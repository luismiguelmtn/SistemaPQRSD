#!/usr/bin/env python3
"""
Script de despliegue para el Sistema PQRSD
Ejecuta la secuencia completa de comandos Docker y Alembic
Opcionalmente puede agregar casos de ejemplo
"""

import subprocess
import sys
import os
import time
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

def run_command(command, description):
    """
    Ejecuta un comando y maneja errores
    """
    print(f"\n🔄 {description}...")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent.parent  # Ejecutar desde la raíz del proyecto
        )
        
        if result.stdout:
            print(f"✅ Salida: {result.stdout.strip()}")
        
        print(f"✅ {description} completado exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"Código de salida: {e.returncode}")
        if e.stdout:
            print(f"Salida estándar: {e.stdout}")
        if e.stderr:
            print(f"Error estándar: {e.stderr}")
        return False

def wait_for_database(max_attempts=30, delay=2):
    """
    Espera a que la base de datos PostgreSQL esté disponible
    """
    print(f"\n⏳ Esperando a que la base de datos esté disponible...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración de la base de datos desde variables de entorno
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'pqrsd_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres')
    }
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"🔍 Intento {attempt}/{max_attempts} - Conectando a la base de datos...")
            
            # Intentar conectar a la base de datos
            conn = psycopg2.connect(**db_config)
            conn.close()
            
            print("✅ Base de datos disponible y lista para usar")
            return True
            
        except psycopg2.OperationalError as e:
            if attempt < max_attempts:
                print(f"⏱️  Base de datos no disponible aún, esperando {delay} segundos...")
                time.sleep(delay)
            else:
                print(f"❌ No se pudo conectar a la base de datos después de {max_attempts} intentos")
                print(f"Error: {e}")
                return False
        except Exception as e:
            print(f"❌ Error inesperado al conectar a la base de datos: {e}")
            return False
    
    return False

def insertar_casos_ejemplo(cantidad_casos):
    """
    Ejecuta el script de insertar casos ejemplo
    """
    print(f"\n📝 Insertando {cantidad_casos} casos de ejemplo...")
    
    success = run_command(
        f"python -m tests.fixtures.insertar_casos_ejemplo {cantidad_casos}",
        f"Insertando {cantidad_casos} casos de ejemplo en la base de datos"
    )
    
    return success

def validar_argumentos():
    """
    Valida y procesa los argumentos de línea de comandos
    
    Returns:
        int or None: Número de casos a insertar, o None si no se especificó
    """
    if len(sys.argv) <= 1:
        return None
    
    try:
        cantidad = int(sys.argv[1])
        if cantidad <= 0:
            print("❌ Error: El número de casos debe ser mayor que 0")
            print("💡 Uso: python -m tests.reset_db [número_de_casos]")
            print("   Ejemplos:")
            print("     python -m tests.reset_db        # Solo reinicio")
            print("     python -m tests.reset_db 50     # Reinicio + 50 casos")
            print("     python -m tests.reset_db 100    # Reinicio + 100 casos")
            sys.exit(1)
        return cantidad
    except ValueError:
        print("❌ Error: El argumento debe ser un número entero")
        print("💡 Uso: python -m tests.reset_db [número_de_casos]")
        print("   Ejemplos:")
        print("     python -m tests.reset_db        # Solo reinicio")
        print("     python -m tests.reset_db 50     # Reinicio + 50 casos")
        print("     python -m tests.reset_db 100    # Reinicio + 100 casos")
        sys.exit(1)

def main():
    """
    Función principal que ejecuta la secuencia de despliegue
    """
    # Validar argumentos
    cantidad_casos = validar_argumentos()
    
    if cantidad_casos:
        print("🚀 Iniciando proceso de reinicio de base de datos con casos de ejemplo")
        print(f"📊 Se insertarán {cantidad_casos} casos de ejemplo después del reinicio")
    else:
        print("🚀 Iniciando proceso de reinicio de base de datos")
        print("📋 Solo se realizará el reinicio sin casos de ejemplo")
    
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent.parent
    if not (project_root / "docker-compose.yml").exists():
        print("❌ Error: No se encontró docker-compose.yml en el directorio del proyecto")
        sys.exit(1)
    
    # Cambiar al directorio del proyecto
    os.chdir(project_root)
    print(f"📁 Directorio de trabajo: {project_root.absolute()}")
    
    # Paso 1: Detener contenedores
    success = run_command(
        "docker compose down -v",
        "Deteniendo y eliminando contenedores con volúmenes"
    )
    if not success:
        print("\n❌ El proceso falló al detener contenedores")
        sys.exit(1)
    
    # Paso 2: Iniciar servicios
    success = run_command(
        "docker compose up -d",
        "Iniciando servicios en segundo plano"
    )
    if not success:
        print("\n❌ El proceso falló al iniciar servicios")
        sys.exit(1)
    
    # Paso 3: Esperar a que la base de datos esté lista
    if not wait_for_database():
        print("\n❌ El proceso falló: la base de datos no está disponible")
        print("💡 Sugerencias:")
        print("   • Verifica que Docker esté ejecutándose")
        print("   • Revisa las variables de entorno en el archivo .env")
        print("   • Ejecuta 'docker compose logs db' para ver los logs de la base de datos")
        sys.exit(1)
    
    # Paso 4: Aplicar migraciones
    success = run_command(
        "alembic upgrade head",
        "Aplicando migraciones de base de datos"
    )
    if not success:
        print("\n❌ El proceso falló al aplicar migraciones")
        print("💡 Sugerencias:")
        print("   • Verifica la configuración de Alembic en alembic.ini")
        print("   • Revisa las variables de entorno de la base de datos")
        print("   • Ejecuta 'alembic current' para ver el estado actual")
        sys.exit(1)
    
    # Paso 5: Insertar casos de ejemplo (opcional)
    if cantidad_casos:
        success = insertar_casos_ejemplo(cantidad_casos)
        if not success:
            print(f"\n⚠️  El reinicio fue exitoso pero falló la inserción de casos de ejemplo")
            print("💡 Puedes intentar insertar los casos manualmente con:")
            print(f"   python -m tests.fixtures.insertar_casos_ejemplo {cantidad_casos}")
        else:
            print(f"\n✅ Se insertaron {cantidad_casos} casos de ejemplo exitosamente")
    
    print("\n" + "=" * 70)
    print("🎉 ¡Proceso completado exitosamente!")
    print("📋 Resumen de acciones realizadas:")
    print("   • Contenedores Docker detenidos y volúmenes eliminados")
    print("   • Servicios Docker iniciados en segundo plano")
    print("   • Base de datos verificada y disponible")
    print("   • Migraciones de base de datos aplicadas")
    
    if cantidad_casos:
        print(f"   • {cantidad_casos} casos de ejemplo insertados")
    
    print("\n💡 El sistema está listo para usar")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)