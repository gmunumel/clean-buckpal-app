from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.money import Money
from src.application.domain.model.activity_window import ActivityWindow
from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status


class PersistenceMapper:
    @staticmethod
    def map_to_domain_entity(
        account: Account,
        activities: list[Activity],
        withdrawal_balance: float,
        deposit_balance: float,
    ) -> Account:
        baseline_balance = account.baseline_balance
        balance = Money.subtract(
            Money.of(deposit_balance), Money.of(withdrawal_balance)
        )
        return PersistenceMapper.map_to_account_entity(
            account.id, Money.add(baseline_balance, balance), activities
        )

    @staticmethod
    def map_to_account_entity(
        account_id: AccountId, money: Money, activities: list[Activity]
    ) -> Account:
        return Account.with_id(
            account_id=account_id,
            baseline_balance=money,
            activity_window=PersistenceMapper.map_to_activity_window(activities),
        )

    @staticmethod
    def map_to_activity_window(activities: list[Activity]) -> ActivityWindow:
        mapped_activities = []
        for activity in activities:
            mapped_activities.append(
                Activity(
                    id=activity.id,
                    owner_account_id=activity.owner_account_id,
                    source_account_id=activity.source_account_id,
                    target_account_id=activity.target_account_id,
                    timestamp=activity.timestamp,
                    money=activity.money,
                )
            )
        return ActivityWindow(mapped_activities)

    @staticmethod
    def map_to_user_entity(
        user_id: UserId, user_name: Name, address: Address, status: Status
    ) -> User:
        return User(id=user_id, name=user_name, address=address, status=status)
