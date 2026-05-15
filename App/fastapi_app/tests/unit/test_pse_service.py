import pytest
from unittest.mock import MagicMock
from App.fastapi_app.application.banking.services import PSEService
from App.fastapi_app.domain.banking.entities import Account, PSETransaction, PSEStatus
from App.fastapi_app.domain.banking.exceptions import InsufficientFunds, PSETransactionNotFound

def test_initiate_payment_success():
    """AC-01: Initialization with enough funds."""
    # Arrange
    uow = MagicMock()
    account = Account(id=1, user_id=1, balance=500.0)
    uow.accounts.get_by_id.return_value = account
    uow.__enter__.return_value = uow
    
    service = PSEService(uow)
    
    # Act
    tx_id = service.initiate_payment(1, 100.0)
    
    # Assert
    assert tx_id is not None
    uow.pse_transactions.save.assert_called_once()
    saved_tx = uow.pse_transactions.save.call_args[0][0]
    assert saved_tx.amount == 100.0
    assert saved_tx.status == PSEStatus.PENDING

def test_initiate_payment_insufficient_funds():
    """AC-02: Initialization with insufficient funds should fail."""
    # Arrange
    uow = MagicMock()
    account = Account(id=1, user_id=1, balance=50.0)
    uow.accounts.get_by_id.return_value = account
    uow.__enter__.return_value = uow
    service = PSEService(uow)
    
    # Act & Assert
    with pytest.raises(InsufficientFunds):
        service.initiate_payment(1, 100.0)

def test_process_webhook_approved():
    """AC-03: Webhook APPROVED should debit the account."""
    # Arrange
    uow = MagicMock()
    tx = PSETransaction(id="uuid-123", account_id=1, amount=100.0, status=PSEStatus.PENDING)
    account = Account(id=1, user_id=1, balance=500.0)
    
    uow.pse_transactions.get_by_transaction_id.return_value = tx
    uow.accounts.get_by_id.return_value = account
    uow.__enter__.return_value = uow
    
    service = PSEService(uow)
    
    # Act
    service.process_webhook("uuid-123", "APPROVED")
    
    # Assert
    assert account.balance == 400.0
    assert tx.status == PSEStatus.APPROVED
    uow.movements.save.assert_called_once()
    uow.accounts.save.assert_called_once()
    uow.__exit__.assert_called_once()

def test_process_webhook_rejected():
    """AC-04: Webhook REJECTED should not debit the account."""
    # Arrange
    uow = MagicMock()
    tx = PSETransaction(id="uuid-123", account_id=1, amount=100.0, status=PSEStatus.PENDING)
    uow.pse_transactions.get_by_transaction_id.return_value = tx
    uow.__enter__.return_value = uow
    service = PSEService(uow)
    
    # Act
    service.process_webhook("uuid-123", "REJECTED")
    
    # Assert
    assert tx.status == PSEStatus.REJECTED
    uow.accounts.save.assert_not_called()
    uow.movements.save.assert_not_called()

def test_webhook_transaction_not_found():
    """Arrojar PSETransactionNotFound si el ID no existe."""
    uow = MagicMock()
    uow.pse_transactions.get_by_transaction_id.return_value = None
    uow.__enter__.return_value = uow
    service = PSEService(uow)
    
    with pytest.raises(PSETransactionNotFound):
        service.process_webhook("unknown", "APPROVED")
