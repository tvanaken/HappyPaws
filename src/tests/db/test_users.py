import pytest
from app.tests.db.conftest import get_client as client  # noqa: F811, F401


@pytest.mark.asyncio
async def test_get_user(client):  # noqa: F811
    response = await client.get("/api/user")
    resp_data = response.json()
    print(resp_data)
    assert response.status_code == 200
    assert resp_data.get("username") == "logged_in_user"
    assert resp_data.get("first_name") == "Jane"
    assert resp_data.get("last_name") == "Doe"
    assert resp_data.get("email") == "jane_doe@yahoo.com"
