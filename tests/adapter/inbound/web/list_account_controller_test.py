import pytest


@pytest.mark.asyncio
async def test_list_account(client, auth_header):
    response = await client.get("/accounts", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_account_not_found(client, auth_header):
    response = await client.get("/accounts?account_id=42", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found."}


@pytest.mark.asyncio
async def test_list_acccount_resource_not_found(client, auth_header):
    response = await client.get("/foo", headers=auth_header)
    assert response.status_code == 404
