import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from App.fastapi_app.application.ports.repositories import UserRepository, AccountsRepository
from App.fastapi_app.application.ports.uow import UnitOfWork
from App.fastapi_app.application.ports.security import TokenService, PasswordHasher

def test_ports_are_importable():
    """
    Tests that the protocols and interfaces can be imported correctly
    and have no syntax or dependency issues.
    """
    assert UserRepository is not None
    assert AccountsRepository is not None
    assert UnitOfWork is not None
    assert TokenService is not None
    assert PasswordHasher is not None
