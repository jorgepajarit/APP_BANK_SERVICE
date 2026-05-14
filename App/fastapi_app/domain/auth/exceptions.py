from App.fastapi_app.domain.exceptions import DomainError

class AuthError(DomainError):
    """Base exception for all authentication-related errors."""
    pass

class UserNotFound(AuthError):
    """Raised when a requested user does not exist."""
    pass

class InvalidCredentials(AuthError):
    """Raised when a user attempts to authenticate with incorrect credentials."""
    pass
