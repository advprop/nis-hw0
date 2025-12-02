from hypothesis import given, settings
from hypothesis import strategies as st

from notes_service.db.repository import NoteRepository
from notes_service.service.notes_service import NotesService


class TestNotesService:
    def test_create_note(self, notes_service):
        note = notes_service.create_note("test title", "test content")

        assert note.title == "test title"
        assert note.content == "test content"
        assert note.id is not None
        assert note.created_at is not None

    def test_get_note_existing(self, notes_service):
        created = notes_service.create_note("test", "content")

        result = notes_service.get_note(created.id)

        assert result is not None
        assert result.id == created.id
        assert result.title == "test"

    def test_get_note_not_found(self, notes_service):
        result = notes_service.get_note("non-existent-id")

        assert result is None

    def test_get_all_notes_empty(self, notes_service):
        notes = notes_service.get_all_notes()

        assert len(notes) == 0

    def test_get_all_notes_with_data(self, notes_service):
        notes_service.create_note("note 1", "content 1")
        notes_service.create_note("note 2", "content 2")

        notes = notes_service.get_all_notes()

        assert len(notes) == 2
        assert any(n.title == "note 1" for n in notes)
        assert any(n.title == "note 2" for n in notes)

    def test_delete_note_existing(self, notes_service):
        created = notes_service.create_note("test", "content")

        result = notes_service.delete_note(created.id)

        assert result is True
        assert notes_service.get_note(created.id) is None

    def test_delete_note_not_found(self, notes_service):
        result = notes_service.delete_note("nonexistent")

        assert result is False

    def test_update_note_existing(self, notes_service):
        created = notes_service.create_note("old", "old content")

        result = notes_service.update_note(created.id, "new", "new content")

        assert result is not None
        assert result.title == "new"
        assert result.content == "new content"

    def test_update_note_not_found(self, notes_service):
        result = notes_service.update_note("nonexistent", "new", "content")

        assert result is None

    @given(title=st.text(min_size=1, max_size=100), content=st.text(max_size=500))
    @settings(max_examples=20)
    def test_create_note_with_hypothesis(self, title, content):
        repo = NoteRepository()
        service = NotesService(repo)

        note = service.create_note(title, content)

        assert note.title == title
        assert note.content == content

    def test_to_note_helper(self, notes_service, note_repository):
        note_data = note_repository.create("test", "content")

        note = notes_service._to_note(note_data)

        assert note.id == note_data["id"]
        assert note.title == note_data["title"]
        assert note.content == note_data["content"]
        assert note.created_at == note_data["created_at"]
