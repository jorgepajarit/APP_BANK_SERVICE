# BITACORA.md -- Registro de implementación de BankService

- Pasos ejecutados: 4 de 15.
- Paso en curso: CAM-05 (Pendiente).
- Última actualización: 2026-05-14
- Rama de trabajo: main.

(Plan detallado en `plan/PLAN_ATOMICO.md`)

## Checklist de Pasos (Pendientes)
- [x] CAM-01 - Preparar entorno virtual y estructura de carpetas
- [x] CAM-02 - Crear entidades de negocio (`User`, `Account`, `Wallet`, `Movement`)
- [x] CAM-03 - Crear excepciones financieras (`InsufficientFunds`, `InvalidAmount`)
- [x] CAM-04 - Definir Puertos (Protocolos de Repositorios, UoW, Security)
- [ ] CAM-05 - Implementar casos de uso de Autenticación (`LoginService`)
- [ ] CAM-06 - Implementar consultas financieras (Saldos y Movimientos)
- [ ] CAM-07 - Implementar servicio de Transferencias con reglas estrictas
- [ ] CAM-08 - Implementar simulador y flujos de webhooks para PSE
- [ ] CAM-09 - Implementar modo memoria (`MockRepository`, `MockUoW`)
- [ ] CAM-10 - Implementar repositorios de SQLAlchemy y PostgreSQL
- [ ] CAM-11 - Desarrollar utilidades de seguridad (PyJWT, Passlib)
- [ ] CAM-12 - Exponer adaptadores de entrada HTTP (Routers de FastAPI)
- [ ] CAM-13 - Desarrollar aplicación cliente interactiva usando Flask
- [ ] CAM-14 - Configurar Docker (creación de Dockerfiles y docker-compose.yml)
- [ ] CAM-15 - Verificar métricas y lanzar CI (100% Cobertura)

---

## Registro de Pasos Ejecutados

### Paso 1 - Preparar entorno virtual y estructura de carpetas
- **Fecha:** 2026-05-13
- **Archivos modificados:** `requirements.txt`, creación de estructura en `App/`, y entorno virtual `.venv`.
- **Validación ejecutada:** `Get-ChildItem .\App\fastapi_app\domain ...` (Verificación estática)
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se creó la estructura base de carpetas de acuerdo con la Arquitectura Hexagonal y se inicializó el entorno virtual con las dependencias base en `requirements.txt`.

### Paso 2 - Crear entidades de negocio
- **Fecha:** 2026-05-13
- **Archivos modificados:** `App/fastapi_app/domain/auth/entities.py`, `App/fastapi_app/domain/banking/entities.py`, `App/fastapi_app/tests/unit/test_domain_entities.py`, `App/__init__.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_domain_entities.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se crearon las entidades base usando `dataclasses` puras en Python, separando `auth` (para User) y `banking` (para Account, Wallet y Movement). Se validaron con pruebas unitarias básicas.

### Paso 3 - Crear excepciones financieras y de autenticación
- **Fecha:** 2026-05-13
- **Archivos modificados:** `App/fastapi_app/domain/exceptions.py`, `App/fastapi_app/domain/banking/exceptions.py`, `App/fastapi_app/domain/auth/exceptions.py`, `App/fastapi_app/tests/unit/test_domain_exceptions.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_domain_exceptions.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementaron las excepciones puras de dominio. Heredan de una base común (`DomainError`) para facilitar su manejo global en los adaptadores más adelante, manteniendo el código libre de frameworks.

### Paso 4 - Definir Puertos de la Aplicación
- **Fecha:** 2026-05-13
- **Archivos modificados:** `App/fastapi_app/application/ports/repositories.py`, `App/fastapi_app/application/ports/uow.py`, `App/fastapi_app/application/ports/security.py`, `App/fastapi_app/tests/unit/test_ports.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_ports.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se definieron las interfaces (Puertos) que conectarán la infraestructura con los Casos de Uso. Se utilizó `typing.Protocol` para repositorios y utilidades, y `abc.ABC` para el patrón `UnitOfWork`.

<!-- Plantilla a copiar y rellenar cada vez que se finalice un paso -->
### Paso {N} - {Título corto del paso}
- **Fecha:** YYYY-MM-DD HH:MM
- **Archivos modificados:** `ruta/al/archivo1.py`, `ruta/al/archivo2.py`
- **Validación ejecutada:** `{comando de pytest o verificación estática}`
- **Resultado:** OK
- **Commit:** `hash` o `pendiente`
- **Observación técnica breve:** {Resumen de lo que se implementó en este paso}

---

## Registro de Decisiones Arquitectónicas (DEC)

### DEC-01 (Paso 2) - Separación de sub-dominios
- **Decisión:** Se crearon las carpetas `auth` y `banking` dentro del dominio.
- **Justificación:** Para mantener el Bounded Context de autenticación (User) separado de las reglas financieras (Account, Movement).
- **Impacto:** Ayudará a organizar los Casos de Uso y Puertos de manera más coherente en los siguientes pasos.

### DEC-02 (Paso 4) - Uso de `typing.Any` en PSETransactionRepository
- **Decisión:** Temporalmente se usó `Any` (tipado genérico) para la entidad de transacción PSE en el puerto.
- **Justificación:** La entidad pura `PSETransaction` no fue creada en CAM-02, pero como el webhook se maneja como un diccionario/json asíncrono, se usó un tipado flexible para evitar bloquear el diseño del puerto.
- **Impacto:** Si se decide tipar fuertemente las transacciones de la pasarela de pagos, se creará su propia entidad en pasos posteriores.

### DEC-03 (Documentación) - Adopción de estética Glassmorphism
- **Decisión:** Se definió oficialmente el estilo visual del frontend como "Glassmorphism" con Dark Mode.
- **Justificación:** Basado en la referencia del repositorio externo exitoso y para cumplir con el requisito de "experiencia premium" del usuario.
- **Impacto:** Se creó `specs/UI_SPEC_001_dashboard_bancario.md` y se actualizó el plan atómico para el paso CAM-13.

<!-- Plantilla para registrar decisiones técnicas importantes que se tomen sobre la marcha -->
### DEC-XX (Paso X) - {Título de la decisión}
- **Decisión:** {Qué se decidió implementar de cierta manera}
- **Justificación:** {Por qué se tomó esa decisión (apoyándose en los .md de contexto)}
- **Impacto:** {Qué efecto tiene esta decisión en pasos futuros}

---

## Registro de Bloqueos (BLOQ)

<!-- Plantilla para documentar errores graves, callejones sin salida o fugas en la arquitectura -->
### BLOQ-XX (Paso X) - {Título del bloqueo}
- **Síntoma:** {Qué está fallando exactamente}
- **Causa probable:** {Por qué creemos que falla}
- **Solución aplicada:** {Qué se hizo para salir del bloqueo}
- **Evidencia:** {Comando o test que demuestra que ya está resuelto}
