from fastapi import Request, status
from fastapi.responses import JSONResponse
from App.fastapi_app.domain.exceptions import DomainError
from App.fastapi_app.domain.auth.exceptions import AuthError, InvalidCredentials
from App.fastapi_app.domain.banking.exceptions import (
    AccountNotFound, PSETransactionNotFound
)

async def domain_error_handler(request: Request, exc: DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(exc, AuthError):
        status_code = status.HTTP_401_UNAUTHORIZED
        if isinstance(exc, InvalidCredentials):
            return JSONResponse(status_code=status_code, content={"detail": "Invalid credentials"})
            
    if isinstance(exc, (AccountNotFound, PSETransactionNotFound)):
        status_code = status.HTTP_404_NOT_FOUND
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)}
    )
