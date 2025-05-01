from datetime import datetime, timedelta

from src.application.port.inbound.deposit_money_use_case import DepositMoneyUseCase
from src.application.port.inbound.deposit_money_command import DepositMoneyCommand
from src.application.port.outbound.load_account_port import LoadAccountPort
from src.application.port.outbound.account_lock import AccountLock
from src.application.domain.model.account import Account

DAYS_BEFORE = 10


class DepositMoneyService(DepositMoneyUseCase):
    def __init__(self, load_account_port: LoadAccountPort, account_lock: AccountLock):
        self._load_account_port = load_account_port
        self._account_lock = account_lock

    def deposit_money(self, deposit_money_command: DepositMoneyCommand) -> bool:
        baseline_date = datetime.now() - timedelta(days=DAYS_BEFORE)

        account = self._load_account(deposit_money_command, baseline_date)

        self._validate_account_id(account)

        try:
            self._lock_account(account)
            account.deposit(deposit_money_command.get_money(), account.get_id())
            return True
        finally:
            self._release_account(account)

    def _validate_account_id(self, account: Account):
        if not account or account.get_id():
            raise ValueError("Invalid account ID")

    def _load_account(
        self, deposit_money_command: DepositMoneyCommand, baseline_date: datetime
    ) -> Account:
        account = self._load_account_port.load_account(
            deposit_money_command.get_account_id(), baseline_date
        )
        return account

    def _lock_account(self, account: Account):
        self._account_lock.lock_account(account.get_id())

    def _release_account(self, account: Account):
        self._account_lock.release_account(account.get_id())
