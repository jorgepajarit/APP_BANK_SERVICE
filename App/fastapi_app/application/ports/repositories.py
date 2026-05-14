from typing import Protocol, Optional, List, Any
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account, Wallet, Movement

class UserRepository(Protocol):
    def get_by_username(self, username: str) -> Optional[User]:
        ...
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...
        
    def save(self, user: User) -> None:
        ...

class AccountsRepository(Protocol):
    def get_by_id(self, account_id: int) -> Optional[Account]:
        ...
        
    def save(self, account: Account) -> None:
        ...

class WalletRepository(Protocol):
    def get_by_user_id(self, user_id: int) -> List[Wallet]:
        ...

class MovementRepository(Protocol):
    def save(self, movement: Movement) -> None:
        ...
        
    def get_by_account_id(self, account_id: int) -> List[Movement]:
        ...

class PSETransactionRepository(Protocol):
    def get_by_transaction_id(self, transaction_id: str) -> Optional[Any]:
        ...
        
    def save(self, transaction: Any) -> None:
        ...
