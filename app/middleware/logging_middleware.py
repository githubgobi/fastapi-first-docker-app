from app.core import logger
from starlette.middleware.base import BaseHTTPMiddleware
import time

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            "request_completed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration": process_time
            }
        )

        return response