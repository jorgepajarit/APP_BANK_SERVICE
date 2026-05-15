from App.fastapi_app.application.ports.repositories import UserRepository
from App.fastapi_app.application.ports.security import TokenService, PasswordHasher
from App.fastapi_app.domain.auth.exceptions import InvalidCredentials

class LoginService:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenService,
        password_hasher: PasswordHasher
    ):
        self.user_repo = user_repo
        self.token_service = token_service
        self.password_hasher = password_hasher

    def login(self, username: str, password: str) -> str:
        """
        Authenticates a user and returns a JWT token.
        Follows FEATURE_SPEC_002_autenticacion.
        """
        user = self.user_repo.get_by_username(username)
        
        # AC-02: User not found
        if not user:
            raise InvalidCredentials("Invalid username or password")
        
        # AC-03: Invalid password
        if not self.password_hasher.verify_password(password, user.password_hash):
            raise InvalidCredentials("Invalid username or password")
            
        # AC-01: Success
        token = self.token_service.create_access_token(data={"sub": user.username})
        return token
