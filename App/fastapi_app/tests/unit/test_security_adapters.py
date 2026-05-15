import pytest
from App.fastapi_app.adapters.outbound.security.jwt_service import PyJWTTokenService
from App.fastapi_app.adapters.outbound.security.passlib_hasher import PasslibPasswordHasher
from App.fastapi_app.domain.auth.exceptions import InvalidCredentials

def test_passlib_hasher():
    hasher = PasslibPasswordHasher()
    password = "secure_password"
    hashed = hasher.get_password_hash(password)
    
    assert hashed != password
    assert hasher.verify_password(password, hashed) is True
    assert hasher.verify_password("wrong_password", hashed) is False

def test_jwt_token_service():
    service = PyJWTTokenService(secret_key="test_secret")
    data = {"sub": "user123"}
    
    # Test valid token
    token = service.create_access_token(data, expires_delta_minutes=15)
    decoded = service.decode_token(token)
    
    assert decoded["sub"] == "user123"
    assert "exp" in decoded

def test_jwt_token_service_expired():
    service = PyJWTTokenService(secret_key="test_secret")
    data = {"sub": "user123"}
    
    # Expire immediately (-1 minutes)
    token = service.create_access_token(data, expires_delta_minutes=-1)
    
    with pytest.raises(InvalidCredentials, match="Token has expired"):
        service.decode_token(token)

def test_jwt_token_service_invalid():
    service = PyJWTTokenService(secret_key="test_secret")
    
    with pytest.raises(InvalidCredentials, match="Invalid token"):
        service.decode_token("invalid.token.string")
