# BITACORA.md -- Registro de implementación de BankService
- Pasos ejecutados: 2 de 15.
- Paso en curso: CAM-03.
- Última actualización: 2026-05-14
- Rama de trabajo: test2.

(Plan detallado en `plan/PLAN_ATOMICO.md`)

## Checklist de Pasos (Pendientes)
- [x] CAM-01 - Preparar entorno virtual y estructura de carpetas
- [x] CAM-02 - Crear entidades de negocio (`User`, `Account`, `Wallet`, `Movement`)
- [] CAM-03 - Crear excepciones financieras (`InsufficientFunds`, `InvalidAmount`)
- [] CAM-04 - Definir Puertos (Protocolos de Repositorios, UoW, Security)
- [] CAM-05 - Implementar casos de uso de Autenticación (`LoginService`)
- [] CAM-06 - Implementar consultas financieras (Saldos y Movimientos)
- [] CAM-07 - Implementar servicio de Transferencias con reglas estrictas
- [] CAM-08 - Implementar simulador y flujos de webhooks para PSE
- [] CAM-09 - Implementar modo memoria (`MockRepository`, `MockUoW`)
- [] CAM-10 - Implementar repositorios de SQLAlchemy y PostgreSQL
- [] CAM-11 - Desarrollar utilidades de seguridad (PyJWT, Passlib)
- [] CAM-12 - Exponer adaptadores de entrada HTTP (Routers de FastAPI)
- [] CAM-13 - Desarrollar aplicación cliente interactiva usando Flask
- [] CAM-14 - Configurar Docker (creación de Dockerfiles y docker-compose.yml)
- [] CAM-15 - Verificar métricas y lanzar CI (100% Cobertura)

## Registro de Pasos Ejecutados

### Paso 1 - Preparar entorno virtual y estructura de carpetas
- **Fecha:** 2026-05-14
- **CAM:** CAM-01
- **Archivos creados:**
  - `.venv/` (entorno virtual Python 3.12.7)
  - `App/fastapi_app/domain/__init__.py`
  - `App/fastapi_app/application/__init__.py`
  - `App/fastapi_app/adapters/__init__.py` (+ inbound/http, outbound)
  - `App/fastapi_app/tests/__init__.py` (+ unit/, e2e/)
  - `App/fastapi_app/main.py`
  - `App/fastapi_app/requirements.txt`
  - `App/fastapi_app/pytest.ini`
  - `App/flask_app/requirements.txt`
- **Validación ejecutada:**
  - `.venv\Scripts\python.exe --version` → Python 3.12.7 ✅
  - `.venv\Scripts\pytest.exe --version` → pytest 8.2.0 ✅
  - Verificación arquitectónica: `domain/` sin imports de infraestructura ✅
- **Resultado:** OK
- **Commit:** pendiente
- **Observación técnica breve:** Se creó la estructura de carpetas definida en `context/ARCHITECTURE.md` Sec. 3. El `.venv` aísla todas las dependencias de `requirements.txt`. La estructura `domain/`, `application/`, `adapters/inbound/http`, `adapters/outbound` y `tests/unit`, `tests/e2e` está 100% alineada con la Arquitectura Hexagonal. Se configuró `pytest.ini` apuntando a `domain` y `application` para asegurar cobertura desde CAM-02.

### Paso 2 - Crear entidades de negocio
- **Fecha:** 2026-05-14
- **CAM:** CAM-02
- **Archivos creados:**
  - `domain/auth/__init__.py`
  - `domain/auth/entities.py` → `User` (dataclass, aggregate root auth)
  - `domain/banking/__init__.py`
  - `domain/banking/entities.py` → `Account`, `Wallet`, `Movement` (frozen), `MovementType`
  - `domain/banking/exceptions.py` → stub `BankingError`, `InsufficientFunds`, `InvalidAmount`
  - `tests/unit/test_domain_entities.py` → 20 tests unitarios
  - `conftest.py` → configuración de sys.path para pytest
- **Validación ejecutada:** `pytest tests/unit/test_domain_entities.py -v --cov=domain --cov-report=term-missing`
- **Resultado:** OK — 20/20 passed, 100% coverage, 0.38s, sin warnings
- **Commit:** pendiente
- **Observación técnica breve:** Se crearon entidades puras Python (sin imports de infraestructura). `Movement` usa `frozen=True` para garantizar inmutabilidad del historial. `Account.debit()`/`credit()` protegen INV-01 e INV-03 con late-import de excepciones de dominio. Se creó un stub de `exceptions.py` (se expande en CAM-03). Uso de `datetime.now(UTC)` en lugar del deprecado `utcnow()` para compatibilidad con Python 3.12+.

### DEC-01 (Paso 2) - Lógica de invariantes en la entidad Account
- **Decisión:** Se implementaron `debit()` y `credit()` directamente en `Account` (no solo en el servicio de aplicación).
- **Justificación:** `DOMAIN.md` Sec. 2 establece que Account debe proteger las invariantes de negocio antes de generar Movements. Colocar la validación solo en el servicio violaría el encapsulamiento DDD.
- **Impacto:** `TransferService` (CAM-07) llamará a `account.debit()` y `account.credit()`, delegando la validación de INV-01/INV-03 a la entidad.

<!-- Plantilla para registrar decisiones técnicas importantes que se tomen sobre la marcha -->
### DEC-XX (Paso X) - {Título de la decisión}
- **Decisión:** {Qué se decidió implementar de cierta manera}
- **Justificación:** {Por qué se tomó esa decisión (apoyándose en los .md de contexto)}
- **Impacto:** {Qué efecto tiene esta decisión en pasos futuros}


## Registro de Bloqueos (BLOQ)
<!-- Plantilla para documentar errores graves, callejones sin salida o fugas en la arquitectura -->
### BLOQ-XX (Paso X) - {Título del bloqueo}
- **Síntoma:** {Qué está fallando exactamente}
- **Causa probable:** {Por qué creemos que falla}
- **Solución aplicada:** {Qué se hizo para salir del bloqueo}
- **Evidencia:** {Comando o test que demuestra que ya está resuelto}
