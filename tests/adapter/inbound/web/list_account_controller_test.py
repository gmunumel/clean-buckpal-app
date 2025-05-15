import pytest


@pytest.mark.asyncio
async def test_list_account(client):
    response = await client.get("/accounts")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_account_not_found(client):
    response = await client.get("/accounts?account_id=42")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found."}


@pytest.mark.asyncio
async def test_list_acccount_resource_not_found(client):
    response = await client.get("/foo")
    assert response.status_code == 404
