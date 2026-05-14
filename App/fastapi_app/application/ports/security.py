from typing import Protocol

class TokenService(Protocol):
    def create_access_token(self, data: dict, expires_delta_minutes: int = 15) -> str:
        ...
    
    def decode_token(self, token: str) -> dict:
        ...

class PasswordHasher(Protocol):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...

    def get_password_hash(self, password: str) -> str:
        ...
