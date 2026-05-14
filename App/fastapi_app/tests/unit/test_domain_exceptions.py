import sys
import os
import pytest

# Ensure Python can find the App package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from App.fastapi_app.domain.exceptions import DomainError
from App.fastapi_app.domain.banking.exceptions import (
    BankingError, InsufficientFunds, InvalidAmount, SameAccount, AccountNotFound, PSETransactionNotFound
)
from App.fastapi_app.domain.auth.exceptions import AuthError, UserNotFound, InvalidCredentials

def test_banking_exceptions_inheritance():
    assert issubclass(BankingError, DomainError)
    assert issubclass(InsufficientFunds, BankingError)
    assert issubclass(InvalidAmount, BankingError)
    assert issubclass(SameAccount, BankingError)
    assert issubclass(AccountNotFound, BankingError)
    assert issubclass(PSETransactionNotFound, BankingError)

def test_auth_exceptions_inheritance():
    assert issubclass(AuthError, DomainError)
    assert issubclass(UserNotFound, AuthError)
    assert issubclass(InvalidCredentials, AuthError)

def test_raise_insufficient_funds():
    with pytest.raises(InsufficientFunds) as excinfo:
        raise InsufficientFunds("Not enough funds to cover the debit.")
    assert "Not enough funds" in str(excinfo.value)
