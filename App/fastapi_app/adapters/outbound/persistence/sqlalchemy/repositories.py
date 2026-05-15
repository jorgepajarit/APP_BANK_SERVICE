from typing import List, Optional
from sqlalchemy.orm import Session
from App.fastapi_app.application.ports.repositories import (
    UserRepository, AccountsRepository, MovementRepository, WalletRepository, PSETransactionRepository
)
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account, Movement, Wallet, PSETransaction

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter_by(username=username).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=user_id).first()

    def save(self, user: User) -> None:
        self.session.add(user)

class SqlAlchemyAccountsRepository(AccountsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.session.query(Account).filter_by(id=account_id).first()

    def get_by_user_id(self, user_id: int) -> List[Account]:
        return self.session.query(Account).filter_by(user_id=user_id).all()

    def save(self, account: Account) -> None:
        self.session.add(account)

class SqlAlchemyMovementRepository(MovementRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, movement: Movement) -> None:
        self.session.add(movement)

    def get_by_account_id(self, account_id: int) -> List[Movement]:
        return self.session.query(Movement).filter_by(account_id=account_id).all()

class SqlAlchemyWalletRepository(WalletRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> List[Wallet]:
        return self.session.query(Wallet).filter_by(user_id=user_id).all()

class SqlAlchemyPSETransactionRepository(PSETransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_transaction_id(self, transaction_id: str) -> Optional[PSETransaction]:
        return self.session.query(PSETransaction).filter_by(id=transaction_id).first()

    def save(self, transaction: PSETransaction) -> None:
        self.session.add(transaction)
