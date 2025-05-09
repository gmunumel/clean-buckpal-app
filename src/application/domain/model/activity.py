from dataclasses import dataclass
from datetime import datetime

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.money import Money


@dataclass
class Activity:
    """
    Activity class representing a financial activity.
    """

    id: ActivityId
    owner_account_id: AccountId
    source_account_id: AccountId
    target_account_id: AccountId
    timestamp: datetime
    money: Money

    def __repr__(self) -> str:
        return (
            f"Activity(id={self.id!r}, owner_account_id={self.owner_account_id!r}, "
            f"source_account_id={self.source_account_id!r}, "
            f"target_account_id={self.target_account_id!r}, "
            f"timestamp={self.timestamp!r}, money={self.money!r})"
        )
