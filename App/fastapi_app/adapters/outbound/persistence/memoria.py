from typing import List, Optional, Dict
from App.fastapi_app.application.ports.repositories import (
    UserRepository, AccountsRepository, MovementRepository, WalletRepository, PSETransactionRepository
)
from App.fastapi_app.application.ports.uow import UnitOfWork
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account, Movement, Wallet, PSETransaction

class InMemoryUserRepository(UserRepository):
    def __init__(self, users: Dict[int, User]):
        self.users = users

    def get_by_username(self, username: str) -> Optional[User]:
        return next((u for u in self.users.values() if u.username == username), None)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def save(self, user: User) -> None:
        self.users[user.id] = user

class InMemoryAccountsRepository(AccountsRepository):
    def __init__(self, accounts: Dict[int, Account]):
        self.accounts = accounts

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.accounts.get(account_id)

    def get_by_user_id(self, user_id: int) -> List[Account]:
        return [a for a in self.accounts.values() if a.user_id == user_id]

    def save(self, account: Account) -> None:
        self.accounts[account.id] = account

class InMemoryMovementRepository(MovementRepository):
    def __init__(self, movements: List[Movement]):
        self.movements = movements

    def save(self, movement: Movement) -> None:
        if movement.id is None:
            movement.id = len(self.movements) + 1
        self.movements.append(movement)

    def get_by_account_id(self, account_id: int) -> List[Movement]:
        return [m for m in self.movements if m.account_id == account_id]

class InMemoryWalletRepository(WalletRepository):
    def __init__(self, wallets: Dict[int, Wallet]):
        self.wallets = wallets

    def get_by_user_id(self, user_id: int) -> List[Wallet]:
        return [w for w in self.wallets.values() if w.user_id == user_id]

class InMemoryPSETransactionRepository(PSETransactionRepository):
    def __init__(self, transactions: Dict[str, PSETransaction]):
        self.transactions = transactions

    def get_by_transaction_id(self, transaction_id: str) -> Optional[PSETransaction]:
        return self.transactions.get(transaction_id)

    def save(self, transaction: PSETransaction) -> None:
        self.transactions[transaction.id] = transaction

class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        # We use internal dictionaries to simulate the persistent state
        self.users_data = {}
        self.accounts_data = {}
        self.movements_data = []
        self.wallets_data = {}
        self.pse_data = {}
        
        self.users = InMemoryUserRepository(self.users_data)
        self.accounts = InMemoryAccountsRepository(self.accounts_data)
        self.movements = InMemoryMovementRepository(self.movements_data)
        self.wallets = InMemoryWalletRepository(self.wallets_data)
        self.pse_transactions = InMemoryPSETransactionRepository(self.pse_data)
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        # In memory implementation for tests usually doesn't need complex rollback
        # unless specifically testing transaction failures.
        pass
