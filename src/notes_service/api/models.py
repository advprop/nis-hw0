from datetime import datetime

from pydantic import BaseModel


class CreateNoteRequest(BaseModel):
    title: str
    content: str = ""


class UpdateNoteRequest(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
