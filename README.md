# Sistema PQRSD

Sistema de Peticiones, Quejas, Reclamos, Sugerencias y Denuncias desarrollado con FastAPI.

## Descripción

Este sistema permite gestionar casos PQRSD de manera eficiente, proporcionando una API REST para crear, consultar, actualizar y obtener estadísticas de los casos.

## Estructura del Proyecto

```
pqrsd-eso/
├── main.py          # Configuración principal de FastAPI
├── routes.py        # Endpoints de la API
├── services.py      # Lógica de negocio y servicios
├── models.py        # Modelos Pydantic
├── enums.py         # Enumeraciones (TipoCaso, EstadoCaso)
├── requirements.txt # Dependencias del proyecto
├── venv/           # Entorno virtual (no incluir en git)
└── README.md       # Este archivo
```

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd pqrsd-eso
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   
   En Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   En macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Ejecutar el servidor

```bash
python -m uvicorn main:app --reload
```

El servidor estará disponible en: http://127.0.0.1:8000

### Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Documentación interactiva (Swagger)**: http://127.0.0.1:8000/docs
- **Documentación alternativa (ReDoc)**: http://127.0.0.1:8000/redoc

## Endpoints Principales

### Casos PQRSD

- `POST /casos/` - Crear un nuevo caso
- `GET /casos/` - Listar todos los casos (con filtros opcionales)
- `GET /casos/{caso_id}` - Obtener un caso por ID
- `GET /casos/numero/{numero_caso}` - Obtener un caso por número
- `PUT /casos/{caso_id}` - Actualizar un caso

### Estadísticas

- `GET /estadisticas/` - Obtener estadísticas del sistema

### Ejemplo de uso

#### Crear un nuevo caso

```bash
curl -X POST "http://127.0.0.1:8000/casos/" \
     -H "Content-Type: application/json" \
     -d '{
       "tipo": "peticion",
       "asunto": "Solicitud de información",
       "descripcion": "Necesito información sobre...",
       "nombre_solicitante": "Juan Pérez",
       "email_solicitante": "juan@email.com",
       "telefono_solicitante": "123456789"
     }'

**Respuesta esperada:**
```json
{
  "id": 1,
  "numero_caso": "PET-0001",
  "tipo": "peticion",
  "estado": "recibido",
  "asunto": "Solicitud de información",
  "descripcion": "Necesito información sobre los horarios de atención",
  "nombre_solicitante": "Juan Pérez",
  "email_solicitante": "juan@email.com",
  "telefono_solicitante": "123456789",
  "fecha_creacion": "2024-01-15T10:30:00",
  "fecha_actualizacion": "2024-01-15T10:30:00",
  "respuesta": null
}
```

#### 📋 Listar casos con filtros

**Ver todos los casos:**
```bash
curl "http://127.0.0.1:8000/casos/"
```

**Ver solo las peticiones:**
```bash
curl "http://127.0.0.1:8000/casos/?tipo=peticion"
```

**Ver solo casos pendientes:**
```bash
curl "http://127.0.0.1:8000/casos/?estado=recibido"
```

#### 📊 Ver estadísticas

```bash
curl "http://127.0.0.1:8000/estadisticas/"
```

**Respuesta esperada:**
```json
{
  "total_casos": 5,
  "por_tipo": {
    "peticion": 2,
    "queja": 1,
    "reclamo": 1,
    "sugerencia": 1
  },
  "por_estado": {
    "recibido": 3,
    "en_proceso": 1,
    "resuelto": 1
  }
}
```
```

## Tipos de Casos

- **PETICION**: Solicitudes de información o servicios (Prefijo: PET)
- **QUEJA**: Manifestaciones de insatisfacción (Prefijo: QUE)
- **RECLAMO**: Solicitudes de corrección o compensación (Prefijo: REC)
- **SUGERENCIA**: Propuestas de mejora (Prefijo: SUG)
- **DENUNCIA**: Reportes de irregularidades (Prefijo: DEN)

### Formato de Números de Caso

Cada caso recibe un número único legible con el formato: `PREFIJO-NNNN`

Ejemplos:
- `PET-0001`: Primera petición
- `QUE-0001`: Primera queja
- `REC-0002`: Segunda reclamación

### Sistema de IDs

- **ID interno**: Entero secuencial (1, 2, 3, ...) para uso del sistema
- **Número de caso**: Formato legible para usuarios y seguimiento

## Estados de Casos

- **RECIBIDO**: Caso recién creado
- **EN_PROCESO**: Caso en revisión
- **RESUELTO**: Caso con respuesta
- **CERRADO**: Caso finalizado

## Desarrollo

### Estructura de archivos

- `main.py`: Punto de entrada de la aplicación
- `routes.py`: Definición de rutas y endpoints
- `services.py`: Lógica de negocio y operaciones de datos
- `models.py`: Esquemas de datos con Pydantic
- `enums.py`: Enumeraciones para tipos y estados

### Desactivar entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

## Notas

- Este proyecto utiliza una "base de datos" en memoria para fines educativos
- En producción, se recomienda usar una base de datos real (PostgreSQL, MySQL, etc.)
- El entorno virtual (`venv/`) no debe incluirse en el control de versiones

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Python 3.8+**: Lenguaje de programación