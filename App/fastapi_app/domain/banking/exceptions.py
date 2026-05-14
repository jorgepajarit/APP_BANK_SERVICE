from App.fastapi_app.domain.exceptions import DomainError

class BankingError(DomainError):
    """Base exception for all banking-related errors."""
    pass

class InsufficientFunds(BankingError):
    """Raised when an account does not have enough balance for a transaction."""
    pass

class SameAccount(BankingError):
    """Raised when the source and target accounts of a transfer are the same."""
    pass

class InvalidAmount(BankingError):
    """Raised when an operation is attempted with an amount <= 0."""
    pass

class AccountNotFound(BankingError):
    """Raised when an operation requests an account that does not exist."""
    pass

class PSETransactionNotFound(BankingError):
    """Raised when a PSE webhook refers to an unknown transaction."""
    pass
