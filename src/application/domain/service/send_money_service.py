from datetime import datetime, timedelta

from src.application.domain.model.account import Account
from src.application.port.outbound.update_account_state_port import (
    UpdateAccountStatePort,
)
from src.application.port.inbound.send_money_use_case import SendMoneyUseCase
from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.port.outbound.load_account_port import LoadAccountPort
from src.application.port.outbound.account_lock import AccountLock
from src.application.domain.service.money_transfer_properties import (
    MoneyTransferProperties,
)
from src.application.domain.service.threshold_exceeded_exception import (
    ThresholdExceededException,
)
from src.application.domain.service.withdraw_exceeded_exception import (
    WithdrawExceededException,
)

DAYS_BEFORE = 10


class SendMoneyService(SendMoneyUseCase):
    """
    Service for sending money between accounts.
    This service is responsible for orchestrating the process of sending money
    between accounts. It uses the LoadAccountPort to load the accounts, the
    AccountLock to lock the accounts during the transaction, and the
    UpdateAccountStatePort to update the state of the accounts after the
    transaction.
    Attributes:
        load_account_port: Port for loading accounts.
        account_lock: Port for locking and unlocking accounts.
        update_account_state_port: Port for updating the state of accounts.
        money_transfer_properties: Properties for money transfer.
    """

    def __init__(
        self,
        load_account_port: LoadAccountPort,
        account_lock: AccountLock,
        update_account_state_port: UpdateAccountStatePort,
        money_transfer_properties: MoneyTransferProperties,
    ):
        self._load_account_port = load_account_port
        self._account_lock = account_lock
        self._update_account_state_port = update_account_state_port
        self._money_transfer_properties = money_transfer_properties

    def send_money(self, send_money_command: SendMoneyCommand) -> bool:
        self._check_threshold(send_money_command)

        baseline_date = datetime.now() - timedelta(days=DAYS_BEFORE)

        source_account, target_account = self._load_accounts(
            send_money_command, baseline_date
        )

        self._validate_account_ids(source_account, target_account)

        try:
            self._lock_account(source_account)
            money = send_money_command.get_money()
            if not source_account.withdraw(money, target_account.get_id()):
                raise WithdrawExceededException(money)

            self._lock_account(target_account)
            target_account.deposit(money, source_account.get_id())

            self._update_account_states(source_account, target_account)
            return True
        finally:
            self._release_accounts(source_account, target_account)

    def _check_threshold(self, send_money_command: SendMoneyCommand):
        money = send_money_command.get_money()
        if money.is_greater_than(
            self._money_transfer_properties.max_transfer_threshold
        ):
            raise ThresholdExceededException(
                self._money_transfer_properties.max_transfer_threshold,
                money,
            )

    def _load_accounts(
        self, send_money_command: SendMoneyCommand, baseline_date: datetime
    ) -> tuple[Account, Account]:
        source_account = self._load_account_port.load_account(
            send_money_command.get_source_account_id(), baseline_date
        )
        target_account = self._load_account_port.load_account(
            send_money_command.get_target_account_id(), baseline_date
        )
        return source_account, target_account

    def _validate_account_ids(self, source_account: Account, target_account: Account):
        if not source_account or source_account.get_id():
            raise ValueError("Expected source account ID not to be empty")
        if not target_account or target_account.get_id():
            raise ValueError("Expected target account ID not to be empty")

    def _lock_account(self, account: Account):
        self._account_lock.lock_account(account.get_id())

    def _release_accounts(self, source_account: Account, target_account: Account):
        self._account_lock.release_account(source_account.get_id())
        self._account_lock.release_account(target_account.get_id())

    def _update_account_states(self, source_account: Account, target_account: Account):
        self._update_account_state_port.update_activities(source_account)
        self._update_account_state_port.update_activities(target_account)
