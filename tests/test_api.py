import allure
from hypothesis import given, settings
from hypothesis import strategies as st


@allure.feature("Health Check")
class TestHealthCheck:
    @allure.story("Health endpoint returns ok")
    def test_health_check(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@allure.feature("Notes API")
class TestNotesCreate:
    @allure.story("Create note with title and content")
    def test_create_note(self, client):
        response = client.post(
            "/notes", json={"title": "test note", "content": "test content"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "test note"
        assert data["content"] == "test content"
        assert "id" in data
        assert "created_at" in data

    @allure.story("Create note without content")
    def test_create_note_without_content(self, client):
        response = client.post("/notes", json={"title": "only title"})

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "only title"
        assert data["content"] == ""

    @allure.story("Create note with polyfactory")
    def test_create_note_with_factory(self, client, create_note_factory):
        request = create_note_factory.build()

        response = client.post(
            "/notes", json={"title": request.title, "content": request.content}
        )

        assert response.status_code == 201
        assert response.json()["title"] == request.title

    @given(title=st.text(min_size=1, max_size=50))
    @settings(max_examples=10)
    def test_create_note_hypothesis(self, title):
        from fastapi.testclient import TestClient

        from notes_service.api.router import repository
        from notes_service.main import app

        repository.clear()
        client = TestClient(app)

        response = client.post("/notes", json={"title": title, "content": "test"})

        assert response.status_code == 201
        assert response.json()["title"] == title


@allure.feature("Notes API")
class TestNotesRead:
    @allure.story("Get existing note")
    def test_get_note(self, client):
        create_response = client.post(
            "/notes", json={"title": "get test", "content": "content"}
        )
        note_id = create_response.json()["id"]

        response = client.get(f"/notes/{note_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "get test"

    @allure.story("Get non-existent note returns 404")
    def test_get_note_not_found(self, client):
        response = client.get("/notes/non-existent-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "note not found"

    @allure.story("Get all notes")
    def test_get_all_notes(self, client):
        client.post("/notes", json={"title": "note 1", "content": "c1"})
        client.post("/notes", json={"title": "note 2", "content": "c2"})

        response = client.get("/notes")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @allure.story("Get all notes empty")
    def test_get_all_notes_empty(self, client):
        response = client.get("/notes")

        assert response.status_code == 200
        assert response.json() == []


@allure.feature("Notes API")
class TestNotesUpdate:
    @allure.story("Update existing note")
    def test_update_note(self, client):
        create_response = client.post(
            "/notes", json={"title": "old", "content": "old content"}
        )
        note_id = create_response.json()["id"]

        response = client.put(
            f"/notes/{note_id}", json={"title": "new", "content": "new content"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "new"
        assert data["content"] == "new content"

    @allure.story("Update non-existent note returns 404")
    def test_update_note_not_found(self, client):
        response = client.put(
            "/notes/nonexistent", json={"title": "new", "content": "content"}
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "note not found"

    @allure.story("Update note with factory")
    def test_update_note_with_factory(self, client, update_note_factory):
        create_response = client.post("/notes", json={"title": "old", "content": "old"})
        note_id = create_response.json()["id"]
        request = update_note_factory.build()

        response = client.put(
            f"/notes/{note_id}",
            json={"title": request.title, "content": request.content},
        )

        assert response.status_code == 200
        assert response.json()["title"] == request.title


@allure.feature("Notes API")
class TestNotesDelete:
    @allure.story("Delete existing note")
    def test_delete_note(self, client):
        create_response = client.post(
            "/notes", json={"title": "to delete", "content": "content"}
        )
        note_id = create_response.json()["id"]

        response = client.delete(f"/notes/{note_id}")

        assert response.status_code == 204

        get_response = client.get(f"/notes/{note_id}")
        assert get_response.status_code == 404

    @allure.story("Delete non-existent note returns 404")
    def test_delete_note_not_found(self, client):
        response = client.delete("/notes/nonexistent")

        assert response.status_code == 404
        assert response.json()["detail"] == "note not found"
