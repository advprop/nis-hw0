from datetime import datetime
from typing import TypedDict
from uuid import uuid4


class NoteData(TypedDict):
    id: str
    title: str
    content: str
    created_at: datetime


class NoteRepository:
    def __init__(self) -> None:
        self._storage: dict[str, NoteData] = {}

    def create(self, title: str, content: str) -> NoteData:
        note_id = str(uuid4())
        note: NoteData = {
            "id": note_id,
            "title": title,
            "content": content,
            "created_at": datetime.now(),
        }
        self._storage[note_id] = note
        return note

    def get_by_id(self, note_id: str) -> NoteData | None:
        return self._storage.get(note_id)

    def get_all(self) -> list[NoteData]:
        return list(self._storage.values())

    def delete(self, note_id: str) -> bool:
        if note_id in self._storage:
            del self._storage[note_id]
            return True
        return False

    def update(self, note_id: str, title: str, content: str) -> NoteData | None:
        if note_id not in self._storage:
            return None
        self._storage[note_id]["title"] = title
        self._storage[note_id]["content"] = content
        return self._storage[note_id]

    def clear(self) -> None:
        self._storage.clear()
