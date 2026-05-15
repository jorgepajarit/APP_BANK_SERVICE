from fastapi import APIRouter, Depends
from App.fastapi_app.adapters.inbound.http.schemas import LoginRequest, TokenResponse
from App.fastapi_app.application.auth.services import LoginService
from App.fastapi_app.adapters.inbound.http.dependencies import get_login_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, login_service: LoginService = Depends(get_login_service)):
    token = login_service.login(request.username, request.password)
    return TokenResponse(access_token=token)
