import jwt
from datetime import datetime, timedelta, timezone
from App.fastapi_app.application.ports.security import TokenService
from App.fastapi_app.domain.auth.exceptions import InvalidCredentials

class PyJWTTokenService(TokenService):
    def __init__(self, secret_key: str = "super_secret_key", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict, expires_delta_minutes: int = 15) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidCredentials("Token has expired")
        except jwt.PyJWTError:
            raise InvalidCredentials("Invalid token")
