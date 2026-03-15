from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, field_validator, Field, computed_field, ConfigDict, EmailStr
# Import custom exception handlers
from core.exception_handlers import user_not_found_handler, validation_exception_handler
from exceptions.user_exceptions import UserNotFoundException
# Import logger
from core.logger import logger
from middleware.logging_middleware import RequestLoggingMiddleware


app = FastAPI(title="FastAPI Docker Example", version="1.0.0")

app.add_middleware(RequestLoggingMiddleware)

# Register custom exception handlers    
app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)
app.add_exception_handler(
    ValueError,
    validation_exception_handler
)

# Simple in-memory database
_db: dict[int, dict] = {}
_counter = 1
# --- Schemas --- 
class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(alias="fullName")
    age: int = Field(gt=18, lt=100)
    email: EmailStr
    salary: float 

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            logger.info(f"Validation failed for name: {value}")
            raise ValueError("Name too short")
        return value
 
class UserResponse(UserCreate):
    id: int
    name: str 
    email: str
    salary: float

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

# --- API Endpoints ---
@app.get("/")
def home():
    return {"message": "FastAPI running inside Docker!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/users", response_model=list[UserResponse])
def get_users():
    return list(_db.values())
 
 
@app.get("/users/{user_id}", response_model=UserResponse)
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
 
 
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    global _counter
    for u in _db.values():
        if u["email"] == payload.email:
            logger.info(f"Email already registered: {payload.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
    user = {"id": _counter, "name": payload.name, "age": payload.age, "email": payload.email, "salary": payload.salary}
    _db[_counter] = user
    _counter += 1
    logger.info(f"User created: {user['id']}")
    return user

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