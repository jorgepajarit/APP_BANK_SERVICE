from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TransferRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float

class PSEPaymentRequest(BaseModel):
    account_id: int
    amount: float

class PSEWebhookRequest(BaseModel):
    transaction_id: str
    status: str

class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float

class MovementResponse(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float

class FinancialSummaryResponse(BaseModel):
    user_id: int
    total_consolidated_balance: float
