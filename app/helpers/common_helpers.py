from typing import  Optional
from fastapi import HTTPException, Header
from core import logger

# ── Helper (makes it easy to reset state in tests) ────────────────────────────
def _reset_db():
    global _db, _counter
    _db = {}
    _counter = 1

def common_parameters(limit: Optional[int] = None, offset: Optional[int] = None):
    return {"limit": limit or 10, "offset": offset or 0}

class Pagination:
    def __init__(self, limit: Optional[int] = None, offset: Optional[int] = None):
        self.limit = limit or 20
        self.offset = offset or 0

def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        logger.info(f"Invalid token: {x_token}")
        raise HTTPException(status_code=401, detail="Invalid X-Token header")