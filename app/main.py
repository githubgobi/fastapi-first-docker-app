from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
# Import custom exception handlers
from core.exception_handlers import user_not_found_handler, validation_exception_handler
from exceptions.user_exceptions import UserNotFoundException
from db.database import engine, Base
# Import logger
from core.logger import logger
from middleware.logging_middleware import RequestLoggingMiddleware
# CORS Middleware
from middleware.security_middleware import add_cors_middleware
from fastapi_pagination import add_pagination

# Routers
from routers.user_router import router as user_router
from routers.file_router import router as file_router
from routers.blog_router import router as blog_router
from routers.customer_routers import router as customer_router
from routers.auth_router import router as auth_router

from dotenv import load_dotenv
load_dotenv()  

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
app.include_router(blog_router)
app.include_router(customer_router)
app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Add pagination
add_pagination(app)
    
@app.on_event("startup")
async def startup_event():
    # Create database tables
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables created successfully")
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")
