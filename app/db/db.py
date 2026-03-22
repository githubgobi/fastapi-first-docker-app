# Simple in-memory database
_db: dict[int, dict] = {}
_counter = 1

from db.database import get_db