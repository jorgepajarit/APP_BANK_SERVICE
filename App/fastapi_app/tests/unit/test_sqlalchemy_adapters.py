import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from App.fastapi_app.adapters.outbound.persistence.sqlalchemy.orm import metadata, start_mappers
from App.fastapi_app.adapters.outbound.persistence.sqlalchemy.uow import SqlAlchemyUnitOfWork
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account

@pytest.fixture
def session_factory():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    start_mappers()
    yield sessionmaker(bind=engine)
    clear_mappers()

def test_uow_can_save_and_retrieve_user(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    
    with uow:
        user = User(id=1, username="jdoe", password_hash="secret")
        uow.users.save(user)
        uow.commit()
        
    with uow:
        retrieved = uow.users.get_by_username("jdoe")
        assert retrieved is not None
        assert retrieved.username == "jdoe"
        assert retrieved.password_hash == "secret"

def test_uow_can_save_and_retrieve_account(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    
    with uow:
        user = User(id=10, username="testuser", password_hash="hash")
        uow.users.save(user)
        
        acc = Account(id=1, user_id=10, balance=1500.0)
        uow.accounts.save(acc)
        uow.commit()
        
    with uow:
        retrieved_acc = uow.accounts.get_by_id(1)
        assert retrieved_acc.balance == 1500.0
        assert retrieved_acc.user_id == 10
