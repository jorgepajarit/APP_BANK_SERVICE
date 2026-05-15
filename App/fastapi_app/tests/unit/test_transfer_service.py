import pytest
from unittest.mock import MagicMock
from App.fastapi_app.application.banking.services import TransferService
from App.fastapi_app.domain.banking.entities import Account
from App.fastapi_app.domain.banking.exceptions import (
    InsufficientFunds, 
    InvalidAmount, 
    SameAccount, 
    AccountNotFound
)

def test_transfer_success():
    """AC-01: Successful transfer between two accounts."""
    # Arrange
    uow = MagicMock()
    source = Account(id=1, user_id=1, balance=1000.0)
    target = Account(id=2, user_id=2, balance=500.0)
    
    uow.accounts.get_by_id.side_effect = lambda id: source if id == 1 else target
    uow.__enter__.return_value = uow
    
    service = TransferService(uow)
    
    # Act
    service.transfer(1, 2, 300.0)
    
    # Assert
    assert source.balance == 700.0
    assert target.balance == 800.0
    assert uow.movements.save.call_count == 2
    # commit() is called by __exit__ when no exception occurs
    uow.__exit__.assert_called_once()
    args, _ = uow.__exit__.call_args
    assert args[0] is None # No exception

def test_transfer_insufficient_funds():
    """AC-03: Transfer with more than available balance should fail (INV-01)."""
    # Arrange
    uow = MagicMock()
    source = Account(id=1, user_id=1, balance=100.0)
    target = Account(id=2, user_id=2, balance=500.0)
    uow.accounts.get_by_id.side_effect = lambda id: source if id == 1 else target
    uow.__enter__.return_value = uow
    
    service = TransferService(uow)
    
    # Act & Assert
    with pytest.raises(InsufficientFunds):
        service.transfer(1, 2, 300.0)
    
    # Verify __exit__ was called with an exception (causing rollback)
    uow.__exit__.assert_called_once()
    args, _ = uow.__exit__.call_args
    assert args[0] is InsufficientFunds

def test_transfer_invalid_amount():
    """AC-02: Transfer with amount <= 0 should fail (INV-03)."""
    service = TransferService(MagicMock())
    with pytest.raises(InvalidAmount):
        service.transfer(1, 2, 0)
    with pytest.raises(InvalidAmount):
        service.transfer(1, 2, -50)

def test_transfer_same_account():
    """AC-04: Transfer to the same account should fail (INV-02)."""
    service = TransferService(MagicMock())
    with pytest.raises(SameAccount):
        service.transfer(1, 1, 100.0)

def test_transfer_account_not_found():
    """Lanzar AccountNotFound si una de las cuentas no existe."""
    uow = MagicMock()
    uow.accounts.get_by_id.return_value = None
    uow.__enter__.return_value = uow
    service = TransferService(uow)
    with pytest.raises(AccountNotFound):
        service.transfer(1, 2, 100.0)
