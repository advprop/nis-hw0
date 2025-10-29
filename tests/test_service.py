import pytest
from notes_service.service.notes_service import NotesService
from notes_service.db.repository import NoteRepository


def test_create_note():
    repo = NoteRepository()
    service = NotesService(repo)

    note = service.create_note("test title", "test content")

    assert note.title == "test title"
    assert note.content == "test content"
    assert note.id is not None


def test_get_note():
    repo = NoteRepository()
    service = NotesService(repo)

    created_note = service.create_note("test", "content")
    fetched_note = service.get_note(created_note.id)

    assert fetched_note is not None
    assert fetched_note.id == created_note.id
    assert fetched_note.title == "test"


def test_get_note_not_found():
    repo = NoteRepository()
    service = NotesService(repo)

    note = service.get_note("non-existent-id")

    assert note is None


def test_get_all_notes():
    repo = NoteRepository()
    service = NotesService(repo)

    service.create_note("note 1", "content 1")
    service.create_note("note 2", "content 2")

    notes = service.get_all_notes()

    assert len(notes) == 2
    assert any(n.title == "note 1" for n in notes)
    assert any(n.title == "note 2" for n in notes)


def test_get_all_notes_empty():
    repo = NoteRepository()
    service = NotesService(repo)

    notes = service.get_all_notes()

    assert len(notes) == 0
