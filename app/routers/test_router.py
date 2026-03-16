from fastapi import APIRouter, Depends
import httpx
from helpers.common_helpers import Pagination, common_parameters, verify_token
from typing import Annotated

router = APIRouter()

# --- API Endpoints ---
@router.get("/")
def home():
    return {"message": "FastAPI running inside Docker!"}

@router.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

# Dependency Injection
@router.get("/items")
def read_items(params=Depends(common_parameters)):
    return params
# Using a class-based dependency
@router.get("/items2")
def read_items2(pagination: Annotated[Pagination, Depends()]):
    return {"limit": pagination.limit, "offset": pagination.offset}
# Using a header-based dependency for authentication
@router.get("/secure-data")
def read_secure_data(token=Depends(verify_token)):
    return {"message": "This is secure data"}

# Example of an endpoint that makes an external API call
@router.get("/github")
async def github():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com")

    return r.json()