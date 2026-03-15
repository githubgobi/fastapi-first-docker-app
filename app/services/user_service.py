from fastapi import  HTTPException

from db.db import _db
from db.db import _counter
from core import logger
from exceptions.user_exceptions import UserNotFoundException

class UserService:

    @staticmethod
    def create_user(user_data: dict):

        global _counter
        for u in _db.values():
            if u["email"] == user_data["email"]:
                logger.info(f"Email already registered: {user_data['email']}")
                raise HTTPException(status_code=400, detail="Email already registered")
        user_id = _counter
        _db[user_id] = {
            "id": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "salary": user_data["salary"],
            "age": user_data["age"]
        }

        _counter += 1
        return _db[user_id]

    @staticmethod
    def get_user(user_id: int):
        user = _db.get(user_id)
        if not user:
            logger.info(f"User with ID {user_id} not found")
            raise UserNotFoundException(user_id)
        logger.info(
            "Fetching user",
            extra={"user_id": user_id}
        )
        return user

    @staticmethod
    def get_all_users():

        return list(_db.values())