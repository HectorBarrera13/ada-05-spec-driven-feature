# AI Usage Log — ADA-05 Spec-Driven Feature

This document records the key interactions, AI proposals, human engineering decisions, and product impacts across the spec-driven development lifecycle of ADA-05.

---

### Entry 1: Requirements & Specification Definition (Fases 1 y 2)

- **Stage**: Requirements & Specification (`REQUIREMENTS.md`, `SPEC.md`)
- **Context / Prompt**:
  Le pedí a la IA estructurar los requerimientos funcionales y no funcionales para la funcionalidad de búsqueda de clientes (Customer Search). Establecí que debíamos permitir criterios flexibles pero apegándonos estrictamente al template y reglas de la especificación ADA-05.
- **AI Proposal**:
  La IA propuso un alcance inicial con 6 requerimientos funcionales (FR-01 a FR-06) para búsqueda parcial insensible a mayúsculas/minúsculas por nombre, correo y consulta unificada, además de reglas de validación (>= 2 caracteres), manejo de resultados vacíos y ordenamiento alfabético. Para los no funcionales, sugirió rendimiento menor a 100ms para 10k registros, usabilidad en CLI con `--json` y códigos de salida estándar, y cero dependencias de terceros en runtime.
- **Human Decision / Adjustment**:
  Acepté el set de requerimientos y añadí consideraciones clave: definí el manejo de caracteres especiales (Q-01) implementando normalización Unicode NFKD (para que acentos como "José" coincidan con "jose") y establecí que los datos de prueba usen por defecto un archivo JSON local (`data/customers.json`). Además, aseguré que `SPEC.md` referenciara los requerimientos por ID sin duplicar definiciones.
- **Impact on Product**:
  Se crearon criterios y límites verificables que previnieron el _scope creep_ antes de escribir código.

---

### Entry 2: Architectural Modeling and Layered Design (Fase 3)

- **Stage**: Architecture (`ARCHITECTURE.md`)
- **Context / Prompt**:
  Planteé a la IA el diseño de los componentes, responsabilidades, flujo de datos e interfaces para la herramienta CLI de búsqueda de clientes, evaluando si convenía un índice invertido (como SQLite FTS) frente a un escaneo lineal en memoria.
- **AI Proposal**:
  La IA sugirió una arquitectura limpia por capas con un Modelo de Dominio (`Customer`, `SearchResult`), un Protocolo de Repositorio (`CustomerRepository`), Capa de Servicio (`CustomerSearchService`) y la Interfaz CLI (`cli.py`), evaluando las opciones de indexación.
- **Human Decision / Adjustment**:
  Decidí optar por el escaneo lineal en memoria con normalización Unicode. Para conjuntos de hasta 10,000 registros, el escaneo lineal se ejecuta en ~15ms, lo que elimina complejidad innecesaria, evita problemas de sincronización con bases de datos y mantiene el proyecto 100% alineado con la restricción de cero dependencias (C-01).
- **Impact on Product**:
  Se mantuvo una base de código ligera, modular, fácil de probar con mocks puros y totalmente libre de dependencias externas.

---

### Entry 3: Domain Implementation & Validation Separation (Fases 4 y 7: T-02, T-03, T-04)

- **Stage**: Implementation & Refactoring (`src/customer_search/`)
- **Context / Prompt**:
  Le indiqué a la IA implementar la entidad de dominio, el repositorio, el servicio de búsqueda y la lógica de validación acorde a las tareas T-02, T-03 y T-04.
- **AI Proposal**:
  En su implementación inicial, la IA colocó la lógica de validación directamente dentro de `service.py`. Al probar la serialización en `test_models.py`, el redondeo nativo de Python (`round(1.2345, 3)`) generó un detalle por el redondeo bancario (_round half to even_).
- **Human Decision / Adjustment**:

1. Decidí desacoplar la validación en su propio módulo (`src/customer_search/validation.py`) para cumplir con el Principio de Responsabilidad Única y permitir pruebas unitarias independientes de los límites de consulta (VR-01, VR-02, VR-03).
2. Ajusté las aserciones de pruebas en punto flotante para utilizar representaciones estables y no ambiguas (`1.25`).

- **Impact on Product**:
  Mayor separación de intereses, aislamiento total de pruebas para reglas de validación y aserciones de pruebas más robustas.

---

### Entry 4: CLI Implementation, Performance Verification & Delivery (Fases 4, 7, 8, 9: T-05, T-06)

- **Stage**: Testing, CLI Presentation & Verification (`cli.py`, `test_cli.py`, `test_performance.py`)
- **Context / Prompt**:
  Le pedí a la IA implementar la interfaz de línea de comandos (CLI), pruebas de integración de punta a punta (E2E) y automatizar la verificación del requerimiento NFR-01 (10,000 registros en menos de 100ms).
- **AI Proposal**:
  La IA propuso añadir soporte para argumentos posicionales además de los flags explícitos `-q/--query`, `-n/--name` y `-e/--email`, junto con una prueba de rendimiento que generara 10,000 registros sintéticos y códigos de salida POSIX estándar (0 para éxito/sin coincidencias, 2 para errores de validación y 1 para errores de archivo/runtime).
- **Human Decision / Adjustment**:
  Acepté el diseño de la CLI y la especificación de códigos de salida. Verifiqué personalmente que `pytest` ejecutara con éxito las 36 pruebas y que el benchmark de 10,000 registros corriera en ~15-25ms (muy por debajo del umbral de 100ms).
- **Impact on Product**:
  Se entregó una experiencia de terminal pulida y amigable, con opciones de salida tabular y en formato JSON, verificada mediante pruebas automatizadas de integración y rendimiento.
