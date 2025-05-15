import pytest


@pytest.mark.asyncio
async def test_list_activity(client):
    response = await client.get("/activities")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_activity_not_found(client):
    response = await client.get("/activities?activity_id=42")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
