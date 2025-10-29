from datetime import datetime
from uuid import uuid4


class NoteRepository:
    def __init__(self):
        self._storage = {}

    def create(self, title, content):
        note_id = str(uuid4())
        note = {
            'id': note_id,
            'title': title,
            'content': content,
            'created_at': datetime.now()
        }
        self._storage[note_id] = note
        return note

    def get_by_id(self, note_id):
        return self._storage.get(note_id)

    def get_all(self):
        return list(self._storage.values())
