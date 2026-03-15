import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(
            "request_started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host
            }
        )

        try:
            response = await call_next(request)

        except Exception as e:
            logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "error": str(e)
                }
            )
            raise

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time_ms": process_time
            }
        )

        response.headers["X-Request-ID"] = request_id

        return response