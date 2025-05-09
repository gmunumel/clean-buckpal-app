import pytest


@pytest.mark.asyncio
async def test_list_activity(client):
    response = await client.get("/activity")
    assert response.status_code == 200
    assert response.json() == []
