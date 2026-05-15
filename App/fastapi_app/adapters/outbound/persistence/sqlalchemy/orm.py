from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, MetaData
from sqlalchemy.orm import registry
from App.fastapi_app.domain.auth.entities import User
from App.fastapi_app.domain.banking.entities import Account, Movement, Wallet, PSETransaction, MovementType, PSEStatus

metadata = MetaData()
mapper_registry = registry()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("password_hash", String(255), nullable=False),
)

accounts = Table(
    "accounts", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("balance", Float, default=0.0),
)

wallets = Table(
    "wallets", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("balance", Float, default=0.0),
)

movements = Table(
    "movements", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("account_id", Integer, ForeignKey("accounts.id"), nullable=False),
    Column("type", SQLEnum(MovementType), nullable=False),
    Column("amount", Float, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

pse_transactions = Table(
    "pse_transactions", metadata,
    Column("id", String(50), primary_key=True),
    Column("account_id", Integer, ForeignKey("accounts.id"), nullable=False),
    Column("amount", Float, nullable=False),
    Column("status", SQLEnum(PSEStatus), nullable=False),
    Column("created_at", DateTime, nullable=False),
)

def start_mappers():
    """
    Configura el mapeo imperativo de SQLAlchemy para mantener las entidades de dominio puras.
    """
    # Verificación para evitar mapear dos veces en entornos de hot-reload
    if User in mapper_registry.mappers:
        return
        
    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(Account, accounts)
    mapper_registry.map_imperatively(Wallet, wallets)
    mapper_registry.map_imperatively(Movement, movements)
    mapper_registry.map_imperatively(PSETransaction, pse_transactions)
