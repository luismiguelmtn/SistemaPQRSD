# 🔄 EJEMPLO PRÁCTICO: Flujo Completo de Datos

## 🎯 Objetivo
Vamos a seguir paso a paso qué sucede cuando un cliente crea un nuevo caso PQRSD, desde que envía los datos hasta que se guardan en la base de datos.

## 📱 Paso 1: Cliente Envía Petición

**El cliente hace una petición HTTP POST:**
```http
POST http://localhost:8000/casos/
Content-Type: application/json

{
    "tipo": "queja",
    "asunto": "Problema con el servicio",
    "descripcion": "El servicio de seguridad no llegó a tiempo según lo acordado",
    "nombre_solicitante": "María García",
    "email_solicitante": "maria.garcia@email.com",
    "telefono_solicitante": "3001234567"
}
```

## 🚪 Paso 2: FastAPI Recibe la Petición

**En `app/routers/caso.py` - Línea 80:**
```python
@router.post("/casos/", response_model=CasoResponse)
def crear_caso(caso: CasoCreate):
```

**¿Qué pasa aquí?**
1. FastAPI ve que la URL `/casos/` con método POST corresponde a esta función
2. Toma el JSON del cuerpo de la petición
3. **AUTOMÁTICAMENTE** convierte el JSON en un objeto `CasoCreate`
4. **VALIDA** que todos los datos sean correctos según las reglas en `models.py`

## ✅ Paso 3: Validación con Pydantic

**En `models.py` - CasoCreate:**
```python
class CasoCreate(BaseModel):
    tipo: TipoCaso  # Debe ser: peticion, queja, reclamo, sugerencia, denuncia
    asunto: str = Field(..., min_length=5, max_length=200)  # Entre 5 y 200 caracteres
    descripcion: str = Field(..., min_length=10, max_length=2000)  # Entre 10 y 2000 caracteres
    nombre_solicitante: str = Field(..., min_length=2, max_length=100)
    email_solicitante: EmailStr  # Debe ser un email válido
    telefono_solicitante: Optional[str] = Field(None, max_length=20)
```

**Pydantic verifica:**
- ✅ `"queja"` es un tipo válido (está en TipoCaso)
- ✅ `"Problema con el servicio"` tiene entre 5 y 200 caracteres
- ✅ La descripción tiene entre 10 y 2000 caracteres
- ✅ `"maria.garcia@email.com"` es un email válido
- ✅ El teléfono no supera 20 caracteres

**Si algo estuviera mal, FastAPI devolvería un error 422 automáticamente.**

## 🔄 Paso 4: Llamada a la Lógica de Negocio

**En `app/routers/caso.py` - Línea 111:**
```python
return crear_nuevo_caso(caso)
```

Esta línea llama a la función `crear_nuevo_caso()` que está en `app/services/caso.py`.

## 🧠 Paso 5: Procesamiento en Services

**En `app/services/caso.py` - función `crear_nuevo_caso()`:**
```python
def crear_nuevo_caso(caso_data: CasoCreate) -> CasoResponse:
    with get_database_session() as session:
        try:
            # 1. Generar número de caso único
            numero_caso = generar_numero_caso()
            
            # 2. Crear objeto de base de datos
            nuevo_caso = Caso.from_pydantic(caso_data, numero_caso)
            
            # 3. Guardar en la base de datos
            session.add(nuevo_caso)
            session.commit()
            session.refresh(nuevo_caso)
            
            # 4. Convertir a formato de respuesta
            return CasoResponse.model_validate(nuevo_caso.to_dict())
            
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear caso: {str(e)}")
```

**¿Qué hace cada paso?**

### 5.1 Generar Número de Caso
```python
numero_caso = generar_numero_caso(tipo="queja", anio=2025)  # Resultado: 1 (número secuencial)
# El formato legible se genera automáticamente: "QUE-2025-0001"
```

### 5.2 Crear Objeto de Base de Datos
```python
nuevo_caso = Caso.from_pydantic(caso_data, numero_caso)
```

Esto convierte nuestro `CasoCreate` en un objeto `Caso` (modelo de SQLAlchemy) que puede guardarse en la base de datos.

### 5.3 Guardar en Base de Datos
```python
session.add(nuevo_caso)    # Prepara para guardar
session.commit()           # Guarda definitivamente
session.refresh(nuevo_caso) # Obtiene el ID generado
```

## 💾 Paso 6: Interacción con la Base de Datos

**En `db_models.py` - clase Caso:**
```python
class Caso(Base):
    __tablename__ = "casos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_caso = Column(String(50), unique=True, nullable=False, index=True)
    tipo = Column(Enum(TipoCaso), nullable=False)
    # ... más columnas
```

**SQLAlchemy ejecuta algo como:**
```sql
INSERT INTO casos (
    numero_caso, anio, tipo, asunto, descripcion, 
    nombre_solicitante, email_solicitante, telefono_solicitante,
    estado, fecha_creacion, fecha_actualizacion
) VALUES (
    1, 2025, 'queja', 'Problema con el servicio',
    'El servicio de seguridad no llegó a tiempo según lo acordado',
    'María García', 'maria.garcia@email.com', '3001234567',
    'recibido', '2025-01-15 10:30:00', '2025-01-15 10:30:00'
);
```

## 📤 Paso 7: Respuesta al Cliente

**El objeto guardado se convierte a `CasoResponse`:**
```python
return CasoResponse.model_validate(nuevo_caso.to_dict())
```

**FastAPI devuelve al cliente:**
```json
{
    "id": 1,
    "numero_caso": 1,
    "anio": 2025,
    "numero_caso_completo": "QUE-2025-0001",
    "tipo": "queja",
    "asunto": "Problema con el servicio",
    "descripcion": "El servicio de seguridad no llegó a tiempo según lo acordado",
    "nombre_solicitante": "María García",
    "email_solicitante": "maria.garcia@email.com",
    "telefono_solicitante": "3001234567",
    "estado": "recibido",
    "fecha_creacion": "2025-01-15T10:30:00",
    "fecha_actualizacion": "2025-01-15T10:30:00",
    "respuesta": null
}
```

## 🔍 Resumen del Flujo Completo

```
Cliente (JSON) 
    ↓
🚪 FastAPI Router (app/routers/caso.py)
    ↓ 
✅ Validación Pydantic (models.py)
    ↓
🧠 Lógica de Negocio (app/services/caso.py)
    ↓
💾 Base de Datos (db_models.py + app/core/database.py)
    ↓
📤 Respuesta al Cliente (JSON)
```

## 🎯 Puntos Clave

1. **Automático**: FastAPI maneja automáticamente la conversión JSON ↔ Python
2. **Validación**: Pydantic valida los datos antes de que lleguen a tu código
3. **Separación**: Cada archivo tiene una responsabilidad específica
4. **Seguridad**: Las transacciones de base de datos se manejan con rollback en caso de error
5. **Consistencia**: Los datos se validan tanto al entrar como al salir

## 🛠️ ¿Dónde Está la "Magia"?

La "magia" está en que **FastAPI + Pydantic + SQLAlchemy** trabajan juntos:

- **FastAPI**: Maneja HTTP, routing, documentación automática
- **Pydantic**: Validación y serialización de datos
- **SQLAlchemy**: Interacción con la base de datos

Tú solo defines:
- Los modelos (estructura de datos)
- La lógica de negocio (qué hacer con los datos)
- Las rutas (cómo acceder a tu API)

¡Y todo lo demás funciona automáticamente! 🎉