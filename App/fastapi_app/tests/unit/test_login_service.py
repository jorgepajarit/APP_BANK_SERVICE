import pytest
from unittest.mock import MagicMock
from App.fastapi_app.application.auth.services import LoginService
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.auth.exceptions import InvalidCredentials

def test_login_success():
    """AC-01: Success case returning a token."""
    # Arrange
    user_repo = MagicMock()
    token_service = MagicMock()
    password_hasher = MagicMock()
    
    user = User(id=1, username="testuser", password_hash="hashed_pw")
    user_repo.get_by_username.return_value = user
    password_hasher.verify_password.return_value = True
    token_service.create_access_token.return_value = "fake-jwt-token"
    
    service = LoginService(user_repo, token_service, password_hasher)
    
    # Act
    token = service.login("testuser", "password123")
    
    # Assert
    assert token == "fake-jwt-token"
    password_hasher.verify_password.assert_called_once_with("password123", "hashed_pw")
    token_service.create_access_token.assert_called_once()

def test_login_invalid_user():
    """AC-02: Invalid user should raise InvalidCredentials."""
    # Arrange
    user_repo = MagicMock()
    user_repo.get_by_username.return_value = None
    service = LoginService(user_repo, MagicMock(), MagicMock())
    
    # Act & Assert
    with pytest.raises(InvalidCredentials):
        service.login("nonexistent", "password")

def test_login_invalid_password():
    """AC-03: Invalid password should raise InvalidCredentials."""
    # Arrange
    user_repo = MagicMock()
    password_hasher = MagicMock()
    
    user = User(id=1, username="testuser", password_hash="hashed_pw")
    user_repo.get_by_username.return_value = user
    password_hasher.verify_password.return_value = False
    
    service = LoginService(user_repo, MagicMock(), password_hasher)
    
    # Act & Assert
    with pytest.raises(InvalidCredentials):
        service.login("testuser", "wrongpassword")
