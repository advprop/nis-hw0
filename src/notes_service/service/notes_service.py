from notes_service.db.repository import NoteData, NoteRepository
from notes_service.domain.note import Note


class NotesService:
    def __init__(self, repository: NoteRepository) -> None:
        self.repository = repository

    def _to_note(self, note_data: NoteData) -> Note:
        return Note(
            id=note_data["id"],
            title=note_data["title"],
            content=note_data["content"],
            created_at=note_data["created_at"],
        )

    def create_note(self, title: str, content: str) -> Note:
        note_data = self.repository.create(title, content)
        return self._to_note(note_data)

    def get_note(self, note_id: str) -> Note | None:
        note_data = self.repository.get_by_id(note_id)
        if not note_data:
            return None
        return self._to_note(note_data)

    def get_all_notes(self) -> list[Note]:
        notes_data = self.repository.get_all()
        return [self._to_note(n) for n in notes_data]

    def delete_note(self, note_id: str) -> bool:
        return self.repository.delete(note_id)

    def update_note(self, note_id: str, title: str, content: str) -> Note | None:
        note_data = self.repository.update(note_id, title, content)
        if not note_data:
            return None
        return self._to_note(note_data)
