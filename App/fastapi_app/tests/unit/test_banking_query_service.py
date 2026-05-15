import pytest
from unittest.mock import MagicMock
from App.fastapi_app.application.banking.services import BankingQueryService
from App.fastapi_app.domain.banking.entities import Account, Movement, Wallet, MovementType
from App.fastapi_app.domain.banking.exceptions import AccountNotFound

def test_get_account_details_success():
    # Arrange
    account_repo = MagicMock()
    account = Account(id=1, user_id=10, balance=1000.0)
    account_repo.get_by_id.return_value = account
    
    service = BankingQueryService(account_repo, MagicMock(), MagicMock())
    
    # Act
    result = service.get_account_details(1)
    
    # Assert
    assert result.id == 1
    assert result.balance == 1000.0
    account_repo.get_by_id.assert_called_once_with(1)

def test_get_account_details_not_found():
    # Arrange
    account_repo = MagicMock()
    account_repo.get_by_id.return_value = None
    service = BankingQueryService(account_repo, MagicMock(), MagicMock())
    
    # Act & Assert
    with pytest.raises(AccountNotFound):
        service.get_account_details(99)

def test_get_movements_success():
    # Arrange
    account_repo = MagicMock()
    movement_repo = MagicMock()
    
    account = Account(id=1, user_id=10, balance=1000.0)
    account_repo.get_by_id.return_value = account
    
    movements = [
        Movement(id=1, account_id=1, type=MovementType.CREDIT, amount=500.0),
        Movement(id=2, account_id=1, type=MovementType.DEBIT, amount=200.0)
    ]
    movement_repo.get_by_account_id.return_value = movements
    
    service = BankingQueryService(account_repo, movement_repo, MagicMock())
    
    # Act
    result = service.get_movements(1)
    
    # Assert
    assert len(result) == 2
    assert result[0].amount == 500.0
    movement_repo.get_by_account_id.assert_called_once_with(1)

def test_get_user_financial_summary():
    # Arrange
    account_repo = MagicMock()
    wallet_repo = MagicMock()
    
    accounts = [Account(id=1, user_id=10, balance=1000.0), Account(id=2, user_id=10, balance=500.0)]
    wallets = [Wallet(id=101, user_id=10, balance=200.0)]
    
    account_repo.get_by_user_id.return_value = accounts
    wallet_repo.get_by_user_id.return_value = wallets
    
    service = BankingQueryService(account_repo, MagicMock(), wallet_repo)
    
    # Act
    summary = service.get_user_financial_summary(10)
    
    # Assert
    assert summary["user_id"] == 10
    assert len(summary["accounts"]) == 2
    assert len(summary["wallets"]) == 1
    assert summary["total_consolidated_balance"] == 1700.0
    account_repo.get_by_user_id.assert_called_once_with(10)
    wallet_repo.get_by_user_id.assert_called_once_with(10)
