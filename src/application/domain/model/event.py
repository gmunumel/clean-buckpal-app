from dataclasses import dataclass
from datetime import datetime


class Event:
    created_at: datetime


@dataclass(frozen=True)
class UserRegisteredEvent(Event):
    """
    UserRegisteredEvent class representing an event that occurs when a user is registered.
    This event is used to notify other components of the system about the registration of
    a new user.
    """

    user_id: int

    def __repr__(self) -> str:
        return f"UserRegisteredEvent(user_id={self.user_id!r})"
