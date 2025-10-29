from notes_service.domain.note import Note
from notes_service.db.repository import NoteRepository


class NotesService:
    def __init__(self, repository):
        self.repository = repository

    def create_note(self, title, content):
        # observability: можно добавить логирование создания заметки
        # logger.info(f"creating note with title: {title}")
        # observability: метрика количества созданных заметок
        # metrics.counter("notes_created").inc()
        note_data = self.repository.create(title, content)
        return Note(
            id=note_data['id'],
            title=note_data['title'],
            content=note_data['content'],
            created_at=note_data['created_at']
        )

    def get_note(self, note_id):
        note_data = self.repository.get_by_id(note_id)
        if not note_data:
            return None
        return Note(
            id=note_data['id'],
            title=note_data['title'],
            content=note_data['content'],
            created_at=note_data['created_at']
        )

    def get_all_notes(self):
        notes_data = self.repository.get_all()
        return [
            Note(
                id=n['id'],
                title=n['title'],
                content=n['content'],
                created_at=n['created_at']
            )
            for n in notes_data
        ]
