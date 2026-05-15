from sqlalchemy.orm import sessionmaker
from App.fastapi_app.application.ports.uow import UnitOfWork
from App.fastapi_app.adapters.outbound.persistence.sqlalchemy.repositories import (
    SqlAlchemyUserRepository, 
    SqlAlchemyAccountsRepository, 
    SqlAlchemyMovementRepository, 
    SqlAlchemyWalletRepository, 
    SqlAlchemyPSETransactionRepository
)

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = SqlAlchemyUserRepository(self.session)
        self.accounts = SqlAlchemyAccountsRepository(self.session)
        self.movements = SqlAlchemyMovementRepository(self.session)
        self.wallets = SqlAlchemyWalletRepository(self.session)
        self.pse_transactions = SqlAlchemyPSETransactionRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
