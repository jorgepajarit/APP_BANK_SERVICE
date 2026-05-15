# tests/unit/test_domain_entities.py -- BankService
# Unit tests for CAM-02: domain entities (User, Account, Wallet, Movement).
# No I/O, no database, no framework — pure Python only.
# Reference: context/DOMAIN.md, context/TECH_CONSTRAINTS.md Sec. 3

from datetime import datetime, UTC
from decimal import Decimal

import pytest

from domain.auth.entities import User
from domain.banking.entities import Account, Movement, MovementType, Wallet
from domain.banking.exceptions import InsufficientFunds, InvalidAmount


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------


class TestUser:
    def test_create_user_stores_fields(self) -> None:
        user = User(id=1, username="john_doe", hashed_password="$2b$12$hashed")
        assert user.id == 1
        assert user.username == "john_doe"
        assert user.hashed_password == "$2b$12$hashed"

    def test_user_is_mutable_dataclass(self) -> None:
        """User is not frozen — username could be updated if business requires it."""
        user = User(id=1, username="old_name", hashed_password="hash")
        user.username = "new_name"
        assert user.username == "new_name"


# ---------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------


class TestMovement:
    def _make_movement(
        self, movement_type: MovementType = MovementType.DEBIT
    ) -> Movement:
        return Movement(
            id=1,
            account_id=10,
            movement_type=movement_type,
            amount=Decimal("100.00"),
            created_at=datetime.now(UTC),
            description="Test movement",
        )

    def test_create_debit_movement(self) -> None:
        m = self._make_movement(MovementType.DEBIT)
        assert m.movement_type == MovementType.DEBIT
        assert m.amount == Decimal("100.00")
        assert m.account_id == 10

    def test_create_credit_movement(self) -> None:
        m = self._make_movement(MovementType.CREDIT)
        assert m.movement_type == MovementType.CREDIT

    def test_movement_is_immutable(self) -> None:
        """Frozen dataclass: altering fields must raise an error (audit integrity)."""
        m = self._make_movement()
        with pytest.raises((AttributeError, TypeError)):
            m.amount = Decimal("999.00")  # type: ignore[misc]

    def test_movement_type_string_values(self) -> None:
        assert MovementType.DEBIT.value == "DEBIT"
        assert MovementType.CREDIT.value == "CREDIT"


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


class TestAccount:
    def _make_account(self, balance: Decimal = Decimal("1000.00")) -> Account:
        return Account(
            id=1,
            user_id=5,
            account_type="savings",
            balance=balance,
        )

    def test_create_account_default_empty_movements(self) -> None:
        account = self._make_account()
        assert account.id == 1
        assert account.user_id == 5
        assert account.account_type == "savings"
        assert account.balance == Decimal("1000.00")
        assert account.movements == []

    def test_two_accounts_do_not_share_movements_list(self) -> None:
        """Each Account instance must have its own movements list (no shared mutable default)."""
        a1 = self._make_account()
        a2 = self._make_account()
        a1.movements.append("dummy")  # type: ignore[arg-type]
        assert len(a2.movements) == 0

    # --- debit() ---

    def test_debit_reduces_balance_and_records_movement(self) -> None:
        account = self._make_account(Decimal("500.00"))
        movement = account.debit(Decimal("200.00"), description="Test debit")

        assert account.balance == Decimal("300.00")
        assert len(account.movements) == 1
        assert movement.movement_type == MovementType.DEBIT
        assert movement.amount == Decimal("200.00")
        assert movement.account_id == account.id

    def test_debit_exact_balance_succeeds(self) -> None:
        """Debiting the exact remaining balance must succeed (INV-01 boundary)."""
        account = self._make_account(Decimal("100.00"))
        account.debit(Decimal("100.00"))
        assert account.balance == Decimal("0.00")

    def test_debit_raises_insufficient_funds(self) -> None:
        """INV-01: balance cannot go negative."""
        account = self._make_account(Decimal("50.00"))
        with pytest.raises(InsufficientFunds):
            account.debit(Decimal("51.00"))

    def test_debit_raises_invalid_amount_when_zero(self) -> None:
        """INV-03: amount must be strictly greater than zero."""
        account = self._make_account()
        with pytest.raises(InvalidAmount):
            account.debit(Decimal("0"))

    def test_debit_raises_invalid_amount_when_negative(self) -> None:
        """INV-03: negative amounts are forbidden."""
        account = self._make_account()
        with pytest.raises(InvalidAmount):
            account.debit(Decimal("-10.00"))

    def test_debit_does_not_record_movement_on_failure(self) -> None:
        """If debit raises, the movements list must remain unchanged (atomicity)."""
        account = self._make_account(Decimal("10.00"))
        with pytest.raises(InsufficientFunds):
            account.debit(Decimal("999.00"))
        assert account.movements == []
        assert account.balance == Decimal("10.00")

    # --- credit() ---

    def test_credit_increases_balance_and_records_movement(self) -> None:
        account = self._make_account(Decimal("200.00"))
        movement = account.credit(Decimal("300.00"), description="Test credit")

        assert account.balance == Decimal("500.00")
        assert len(account.movements) == 1
        assert movement.movement_type == MovementType.CREDIT
        assert movement.amount == Decimal("300.00")

    def test_credit_raises_invalid_amount_when_zero(self) -> None:
        account = self._make_account()
        with pytest.raises(InvalidAmount):
            account.credit(Decimal("0"))

    def test_credit_raises_invalid_amount_when_negative(self) -> None:
        account = self._make_account()
        with pytest.raises(InvalidAmount):
            account.credit(Decimal("-5.00"))

    def test_multiple_operations_accumulate_movements(self) -> None:
        """Consecutive debits and credits must all appear in the movements list."""
        account = self._make_account(Decimal("1000.00"))
        account.debit(Decimal("100.00"))
        account.credit(Decimal("50.00"))
        account.debit(Decimal("200.00"))

        assert account.balance == Decimal("750.00")
        assert len(account.movements) == 3
        assert account.movements[0].movement_type == MovementType.DEBIT
        assert account.movements[1].movement_type == MovementType.CREDIT
        assert account.movements[2].movement_type == MovementType.DEBIT


# ---------------------------------------------------------------------------
# Wallet
# ---------------------------------------------------------------------------


class TestWallet:
    def test_create_wallet_stores_fields(self) -> None:
        wallet = Wallet(id=3, user_id=5, balance=Decimal("250.00"))
        assert wallet.id == 3
        assert wallet.user_id == 5
        assert wallet.balance == Decimal("250.00")

    def test_wallet_balance_is_mutable(self) -> None:
        """Wallet balance can be modified directly (business logic delegated to services)."""
        wallet = Wallet(id=1, user_id=1, balance=Decimal("100.00"))
        wallet.balance += Decimal("50.00")
        assert wallet.balance == Decimal("150.00")
