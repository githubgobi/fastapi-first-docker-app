from fastapi import FastAPI
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
from routers.test_router import router as test_router

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
app.include_router(test_router)

