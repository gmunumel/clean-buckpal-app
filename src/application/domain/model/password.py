from dataclasses import dataclass
from typing import Optional
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class Password:
    """
    Password value object for handling password hashing and verification.
    Only one of plain or hashed should be set at a time.
    """

    plain: Optional[str] = None
    hashed: Optional[str] = None

    def __post_init__(self):
        if not self.plain and not self.hashed:
            raise ValueError("Either plain or hashed password must be provided.")
        if self.plain and self.hashed:
            raise ValueError("Only one of plain or hashed should be set.")

    def hash(self) -> "Password":
        if not self.plain:
            raise ValueError("No plain password to hash.")
        hashed = PWD_CONTEXT.hash(self.plain)
        return Password(plain=None, hashed=hashed)

    def verify(self, plain_password: str) -> bool:
        if not self.hashed:
            raise ValueError("No hashed password to verify against.")
        return PWD_CONTEXT.verify(plain_password, self.hashed)

    def __str__(self) -> str:
        if self.plain:
            return self.plain
        if self.hashed:
            return self.hashed
        return ""
