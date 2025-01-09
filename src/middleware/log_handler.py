import time
import uuid
from loguru import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from core.config import settings
import json
from typing import Dict, Any
import httpx

# Configure Loguru to log to a file with rotation
logger.add(f"{settings.LOG_BASE_DIR}/app.log", rotation="10 MB",
           retention="7 days", compression="zip", serialize=True)


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request is related to OpenAPI (Swagger Docs)
        if request.url.path in ["/docs", "/openapi.json"]:
            return await call_next(request)

        request_id = str(uuid.uuid4())  # Generate a unique request ID
        start_time = time.time()

        try:
            # Process the request and get the response
            response = await call_next(request)
            response_status = response.status_code
            response_body = [chunk async for chunk in response.body_iterator]
            response_body = response_body[0].decode()

        except Exception as e:
            # Capture the exception details
            response_status = 500
            response_body = str(e)

            # Log the error in JSON format to Loguru
            logger.error({
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "body": (await request.body()).decode("utf-8") if await request.body() else None,
                },
                "response": {
                    "status_code": response_status,
                    "error": response_body,
                },
                "duration": time.time() - start_time,
                "request_id": request_id,
            })

            # Return a structured error response to the client
            return JSONResponse(
                status_code=response_status,
                content={
                    "detail": "Internal Server Error!",
                    "request_id": request_id,
                    "error": response_body,
                },
            )

        # Log the successful response in JSON format to Loguru
        duration = time.time() - start_time
        request_body = await request.body()

        log_data = {
            "request": {
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "body": request_body.decode("utf-8")[:settings.MAX_BODY_SIZE] if request_body else None,
            },
            "response": {
                "status_code": response_status,
                "body": response_body[:settings.MAX_BODY_SIZE] if isinstance(response_body, bytes) else response_body[:settings.MAX_BODY_SIZE],
            },
            "duration": duration,
            "request_id": request_id,
        }

        logger.info(log_data)

        # Check if the response is JSON to wrap it
        if response.headers.get("content-type") == "application/json":
            response_body = {
                "request_id": request_id,
                "result": json.loads(response_body),
            }
            # Send the new wrapped response
            return JSONResponse(content=response_body, status_code=response.status_code)

        # Return the original response to the client
        return response


async def _log_request_and_response(self,
                                        method: str,
                                        url: str,
                                        content_type: str = None,
                                        params: Dict[str, Any] = None,
                                        json: Dict[str, Any] = None,
                                        data: Dict[str, Any] = None,
                                        response: httpx.Response = None,
                                        error: Exception = None):
        request_data = {
            "method": method,
            "url": url,
            "params": params,
            "json": str(json)[:settings.MAX_BODY_SIZE],
            "data": str(data)[:settings.MAX_BODY_SIZE],
            "content_type": content_type
        }

        if error:
            logger.error({
                "request": request_data,
                "error": str(error),
            })
        else:
            response_data = {
                "status_code": response.status_code,
                # Limiting to 500 chars for logging
                "body": response.text[:settings.MAX_BODY_SIZE],
                "headers": dict(response.headers)
            }
            logger.info({
                "request": request_data,
                "response": response_data,
            })
