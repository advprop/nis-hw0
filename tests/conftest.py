import pytest
from fastapi.testclient import TestClient
from polyfactory.factories.pydantic_factory import ModelFactory

from notes_service.api.models import CreateNoteRequest, UpdateNoteRequest
from notes_service.api.router import repository
from notes_service.db.repository import NoteRepository
from notes_service.main import app
from notes_service.service.notes_service import NotesService


class CreateNoteRequestFactory(ModelFactory):  # type: ignore[misc]
    __model__ = CreateNoteRequest


class UpdateNoteRequestFactory(ModelFactory):  # type: ignore[misc]
    __model__ = UpdateNoteRequest


@pytest.fixture
def client():
    repository.clear()
    return TestClient(app)


@pytest.fixture
def note_repository():
    return NoteRepository()


@pytest.fixture
def notes_service(note_repository):
    return NotesService(note_repository)


@pytest.fixture
def create_note_factory():
    return CreateNoteRequestFactory


@pytest.fixture
def update_note_factory():
    return UpdateNoteRequestFactory
