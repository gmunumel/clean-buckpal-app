import pytest


@pytest.mark.asyncio
async def test_list_activity(client, auth_header):
    response = await client.get("/activities", headers=auth_header)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_activity_not_found(client, auth_header):
    response = await client.get("/activities?activity_id=42", headers=auth_header)
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found."}
