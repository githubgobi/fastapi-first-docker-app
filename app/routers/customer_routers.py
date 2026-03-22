from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.customer_service import create_customer, get_customers

router = APIRouter(prefix="/customers")


@router.post("/")
async def add_customer(name: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    return await create_customer(db, name, email, password)


@router.get("/")
async def list_customers(db: AsyncSession = Depends(get_db)):
    return await get_customers(db)