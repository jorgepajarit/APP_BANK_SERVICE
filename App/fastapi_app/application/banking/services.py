from typing import List, Dict, Any
from App.fastapi_app.application.ports.repositories import AccountsRepository, MovementRepository, WalletRepository
from App.fastapi_app.application.ports.uow import UnitOfWork
from App.fastapi_app.domain.banking.entities import Account, Movement, Wallet, MovementType, PSETransaction, PSEStatus
from App.fastapi_app.domain.banking.exceptions import (
    InsufficientFunds, 
    InvalidAmount, 
    SameAccount, 
    AccountNotFound,
    PSETransactionNotFound
)

class BankingQueryService:
    def __init__(
        self,
        account_repo: AccountsRepository,
        movement_repo: MovementRepository,
        wallet_repo: WalletRepository
    ):
        self.account_repo = account_repo
        self.movement_repo = movement_repo
        self.wallet_repo = wallet_repo

    def get_account_details(self, account_id: int) -> Account:
        """
        Retrieves the details of a specific account, including its balance.
        """
        account = self.account_repo.get_by_id(account_id)
        if not account:
            raise AccountNotFound(f"Account with ID {account_id} not found")
        return account

    def get_movements(self, account_id: int) -> List[Movement]:
        """
        Retrieves the history of movements for a specific account.
        """
        self.get_account_details(account_id)
        return self.movement_repo.get_by_account_id(account_id)

    def get_user_financial_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Consolidates all accounts and wallets for a specific user.
        """
        accounts = self.account_repo.get_by_user_id(user_id)
        wallets = self.wallet_repo.get_by_user_id(user_id)
        
        total_balance = sum(a.balance for a in accounts) + sum(w.balance for w in wallets)
        
        return {
            "user_id": user_id,
            "accounts": accounts,
            "wallets": wallets,
            "total_consolidated_balance": total_balance
        }

class TransferService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def transfer(self, source_id: int, target_id: int, amount: float) -> None:
        """
        Executes an atomic transfer between two accounts.
        Follows FEATURE_SPEC_001_transferir_fondos and protects INV-01 to INV-04.
        """
        if amount <= 0:
            raise InvalidAmount("Amount must be greater than zero")

        if source_id == target_id:
            raise SameAccount("Source and target accounts must be different")

        with self.uow:
            source = self.uow.accounts.get_by_id(source_id)
            target = self.uow.accounts.get_by_id(target_id)

            if not source or not target:
                raise AccountNotFound("One or both accounts were not found")

            if source.balance < amount:
                raise InsufficientFunds(f"Insufficient funds in account {source_id}")

            source.balance -= amount
            target.balance += amount

            debit_move = Movement(id=None, account_id=source_id, type=MovementType.DEBIT, amount=amount)
            credit_move = Movement(id=None, account_id=target_id, type=MovementType.CREDIT, amount=amount)

            self.uow.accounts.save(source)
            self.uow.accounts.save(target)
            self.uow.movements.save(debit_move)
            self.uow.movements.save(credit_move)

class PSEService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def initiate_payment(self, account_id: int, amount: float) -> str:
        """
        Initializes a PSE payment process.
        Follows FEATURE_SPEC_003 (AC-01, AC-02).
        """
        if amount <= 0:
            raise InvalidAmount("Amount must be greater than zero")

        with self.uow:
            account = self.uow.accounts.get_by_id(account_id)
            if not account:
                raise AccountNotFound(f"Account {account_id} not found")

            if account.balance < amount:
                raise InsufficientFunds(f"Insufficient funds for PSE payment")

            import uuid
            transaction_id = str(uuid.uuid4())
            transaction = PSETransaction(
                id=transaction_id,
                account_id=account_id,
                amount=amount,
                status=PSEStatus.PENDING
            )
            self.uow.pse_transactions.save(transaction)
            return transaction_id

    def process_webhook(self, transaction_id: str, status: str) -> None:
        """
        Processes the callback from the PSE simulator.
        Follows FEATURE_SPEC_003 (AC-03, AC-04).
        """
        with self.uow:
            transaction = self.uow.pse_transactions.get_by_transaction_id(transaction_id)
            if not transaction:
                raise PSETransactionNotFound(f"PSE Transaction {transaction_id} not found")

            if transaction.status != PSEStatus.PENDING:
                return

            if status == "APPROVED":
                account = self.uow.accounts.get_by_id(transaction.account_id)
                if not account:
                    raise AccountNotFound("Account for PSE transaction no longer exists")
                
                if account.balance < transaction.amount:
                    raise InsufficientFunds("Insufficient funds at consolidation time")
                
                account.balance -= transaction.amount
                movement = Movement(
                    id=None,
                    account_id=account.id,
                    type=MovementType.DEBIT,
                    amount=transaction.amount
                )
                transaction.status = PSEStatus.APPROVED
                self.uow.accounts.save(account)
                self.uow.movements.save(movement)
            else:
                transaction.status = PSEStatus.REJECTED

            self.uow.pse_transactions.save(transaction)
