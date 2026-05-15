# domain/banking/exceptions.py -- BankService
# Stub created in CAM-02 to allow entity debit()/credit() methods to function.
# Full documentation and additional exceptions will be added in CAM-03.
# Reference: context/DOMAIN.md Sec. 4 — Errores de dominio.


class BankingError(Exception):
    """Base class for all domain-level banking errors."""


class InsufficientFunds(BankingError):
    """Raised when an Account balance cannot cover a debit operation (INV-01)."""


class InvalidAmount(BankingError):
    """Raised when a financial operation amount is zero or negative (INV-03)."""
