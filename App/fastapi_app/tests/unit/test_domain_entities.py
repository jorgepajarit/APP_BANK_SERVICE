import sys
import os

# Asegurarse de que Python pueda encontrar el paquete App
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from datetime import datetime
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account, Wallet, Movement, MovementType

def test_create_user():
    user = User(id=1, username="test_user", password_hash="hashed")
    assert user.id == 1
    assert user.username == "test_user"

def test_create_account():
    account = Account(id=1, user_id=1, balance=100.0)
    assert account.id == 1
    assert account.user_id == 1
    assert account.balance == 100.0

def test_create_wallet():
    wallet = Wallet(id=1, user_id=1, balance=50.0)
    assert wallet.id == 1
    assert wallet.user_id == 1
    assert wallet.balance == 50.0

def test_create_movement():
    mov = Movement(id=1, account_id=1, type=MovementType.CREDIT, amount=50.0)
    assert mov.id == 1
    assert mov.account_id == 1
    assert mov.type == MovementType.CREDIT
    assert mov.amount == 50.0
    assert isinstance(mov.created_at, datetime)
