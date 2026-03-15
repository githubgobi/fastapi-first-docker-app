import httpx
from typing import Annotated
from helpers.common_helpers import Pagination, common_parameters, verify_token
from fastapi import FastAPI, Depends
# Import custom exception handlers
from core.exception_handlers import user_not_found_handler, validation_exception_handler
from exceptions.user_exceptions import UserNotFoundException
# Import logger
from core.logger import logger
from middleware.logging_middleware import RequestLoggingMiddleware
# CORS Middleware
from middleware.security_middleware import add_cors_middleware

# Routers
from routers.user_router import router as user_router
from routers.file_router import router as file_router

app = FastAPI(title="FastAPI Docker Example", version="1.0.0")

app.add_middleware(RequestLoggingMiddleware)
# register middleware
add_cors_middleware(app)

# Register custom exception handlers    
app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)
app.add_exception_handler(
    ValueError,
    validation_exception_handler
)
# Register routers
app.include_router(user_router)
app.include_router(file_router)

# --- API Endpoints ---
@app.get("/")
def home():
    return {"message": "FastAPI running inside Docker!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

# Dependency Injection
@app.get("/items")
def read_items(params=Depends(common_parameters)):
    return params
# Using a class-based dependency
@app.get("/items2")
def read_items2(pagination: Annotated[Pagination, Depends()]):
    return {"limit": pagination.limit, "offset": pagination.offset}
# Using a header-based dependency for authentication
@app.get("/secure-data")
def read_secure_data(token=Depends(verify_token)):
    return {"message": "This is secure data"}

# Example of an endpoint that makes an external API call
@app.get("/github")
async def github():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com")

    return r.json()