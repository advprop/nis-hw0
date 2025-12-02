from fastapi import APIRouter, HTTPException

from notes_service.api.models import CreateNoteRequest, NoteResponse, UpdateNoteRequest
from notes_service.db.repository import NoteRepository
from notes_service.service.notes_service import NotesService


router = APIRouter(prefix="/notes", tags=["notes"])

repository = NoteRepository()
service = NotesService(repository)


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(request: CreateNoteRequest) -> NoteResponse:
    note = service.create_note(request.title, request.content)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: str) -> NoteResponse:
    note = service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
    )


@router.get("", response_model=list[NoteResponse])
def get_all_notes() -> list[NoteResponse]:
    notes = service.get_all_notes()
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            created_at=note.created_at,
        )
        for note in notes
    ]


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: str, request: UpdateNoteRequest) -> NoteResponse:
    note = service.update_note(note_id, request.title, request.content)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
    )


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: str) -> None:
    deleted = service.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="note not found")
