from datetime import datetime
from dataclasses import dataclass


@dataclass
class Note:
    id: str
    title: str
    content: str
    created_at: datetime
