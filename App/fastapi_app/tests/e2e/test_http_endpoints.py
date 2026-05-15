import pytest
from fastapi.testclient import TestClient
from App.fastapi_app.main import app
from App.fastapi_app.adapters.inbound.http.dependencies import _mock_uow
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account
from App.fastapi_app.adapters.outbound.security.passlib_hasher import PasslibPasswordHasher

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_data():
    # Reset memory UoW data
    _mock_uow.users_data.clear()
    _mock_uow.accounts_data.clear()
    _mock_uow.movements_data.clear()
    _mock_uow.wallets_data.clear()
    _mock_uow.pse_data.clear()

    # Seed data
    hasher = PasslibPasswordHasher()
    user = User(id=1, username="testuser", password_hash=hasher.get_password_hash("password123"))
    _mock_uow.users.save(user)

    account1 = Account(id=1, user_id=1, balance=50000.0)
    account2 = Account(id=2, user_id=1, balance=10000.0)
    _mock_uow.accounts.save(account1)
    _mock_uow.accounts.save(account2)

def test_login_success():
    response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_invalid_credentials():
    response = client.post("/auth/login", json={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401

def test_get_financial_summary():
    response = client.get("/banking/summary/1")
    assert response.status_code == 200
    data = response.json()
    assert data["total_consolidated_balance"] == 60000.0

def test_transfer_success():
    response = client.post("/banking/transfer", json={
        "source_account_id": 1,
        "target_account_id": 2,
        "amount": 10000.0
    })
    assert response.status_code == 200
    # Verify balances updated correctly via UoW
    assert _mock_uow.accounts.get_by_id(1).balance == 40000.0
    assert _mock_uow.accounts.get_by_id(2).balance == 20000.0

def test_transfer_insufficient_funds():
    response = client.post("/banking/transfer", json={
        "source_account_id": 1,
        "target_account_id": 2,
        "amount": 100000.0
    })
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]

def test_pse_payment_flow():
    # Initiate
    response = client.post("/pse/payment", json={"account_id": 1, "amount": 15000.0})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING"
    tx_id = data["transaction_id"]

    # Webhook
    webhook_res = client.post("/pse/webhook", json={"transaction_id": tx_id, "status": "APPROVED"})
    assert webhook_res.status_code == 200

    # Balance check
    assert _mock_uow.accounts.get_by_id(1).balance == 35000.0
