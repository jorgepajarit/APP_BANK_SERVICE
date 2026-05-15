# domain/banking/entities.py -- BankService
# Pure domain entities. NO external framework imports allowed.
# Reference: context/DOMAIN.md (Sec. 1, 2, 3, 6)
# Invariants enforced: INV-01, INV-03 via debit()/credit() — exceptions raised from CAM-03.

from dataclasses import dataclass, field
from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum
from typing import List


class MovementType(Enum):
    """Discriminator for financial movements affecting an Account balance."""

    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


@dataclass(frozen=True)
class Movement:
    """Immutable historical record of a single financial transaction.

    Reference: context/DOMAIN.md — 'Movement: Registro histórico inmutable'.
    Uses frozen=True to enforce immutability: once a Movement is registered,
    it cannot be altered. This preserves the audit trail integrity.
    """

    id: int
    account_id: int
    movement_type: MovementType
    amount: Decimal
    created_at: datetime
    description: str


@dataclass
class Account:
    """Bank account associated with a User.

    Aggregate Root for the banking bounded context.
    Exposes debit() and credit() methods that enforce business invariants
    INV-01 (positive balance) and INV-03 (amount > 0) before mutating state.
    No code outside this entity may directly modify the balance field.

    Reference: context/DOMAIN.md Sec. 2 — 'Account actúa como la entidad
    principal que debe proteger las invariantes de negocio'.
    """

    id: int
    user_id: int
    account_type: str
    balance: Decimal
    movements: List[Movement] = field(default_factory=list)

    def debit(self, amount: Decimal, description: str = "Debit") -> Movement:
        """Deduct amount from balance, enforcing INV-01 and INV-03.

        Raises:
            InvalidAmount: if amount <= 0 (INV-03).
            InsufficientFunds: if balance < amount (INV-01).
        """
        # Late import to avoid circular dependency before CAM-03 exceptions exist.
        from domain.banking.exceptions import InsufficientFunds, InvalidAmount

        if amount <= Decimal("0"):
            raise InvalidAmount(
                f"Debit amount must be greater than zero, got: {amount}"
            )
        if self.balance < amount:
            raise InsufficientFunds(
                f"Insufficient funds: balance={self.balance}, requested={amount}"
            )

        self.balance -= amount
        movement = Movement(
            id=len(self.movements) + 1,
            account_id=self.id,
            movement_type=MovementType.DEBIT,
            amount=amount,
            created_at=datetime.now(UTC),
            description=description,
        )
        self.movements.append(movement)
        return movement

    def credit(self, amount: Decimal, description: str = "Credit") -> Movement:
        """Add amount to balance, enforcing INV-03.

        Raises:
            InvalidAmount: if amount <= 0 (INV-03).
        """
        from domain.banking.exceptions import InvalidAmount

        if amount <= Decimal("0"):
            raise InvalidAmount(
                f"Credit amount must be greater than zero, got: {amount}"
            )

        self.balance += amount
        movement = Movement(
            id=len(self.movements) + 1,
            account_id=self.id,
            movement_type=MovementType.CREDIT,
            amount=amount,
            created_at=datetime.now(UTC),
            description=description,
        )
        self.movements.append(movement)
        return movement


@dataclass
class Wallet:
    """Digital wallet associated with a User.

    An independent financial product from the main Account, used to
    manage separate fund pools (e.g., savings goals, reserved funds).
    Reference: context/DOMAIN.md Sec. 1 — 'Wallet'.
    """

    id: int
    user_id: int
    balance: Decimal
