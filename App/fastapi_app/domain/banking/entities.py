from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

class MovementType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class PSEStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

@dataclass
class Movement:
    id: Optional[int]
    account_id: int
    type: MovementType
    amount: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Account:
    id: int
    user_id: int
    balance: float = 0.0

@dataclass
class Wallet:
    id: int
    user_id: int
    balance: float = 0.0

@dataclass
class PSETransaction:
    id: str
    account_id: int
    amount: float
    status: PSEStatus = PSEStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
