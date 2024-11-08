import pytest

from fastapi.testclient import TestClient
from datetime import datetime
from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "online"
    assert "timestamp" in data


def test_create_task():
    """Test task creation"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": datetime.now().isoformat(),
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "completed" in data
    assert not data["completed"]


def test_list_tasks():
    """Test listing tasks"""
    # Create a task first
    task_data = {"title": "Test Task"}
    client.post("/tasks/", json=task_data)

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_task():
    """Test getting a specific task"""
    # Create a task first
    task_data = {"title": "Test Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


def test_update_task():
    """Test updating a task"""
    # Create a task first
    task_data = {"title": "Test Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {"title": "Updated Task", "description": "Updated description"}
    response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_delete_task():
    """Test deleting a task"""
    # Create a task first
    task_data = {"title": "Test Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_complete_task():
    """Test marking a task as completed"""
    # Create a task first
    task_data = {"title": "Test Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Complete the task
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"]


def test_complete_nonexistent_task():
    """Test completing a task that doesn't exist"""
    response = client.post("/tasks/nonexistent-id/complete")
    assert response.status_code == 404
