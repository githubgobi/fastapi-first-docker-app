from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, field_validator, Field, computed_field, ConfigDict, EmailStr


app = FastAPI(title="FastAPI Docker Example", version="1.0.0")

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
        raise HTTPException(status_code=404, detail="User not found")
    return user
 
 
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    global _counter
    for u in _db.values():
        if u["email"] == payload.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user = {"id": _counter, "name": payload.name, "age": payload.age, "email": payload.email, "salary": payload.salary}
    _db[_counter] = user
    _counter += 1
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