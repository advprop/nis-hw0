from datetime import datetime

from hypothesis import given, settings
from hypothesis import strategies as st

from notes_service.domain.note import Note


class TestNote:
    def test_note_creation(self):
        now = datetime.now()
        note = Note(id="123", title="test", content="content", created_at=now)

        assert note.id == "123"
        assert note.title == "test"
        assert note.content == "content"
        assert note.created_at == now

    def test_note_equality(self):
        now = datetime.now()
        note1 = Note(id="123", title="test", content="content", created_at=now)
        note2 = Note(id="123", title="test", content="content", created_at=now)

        assert note1 == note2

    @given(
        id=st.text(min_size=1, max_size=36),
        title=st.text(min_size=1, max_size=100),
        content=st.text(max_size=500),
    )
    @settings(max_examples=20)
    def test_note_with_hypothesis(self, id, title, content):
        now = datetime.now()
        note = Note(id=id, title=title, content=content, created_at=now)

        assert note.id == id
        assert note.title == title
        assert note.content == content
