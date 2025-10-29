from fastapi import APIRouter, HTTPException
from notes_service.api.models import CreateNoteRequest, NoteResponse
from notes_service.service.notes_service import NotesService
from notes_service.db.repository import NoteRepository


router = APIRouter(prefix="/notes", tags=["notes"])

repository = NoteRepository()
service = NotesService(repository)


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(request: CreateNoteRequest):
    # observability: можно добавить tracing для отслеживания запросов
    # with tracer.start_span("create_note"):
    note = service.create_note(request.title, request.content)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: str):
    # observability: метрика времени выполнения запроса
    # with metrics.timer("get_note_duration"):
    note = service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at
    )


@router.get("", response_model=list[NoteResponse])
def get_all_notes():
    notes = service.get_all_notes()
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            created_at=note.created_at
        )
        for note in notes
    ]
