from passlib.context import CryptContext
from App.fastapi_app.application.ports.security import PasswordHasher

# Using pbkdf2_sha256 as it does not require external C dependencies like bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class PasslibPasswordHasher(PasswordHasher):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
