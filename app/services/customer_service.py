from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.customer_schema import Customer
from core.security import hash_password


async def create_customer(db: AsyncSession, name: str, email: str, password: str):
    hashed_pwd = hash_password(password)
    customer = Customer(name=name, email=email, hashed_password=hashed_pwd)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


async def get_customers(db: AsyncSession):
    result = await db.execute(select(Customer))
    return result.scalars().all()