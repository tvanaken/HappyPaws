import pytest
from app.tests.db.conftest import create_fake_tasks as tasks  # noqa: F811, F401
from app.tests.db.conftest import get_client as client  # noqa: F811, F401


@pytest.mark.asyncio
async def test_get_tasks(client, tasks):  # noqa: F811
    response = await client.get("/api/tasks")
    assert response.status_code == 200
    resp_data = response.json()
    assert len(resp_data) == 2
    # verify that the correct two tasks are in the list
    assert resp_data[0].get("id") == tasks[0].id
    assert resp_data[1].get("id") == tasks[1].id

    # verify that task 1 has the correct keys and values:
    assert resp_data[0].get("name") == tasks[0].name
    assert resp_data[0].get("description") == tasks[0].description
    assert resp_data[0].get("done") == tasks[0].done


@pytest.mark.asyncio
async def test_get_tasks_detail(client, tasks):  # noqa: F811
    task = tasks[0]
    url = f"/api/tasks/{task.id}"
    response = await client.get(url)
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data.get("id") == task.id
    assert resp_data.get("name") == task.name
    assert resp_data.get("description") == task.description
    assert resp_data.get("done") == task.done


@pytest.mark.asyncio
async def test_get_task_unauthorized_404(client, tasks):  # noqa: F811
    task = tasks[2]
    response = await client.get(f"/api/tasks/{task.id}")
    resp_data = response.json()
    assert response.status_code == 404
    assert resp_data.get("message") == "Not found."


@pytest.mark.asyncio
async def test_post_task(client, tasks):  # noqa: F811
    task = {"name": "Dummy Task", "description": "Dummy Description"}
    response = await client.post("/api/tasks", json=task)
    resp_data = response.json()
    print(resp_data)
    assert response.status_code == 201
    assert resp_data.get("name") == "Dummy Task"
    assert resp_data.get("description") == "Dummy Description"
    assert resp_data.get("done") is False
    assert resp_data.get("user_id") == 1


@pytest.mark.asyncio
async def test_post_task_missing_name(client):  # noqa: F811
    task = {"description": "Dummy Description"}
    response = await client.post("/api/tasks", json=task)
    resp_data = response.json()
    assert response.status_code == 400
    assert resp_data.get("detail") == "Name cannot be empty"


@pytest.mark.asyncio
async def test_post_task_missing_description(client):  # noqa: F811
    task = {"name": "Dummy Name"}
    response = await client.post("/api/tasks", json=task)
    resp_data = response.json()
    assert response.status_code == 400
    assert resp_data.get("detail") == "Description cannot be empty"


@pytest.mark.asyncio
async def test_delete_task(client, tasks):  # noqa: F811
    task = tasks[0]
    url = f"/api/tasks/{task.id}"
    response = await client.delete(url)
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data.get("message") == "task deleted"


@pytest.mark.asyncio
async def test_delete_task_unauthorized_404(client, tasks):  # noqa: F811
    task = tasks[3]
    response = await client.delete(f"/api/tasks/{task.id}")
    resp_data = response.json()
    assert response.status_code == 404
    assert resp_data.get("message") == "Not found."


@pytest.mark.asyncio
async def test_patch_task_some_props(client, tasks):  # noqa: F811
    task = tasks[0]
    url = f"/api/tasks/{task.id}"
    response = await client.patch(url, json={"name": "New Name"})
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data.get("name") == "New Name"
    assert resp_data.get("description") == task.description
    assert resp_data.get("done") == task.done


@pytest.mark.asyncio
async def test_patch_task_all_props(client, tasks):  # noqa: F811
    task = tasks[0]
    url = f"/api/tasks/{task.id}"
    response = await client.patch(
        url, json={"name": "New Name", "description": "New Description", "done": True}
    )
    resp_data = response.json()
    assert response.status_code == 200
    assert resp_data.get("name") == "New Name"
    assert resp_data.get("description") == "New Description"
    assert resp_data.get("done") is True


@pytest.mark.asyncio
async def test_patch_task_unauthorized_404(client, tasks):  # noqa: F811
    task = tasks[2]
    response = await client.patch(f"/api/tasks/{task.id}", json={})
    resp_data = response.json()
    assert response.status_code == 404
    assert resp_data.get("message") == "Not found."
