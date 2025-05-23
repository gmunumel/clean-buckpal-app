import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from src.app import app
from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.adapter.inbound.web.jwt_utils import create_jwt_token
from src.common.config import DUMMY_USER


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def given_account_with_id(mocker):
    def _create_mocked_account(account_id: AccountId):
        mocked_account = mocker.Mock(spec=Account)
        mocked_account.id = account_id
        return mocked_account

    return _create_mocked_account


@pytest.fixture
def given_activity_with_id(mocker):
    def _create_mocked_activity(activity_id: ActivityId):
        mocked_activity = mocker.Mock(spec=Activity)
        mocked_activity.id = activity_id
        return mocked_activity

    return _create_mocked_activity


@pytest.fixture
def given_user_with_id(mocker):
    def _create_mocked_user(user_id: UserId):
        mocked_user = mocker.Mock(spec=User)
        mocked_user.id = user_id
        return mocked_user

    return _create_mocked_user


@pytest.fixture
def auth_header():
    token = create_jwt_token(DUMMY_USER)
    return {"Authorization": f"Bearer {token}"}
