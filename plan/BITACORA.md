# BITACORA.md -- Registro de implementación de BankService

- Pasos ejecutados: 10 de 15.
- Paso en curso: CAM-11 (Pendiente).
- Última actualización: 2026-05-14
- Rama de trabajo: main.

(Plan detallado en `plan/PLAN_ATOMICO.md`)

## Checklist de Pasos (Pendientes)
- [x] CAM-01 - Preparar entorno virtual y estructura de carpetas
- [x] CAM-02 - Crear entidades de negocio (`User`, `Account`, `Wallet`, `Movement`)
- [x] CAM-03 - Crear excepciones financieras (`InsufficientFunds`, `InvalidAmount`)
- [x] CAM-04 - Definir Puertos (Protocolos de Repositorios, UoW, Security)
- [x] CAM-05 - Implementar casos de uso de Autenticación (`LoginService`)
- [x] CAM-06 - Implementar consultas financieras (Saldos y Movimientos)
- [x] CAM-07 - Implementar servicio de Transferencias con reglas estrictas
- [x] CAM-08 - Implementar simulador y flujos de webhooks para PSE
- [x] CAM-09 - Implementar modo memoria (`MockRepository`, `MockUoW`)
- [x] CAM-10 - Implementar repositorios de SQLAlchemy y PostgreSQL
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

### Paso 5 - Implementar casos de uso de Autenticación (LoginService)
- **Fecha:** 2026-05-14 20:25
- **Archivos modificados:** `App/fastapi_app/application/auth/services.py`, `App/fastapi_app/tests/unit/test_login_service.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_login_service.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementó `LoginService` inyectando los puertos de seguridad y repositorios. Se validaron los casos de éxito, usuario inexistente y contraseña incorrecta arrojando `InvalidCredentials` (AC-01, AC-02, AC-03).

### Paso 6 - Implementar consultas financieras (Saldos y Movimientos)
- **Fecha:** 2026-05-14 20:28
- **Archivos modificados:** `App/fastapi_app/application/ports/repositories.py`, `App/fastapi_app/application/banking/services.py`, `App/fastapi_app/tests/unit/test_banking_query_service.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_banking_query_service.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementó `BankingQueryService` para centralizar la lógica de consulta de detalles de cuenta, historial de movimientos y resumen consolidado del usuario. Se actualizó el puerto `AccountsRepository` para incluir `get_by_user_id`.

### Paso 7 - Implementar servicio de Transferencias con reglas estrictas
- **Fecha:** 2026-05-14 20:30
- **Archivos modificados:** `App/fastapi_app/application/banking/services.py`, `App/fastapi_app/tests/unit/test_transfer_service.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_transfer_service.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementó `TransferService` utilizando el patrón `UnitOfWork` para asegurar la atomicidad de la operación (INV-04). Se validaron las invariantes de saldo suficiente (INV-01), cuentas distintas (INV-02) y montos positivos (INV-03).

### Paso 8 - Implementar simulador y flujos de webhooks para PSE
- **Fecha:** 2026-05-14 20:32
- **Archivos modificados:** `App/fastapi_app/domain/banking/entities.py`, `App/fastapi_app/application/ports/repositories.py`, `App/fastapi_app/application/banking/services.py`, `App/fastapi_app/tests/unit/test_pse_service.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_pse_service.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se formalizaron las entidades `PSETransaction` y `PSEStatus` en el dominio. Se implementó `PSEService` para manejar la inicialización de pagos y el callback asíncrono (webhooks). Se aseguró la protección contra doble procesamiento y la atomicidad mediante `UnitOfWork`.

### Paso 9 - Implementar modo memoria (MockRepository, MockUoW)
- **Fecha:** 2026-05-14 20:33
- **Archivos modificados:** `App/fastapi_app/adapters/outbound/persistence/memoria.py`, `App/fastapi_app/tests/unit/test_memoria_adapters.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_memoria_adapters.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementaron los adaptadores de salida en memoria para todos los repositorios y el Unit of Work. Esto permitirá desacoplar los tests unitarios de mocks manuales repetitivos y servirá como base para el "Modo Memoria" de la aplicación.

### Paso 10 - Implementar repositorios de SQLAlchemy y PostgreSQL
- **Fecha:** 2026-05-14 20:36
- **Archivos modificados:** `App/fastapi_app/adapters/outbound/persistence/sqlalchemy/orm.py`, `App/fastapi_app/adapters/outbound/persistence/sqlalchemy/repositories.py`, `App/fastapi_app/adapters/outbound/persistence/sqlalchemy/uow.py`, `App/fastapi_app/tests/unit/test_sqlalchemy_adapters.py`
- **Validación ejecutada:** `pytest App/fastapi_app/tests/unit/test_sqlalchemy_adapters.py`
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se implementó la persistencia real utilizando SQLAlchemy 2.0. Se optó por un mapeo imperativo para mantener las entidades de dominio totalmente limpias de dependencias del ORM. Se validó el funcionamiento del Unit of Work y los repositorios mediante una base de datos SQLite en memoria para pruebas.

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

### DEC-04 (Paso 6) - Extensión del Puerto AccountsRepository
- **Decisión:** Se añadió el método `get_by_user_id` a la interfaz del repositorio de cuentas.
- **Justificación:** Para cumplir con el requerimiento de negocio de "Resumen Financiero Consolidado" descrito en `CONTEXT.md`.
- **Impacto:** Permite al `BankingQueryService` agrupar todas las cuentas de un cliente de forma eficiente.

### DEC-05 (Paso 8) - Formalización de Entidades PSE
- **Decisión:** Se crearon las entidades `PSETransaction` y `PSEStatus` dentro del dominio de banking.
- **Justificación:** Para eliminar el uso de `Any` en los puertos y garantizar un tipado fuerte en la gestión de pagos externos asíncronos.
- **Impacto:** Mejora la trazabilidad de los pagos y permite validar estados en la capa de aplicación.

### DEC-06 (Paso 10) - Mapeo Imperativo en SQLAlchemy
- **Decisión:** Se utilizó `mapper_registry.map_imperatively` en lugar de herencia declarativa (`Base`).
- **Justificación:** Para cumplir con el principio de Arquitectura Hexagonal y DDD de mantener el núcleo (dominio) 100% independiente de frameworks de infraestructura.
- **Impacto:** Las entidades en `domain/` no heredan de nada ni tienen decoradores de SQLAlchemy, facilitando su portabilidad y testeo.

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
