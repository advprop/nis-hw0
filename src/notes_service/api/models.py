from pydantic import BaseModel
from datetime import datetime


class CreateNoteRequest(BaseModel):
    title: str
    content: str = ""


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
