from xml.dom import ValidationErr

from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.user_exceptions import UserNotFoundException

async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "USER_NOT_FOUND",
            "message": f"User {exc.user_id} not found"
        }
    )
async def validation_exception_handler(request: Request, exc: ValidationErr):
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "details": exc.errors()
        }
    )