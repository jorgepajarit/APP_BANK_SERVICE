from fastapi import Depends
from App.fastapi_app.adapters.outbound.persistence.memoria import InMemoryUnitOfWork
from App.fastapi_app.adapters.outbound.security.jwt_service import PyJWTTokenService
from App.fastapi_app.adapters.outbound.security.passlib_hasher import PasslibPasswordHasher
from App.fastapi_app.application.auth.services import LoginService
from App.fastapi_app.application.banking.services import BankingQueryService, TransferService, PSEService

# Global instance for memory persistence across requests
_mock_uow = InMemoryUnitOfWork()

def get_uow() -> InMemoryUnitOfWork:
    return _mock_uow

def get_token_service() -> PyJWTTokenService:
    return PyJWTTokenService()

def get_password_hasher() -> PasslibPasswordHasher:
    return PasslibPasswordHasher()

def get_login_service(
    uow: InMemoryUnitOfWork = Depends(get_uow),
    token_service: PyJWTTokenService = Depends(get_token_service),
    password_hasher: PasslibPasswordHasher = Depends(get_password_hasher)
) -> LoginService:
    return LoginService(uow.users, token_service, password_hasher)

def get_banking_query_service(uow: InMemoryUnitOfWork = Depends(get_uow)) -> BankingQueryService:
    return BankingQueryService(uow.accounts, uow.movements, uow.wallets)

def get_transfer_service(uow: InMemoryUnitOfWork = Depends(get_uow)) -> TransferService:
    return TransferService(uow)

def get_pse_service(uow: InMemoryUnitOfWork = Depends(get_uow)) -> PSEService:
    return PSEService(uow)
