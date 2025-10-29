from fastapi.testclient import TestClient
from notes_service.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note():
    response = client.post(
        "/notes",
        json={"title": "test note", "content": "test content"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test note"
    assert data["content"] == "test content"
    assert "id" in data
    assert "created_at" in data


def test_create_note_without_content():
    response = client.post(
        "/notes",
        json={"title": "only title"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "only title"
    assert data["content"] == ""


def test_get_note():
    create_response = client.post(
        "/notes",
        json={"title": "get test", "content": "content"}
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "get test"


def test_get_note_not_found():
    response = client.get("/notes/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "note not found"


def test_get_all_notes():
    client.post("/notes", json={"title": "note 1", "content": "c1"})
    client.post("/notes", json={"title": "note 2", "content": "c2"})

    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
