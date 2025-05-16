import pytest


@pytest.mark.asyncio
async def test_list_user(client, auth_header):
    response = await client.get("/users", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_user_not_found(client, auth_header):
    response = await client.get("/users?user_id=42", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}
