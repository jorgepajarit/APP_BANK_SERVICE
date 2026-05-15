# domain/auth/entities.py -- BankService
# Pure domain entity. NO external framework imports allowed.
# Reference: context/DOMAIN.md (Sec. 1 - Lenguaje ubicuo, Sec. 2 - Aggregate Roots)

from dataclasses import dataclass


@dataclass
class User:
    """Represents a registered and authenticated customer in the banking system.

    Aggregate Root for the authentication bounded context.
    The hashed_password field must always contain a cryptographic hash,
    never a plain-text password. Hashing is delegated to the PasswordHasher
    port (infrastructure adapter - CAM-11).
    """

    id: int
    username: str
    hashed_password: str
