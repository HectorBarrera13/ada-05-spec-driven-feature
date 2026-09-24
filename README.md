# Customer Search — ADA-05 Spec-Driven Feature

Feature de búsqueda de clientes (Customer Search) construida mediante la metodología **Spec-Driven Development** asistida por IA (Antigravity CLI / agy), desarrollada para la asignatura de **Ingeniería de Software Asistida por IA (UADY)**.

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Requisitos](#instalación-y-requisitos)
- [Uso de la Línea de Comandos (CLI)](#uso-de-la-línea-de-comandos-cli)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Trazabilidad y Flujo Spec-Driven](#trazabilidad-y-flujo-spec-driven)
- [Reflexión Académica (Sección 18 del ADA)](#reflexión-académica-sección-18-del-ada)

---

## Descripción General

Customer Search permite buscar clientes por nombre o correo electrónico soportando coincidencia parcial insensible a mayúsculas/minúsculas y normalización de caracteres acentuados (diacríticos), validación estricta de entradas y visualización en tabla formateada o JSON.

### Características Principales:
- **Búsqueda Flexible (FR-01, FR-02, FR-03)**: Búsqueda unificada en nombre y correo, o filtrado específico (`--name`, `--email`).
- **Normalización Unicode (SR-01, SR-02)**: Normalización NFKD para que términos como `"jose"` coincidan con `"José García"`.
- **Validación Robusta (FR-04, VR-01 a VR-03)**: Rechaza consultas vacías, de solo espacios en blanco o con menos de 2 caracteres (código de salida `2`).
- **Rendimiento Óptimo (NFR-01)**: Búsqueda en memoria de 10,000 registros en menos de 25 ms (límite: 100 ms).
- **Cero Dependencias en Runtime (NFR-03, C-01)**: Desarrollado exclusivamente con la biblioteca estándar de Python 3.11+.

---

## Estructura del Proyecto

```
ada-05-spec-driven-feature/
├── README.md                      # Documentación principal y reflexiones
├── REQUIREMENTS.md                # Requisitos funcionales y no funcionales (Fuente de verdad)
├── SPEC.md                        # Especificación verificable (Contrato técnico)
├── ARCHITECTURE.md                # Arquitectura de software, diagramas y decisiones
├── TASKS.md                       # Desglose de tareas T-01 a T-06
├── AGENTS.md                      # Reglas de ejecución para el agente de codificación
├── AI_USAGE_LOG.md                # Bitácora de uso e interacciones con IA
├── data/
│   └── customers.json             # Dataset semilla para pruebas y CLI
├── src/
│   └── customer_search/
│       ├── __init__.py
│       ├── models.py              # Entidades de dominio (Customer, SearchResult)
│       ├── repository.py          # Abstracción de datos (InMemoryCustomerRepository)
│       ├── service.py             # Lógica de búsqueda y normalización
│       ├── validation.py          # Reglas de validación de entrada
│       ├── exceptions.py          # Excepciones de dominio
│       └── cli.py                 # Interfaz de línea de comandos (CLI)
├── tests/
│   ├── __init__.py
│   ├── test_setup.py              # Test de importación y entorno
│   ├── test_models.py             # Pruebas de entidades y serialización
│   ├── test_repository.py         # Pruebas de repositorio y carga JSON
│   ├── test_service.py            # Pruebas de algoritmos de búsqueda y orden
│   ├── test_validation.py         # Pruebas de reglas de validación
│   ├── test_cli.py                # Pruebas de integración CLI y códigos de salida
│   └── test_performance.py       # Benchmark de 10,000 registros (<100ms)
├── docs/
│   └── traceability.md            # Matriz de trazabilidad extremo a extremo
└── results/
    └── agent-report.md            # Informe final de ejecución del agente
```

---

## Instalación y Requisitos

### Requisitos del Sistema:
- Python 3.11 o superior (probado en Python 3.14).
- `pytest` >= 8.0 para ejecución de pruebas automatizadas.

### Instalación:

1. Clonar el repositorio y acceder a la carpeta:
```bash
cd ada-05-spec-driven-feature
```

2. (Opcional) Crear y activar un entorno virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar en modo editable con herramientas de desarrollo:
```bash
pip install -e .
```

---

## Uso de la Línea de Comandos (CLI)

El comando puede ejecutarse directamente mediante `customer-search` o con `python3 -m customer_search.cli`:

### 1. Búsqueda unificada por nombre o correo (argumento posicional o `-q`):
```bash
PYTHONPATH=src python3 -m customer_search.cli "alice"
```
**Salida de ejemplo:**
```
ID       | Name          | Email                     | Phone       | Status
---------+---------------+---------------------------+-------------+-------
CUST-001 | Alice Johnson | alice.johnson@example.com | +1-555-0101 | Active

Found 1 customer(s) in 0.08 ms.
```

### 2. Coincidencia insensible a acentos / diacríticos:
```bash
PYTHONPATH=src python3 -m customer_search.cli "garcia"
```
Encuentra a `"José García"` gracias a la normalización Unicode NFKD.

### 3. Salida estructurada en JSON (`--json`):
```bash
PYTHONPATH=src python3 -m customer_search.cli "garcia" --json
```
**Salida JSON:**
```json
{
  "customers": [
    {
      "id": "CUST-005",
      "name": "José García",
      "email": "jose.garcia@soluciones.mx",
      "phone": "+52-999-1234567",
      "is_active": true
    }
  ],
  "total_count": 1,
  "query": "query='garcia'",
  "execution_time_ms": 0.091
}
```

### 4. Filtros específicos por nombre (`-n`) o correo (`-e`):
```bash
PYTHONPATH=src python3 -m customer_search.cli -n "Doe"
PYTHONPATH=src python3 -m customer_search.cli -e "acme.org"
```

### 5. Códigos de salida del proceso:
- `0`: Búsqueda exitosa (incluso si hay 0 coincidencias, mostrando mensaje amigable).
- `2`: Error de validación (consulta vacía, espacios en blanco o menos de 2 caracteres).
- `1`: Error de datos o archivo inexistente.

---

## Ejecución de Pruebas

Ejecuta el conjunto completo de pruebas automatizadas:

```bash
pytest -v
```

El conjunto incluye 36 pruebas divididas en:
- Pruebas unitarias de modelos y serialización (`test_models.py`).
- Pruebas del repositorio y manejo de archivos JSON corruptos/inexistentes (`test_repository.py`).
- Pruebas de la lógica de búsqueda, orden alfabético y diacríticos (`test_service.py`).
- Pruebas de validación de límites de entrada (`test_validation.py`).
- Pruebas de integración CLI de extremo a extremo (`test_cli.py`).
- Benchmark de rendimiento con 10,000 registros en memoria (`test_performance.py`).

---

## Trazabilidad y Flujo Spec-Driven

La trazabilidad completa desde la necesidad del usuario hasta la prueba de verificación se encuentra detallada en [`docs/traceability.md`](docs/traceability.md).

---

## Reflexión Académica (Sección 18 del ADA)

A continuación se responden de manera fundamentada las 12 preguntas de reflexión solicitadas por la guía del ADA-05:

### 1. ¿Qué diferencia hay entre requirement, specification y prompt?
- **Requirement**: Expresa la necesidad del negocio o usuario desde una perspectiva de alto nivel (el qué y el porqué), definiendo identificadores estables y criterios funcionales/no funcionales (ej. FR-01: "buscar clientes por nombre de forma insensible a mayúsculas").
- **Specification**: Es el contrato técnico detallado y verificable derivado del requisito (el cómo verificable). Define modelos de datos, reglas algorítmicas (ej. Unicode NFKD), restricciones de longitud, manejo de excepciones y criterios de aceptación medibles sin duplicar el texto del requisito.
- **Prompt**: Es la instrucción operativa o disparador conversacional suministrado al modelo/agente de IA en un momento dado para ejecutar una tarea acotada dentro del marco definido por la especificación.

### 2. ¿Qué información fue indispensable antes de programar?
Fue indispensable contar con:
- La definición exacta del modelo de datos (`Customer` con `id`, `name`, `email`, `phone`, `is_active`).
- Las reglas de validación explícitas (longitud mínima de 2 caracteres, no vacíos ni solo espacios).
- La resolución sobre caracteres especiales y acentos (normalización diacrítica).
- Los criterios de salida y códigos de estado (0 para éxito/0 resultados, 2 para validación, 1 para error de datos).
- El presupuesto de rendimiento no funcional (<100 ms para 10,000 registros).

### 3. ¿Qué decisiones debieron resolverse antes de programar?
1. Seleccionar la interfaz de entrega: se optó por un CLI local rápido y sin dependencias de red/servidor en lugar de una API FastAPI más pesada.
2. La estrategia de almacenamiento: repositorio en memoria con soporte de carga desde JSON local vs. base de datos externa.
3. El enfoque de indexación: escaneo lineal optimizado con normalización en memoria, que demostró ejecutarse en menos de 25 ms para 10k registros, evitando la sobrecarga de un motor FTS externo.

### 4. ¿Qué errores evitó SPEC.md?
Evitó que el agente de IA:
- Inventara reglas arbitrarias de validación o permitiera búsquedas de un solo carácter que generaran sobrecarga o resultados excesivos.
- Tratara una búsqueda con 0 coincidencias como un error o excepción de sistema.
- Modificara la firma de los datos en tiempo de codificación.
- Ignorara los casos de acentuación en nombres de habla hispana como "José" o "María".

### 5. ¿Qué problema evita separar REQUIREMENTS.md de SPEC.md?
Evita el acoplamiento entre la intención de negocio y la solución técnica. Si el negocio cambia la regla de búsqueda o agrega campos, `REQUIREMENTS.md` mantiene la trazabilidad original sin obligar a reescribir toda la especificación técnica. Asimismo, evita la duplicación inconsistente de requerimientos (principio Single Source of Truth).

### 6. ¿Qué papel tuvo AGENTS.md?
Actuó como la constitución o sistema de control de calidad del agente autónomo. Estableció directrices estrictas:
- Prohibición explícita de inventar requerimientos de negocio.
- Prohibición de alterar las especificaciones o debilitar pruebas para hacerlas pasar.
- Obligación de ejecutar pruebas antes y después de cada cambio y avanzar tarea por tarea según `TASKS.md`.

### 7. ¿Qué cambió durante la revisión humana?
- Se detectó y corrigió una inconsistencia en una aserción de punto flotante en las pruebas generada por el redondeo bancario de Python (`round half to even`).
- Se decidió desacoplar la validación de entrada en un módulo autónomo (`validation.py`) para fortalecer el principio de responsabilidad única.
- Se verificó que las búsquedas cortas (<2 caracteres) fallaran de forma controlada mediante `CustomerSearchValidationError` con código de salida 2.

### 8. ¿La arquitectura coincidió con el código final?
Sí, en un 100%. El código final refleja fielmente el diseño de capas establecido en `ARCHITECTURE.md`:
- Dominio inmutable (`models.py`).
- Capa de datos desacoplada mediante Protocol (`repository.py`).
- Servicio de negocio y normalización (`service.py`).
- Módulo de validación pura (`validation.py`).
- Interfaz CLI (`cli.py`).

### 9. ¿Qué requisito fue más difícil de probar?
El requisito no funcional de rendimiento (NFR-01: búsqueda en <100 ms para 10,000 registros). Requirió construir un fixture sintético generador de 10,000 clientes con datos realistas, asegurar que la generación del dataset no alterara la medición neta de la búsqueda y garantizar que la prueba fuera determinista sin depender de variaciones de hardware.

### 10. ¿Qué mejorarías en tu proceso spec-driven?
Incorporaría una etapa inicial de validación sintáctica automatizada de la especificación mediante herramientas de validación de esquemas (ej. Pydantic o JSON Schema) antes de iniciar las tareas, y agregaría pruebas de mutación (mutation testing) para garantizar que las pruebas cubran no solo las líneas de código, sino la totalidad de los caminos lógicos.

### 11. ¿Por qué SPEC.md puede funcionar como contrato verificable sin duplicar los requisitos?
Porque `SPEC.md` utiliza identificadores estables (`FR-01`, `FR-02`, etc.) en su sección `Requirements Covered` y traduce esos objetivos en reglas operativas (`SR-01`), reglas de validación (`VR-01`), criterios de aceptación (`AC-01`) y escenarios de prueba (`TS-01`). De este modo, cada línea de código y cada prueba apunta a un criterio verificable sin necesidad de repetir la narrativa del requerimiento original.

### 12. ¿Qué decisiones importantes aparecen en tu AI Usage Log y cómo cambió tu criterio después de revisar las sugerencias de la IA?
Aparecen decisiones como:
1. La adopción de escaneo lineal con normalización NFKD frente a la propuesta inicial de emplear SQLite FTS5, demostrando que la solución más simple cumplía con creces el presupuesto de rendimiento (<25ms vs <100ms) sin añadir dependencias.
2. La extracción de `validation.py` como módulo independiente tras observar que acoplar la validación al servicio dificultaba las pruebas de límites de entrada.
3. La corrección de aserciones flotantes causadas por el comportamiento nativo de redondeo en Python 3.14.
Esto reforzó el criterio de que el rol del desarrollador no es aceptar pasivamente el código de la IA, sino guiar la arquitectura, desafiar la complejidad innecesaria y velar por la rigurosidad de los contratos.
