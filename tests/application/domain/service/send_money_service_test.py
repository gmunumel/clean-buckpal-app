from unittest.mock import call
import pytest

from src.application.domain.model.account import AccountId
from src.application.domain.model.money import Money
from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.service.send_money_service import SendMoneyService
from src.application.domain.service.money_transfer_properties import (
    MoneyTransferProperties,
)
from src.application.domain.service.withdraw_exceeded_exception import (
    WithdrawExceededException,
)


@pytest.fixture
def money_transfer_properties():
    return MoneyTransferProperties(Money.of(float("inf")).amount)


@pytest.fixture
def send_money_service(mocker, money_transfer_properties):
    load_account_port = mocker.Mock()
    account_lock = mocker.Mock()
    update_account_state_port = mocker.Mock()

    service = SendMoneyService(
        load_account_port=load_account_port,
        account_lock=account_lock,
        update_account_state_port=update_account_state_port,
        money_transfer_properties=money_transfer_properties,
    )
    return service, load_account_port, account_lock, update_account_state_port


def test_send_money_service_given_withdrawal_fails_then_only_source_account_is_locked_and_released(
    send_money_service, given_account_with_id
):
    service, load_account_port, account_lock, _ = send_money_service

    source_account_id = AccountId(41)
    source_account = given_account_with_id(source_account_id)

    target_account_id = AccountId(42)
    target_account = given_account_with_id(target_account_id)

    source_account.withdraw.return_value = False
    target_account.deposit.return_value = True

    load_account_port.load_account.side_effect = [source_account, target_account]

    command = SendMoneyCommand(
        source_account_id=source_account_id,
        target_account_id=target_account_id,
        money=Money.of(300),
    )

    with pytest.raises(
        WithdrawExceededException,
        match=r"Not enough money to withdraw\. Tried to transfer \$300\.00\!",
    ):
        service.send_money(command)

    account_lock.lock_account.assert_has_calls([call(source_account_id)])
    account_lock.release_account.assert_has_calls(
        [call(source_account_id), call(target_account_id)]
    )


def test_send_money_service_transaction_succeeds(
    send_money_service, given_account_with_id
):
    service, load_account_port, account_lock, update_account_state_port = (
        send_money_service
    )

    source_account_id = AccountId(41)
    source_account = given_account_with_id(source_account_id)

    target_account_id = AccountId(42)
    target_account = given_account_with_id(target_account_id)

    source_account.withdraw.return_value = True
    target_account.deposit.return_value = True

    load_account_port.load_account.side_effect = [source_account, target_account]

    money = Money.of(500)
    command = SendMoneyCommand(
        source_account_id=source_account_id,
        target_account_id=target_account_id,
        money=money,
    )

    success = service.send_money(command)

    assert success

    account_lock.lock_account.assert_has_calls(
        [call(source_account_id), call(target_account_id)]
    )
    account_lock.release_account.assert_has_calls(
        [call(source_account_id), call(target_account_id)]
    )

    source_account.withdraw.assert_called_once_with(money, target_account_id)
    target_account.deposit.assert_called_once_with(money, source_account_id)

    update_account_state_port.update_accounts.assert_has_calls(
        [call([source_account, target_account])]
    )
    update_account_state_port.update_activities.assert_has_calls(
        [call([source_account, target_account])]
    )
