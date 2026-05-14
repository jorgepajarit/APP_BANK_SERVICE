import abc
from App.fastapi_app.application.ports.repositories import (
    AccountsRepository, 
    MovementRepository, 
    UserRepository, 
    PSETransactionRepository,
    WalletRepository
)

class UnitOfWork(abc.ABC):
    users: UserRepository
    accounts: AccountsRepository
    movements: MovementRepository
    wallets: WalletRepository
    pse_transactions: PSETransactionRepository

    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
