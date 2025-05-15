import pytest


@pytest.mark.asyncio
async def test_list_user(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_user_not_found(client):
    response = await client.get("/users?user_id=42")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
