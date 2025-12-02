from hypothesis import given, settings
from hypothesis import strategies as st

from notes_service.db.repository import NoteRepository


class TestNoteRepository:
    def test_create_note(self, note_repository):
        result = note_repository.create("test", "content")

        assert result["title"] == "test"
        assert result["content"] == "content"
        assert result["id"] is not None
        assert result["created_at"] is not None

    def test_get_by_id_existing(self, note_repository):
        created = note_repository.create("test", "content")

        result = note_repository.get_by_id(created["id"])

        assert result is not None
        assert result["id"] == created["id"]

    def test_get_by_id_not_found(self, note_repository):
        result = note_repository.get_by_id("nonexistent")

        assert result is None

    def test_get_all_empty(self, note_repository):
        result = note_repository.get_all()

        assert result == []

    def test_get_all_with_notes(self, note_repository):
        note_repository.create("note1", "content1")
        note_repository.create("note2", "content2")

        result = note_repository.get_all()

        assert len(result) == 2

    def test_delete_existing(self, note_repository):
        created = note_repository.create("test", "content")

        result = note_repository.delete(created["id"])

        assert result is True
        assert note_repository.get_by_id(created["id"]) is None

    def test_delete_not_found(self, note_repository):
        result = note_repository.delete("nonexistent")

        assert result is False

    def test_update_existing(self, note_repository):
        created = note_repository.create("old", "old content")

        result = note_repository.update(created["id"], "new", "new content")

        assert result is not None
        assert result["title"] == "new"
        assert result["content"] == "new content"

    def test_update_not_found(self, note_repository):
        result = note_repository.update("nonexistent", "new", "content")

        assert result is None

    def test_clear(self, note_repository):
        note_repository.create("note1", "content1")
        note_repository.create("note2", "content2")

        note_repository.clear()

        assert note_repository.get_all() == []

    @given(title=st.text(min_size=1, max_size=100), content=st.text(max_size=500))
    @settings(max_examples=20)
    def test_create_with_hypothesis(self, title, content):
        repo = NoteRepository()
        result = repo.create(title, content)

        assert result["title"] == title
        assert result["content"] == content
