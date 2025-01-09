import httpx
from loguru import logger
from typing import Dict, Any
from core.config import settings
from models.enums import HttpMethod, HttpContentType

# Configure Loguru to log to a file with rotation
logger.add(f"{settings.LOG_BASE_DIR}/api.log", rotation="10 MB", retention="7 days",
           compression="zip", serialize=True)


class RestAPI:
    def __init__(self):
        # Initialize the HTTP client (You can configure timeouts, base URL, etc. here)
        self.client = httpx.AsyncClient(timeout=8)

    async def _log_request_and_response(self,
                                        url: str,
                                        method: HttpMethod,
                                        content_type: HttpContentType = None,
                                        params: Dict[str, Any] = None,
                                        json: Dict[str, Any] = None,
                                        data: Dict[str, Any] = None,
                                        response: httpx.Response = None,
                                        error: Exception = None):
        request_data = {
            "method": str(method),
            "url": url,
            "params": params,
            "json": str(json)[:settings.MAX_BODY_SIZE] if json else "",
            "data": str(data)[:settings.MAX_BODY_SIZE] if data else "",
            "content_type": str(content_type)
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

    async def send_request(self,
                           url: str,
                           method: HttpMethod,
                           content_type: HttpContentType = HttpContentType.JSON,
                           params: Dict[str, Any] = None,
                           json: Dict[str, Any] = None,
                           data: Dict[str, Any] = None,
                           headers: Dict[str, str] = None) -> httpx.Response:
        """ Send and log request """
        try:
            if method == HttpMethod.GET:
                response = await self.client.get(url, params=params, headers=headers)
            elif method == HttpMethod.POST and content_type == HttpContentType.FORM:
                response = await self.client.post(url, data=data, params=params, headers=headers)
            elif method == HttpMethod.POST and content_type != HttpContentType.FORM:
                response = await self.client.post(url, json=json, params=params, headers=headers)
            elif method == HttpMethod.DELETE:
                response = await self.client.delete(url, params=params, headers=headers)
            elif method == HttpMethod.PUT:
                response = await self.client.put(url, data=data, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method")

            # Log the request and response
            await self._log_request_and_response(url, method, content_type, params, json, data, response)
            return response

        except Exception as e:
            # Log the error
            await self._log_request_and_response(url, method, content_type, params, json, data, None, e)
            raise e  # Reraise the exception if needed
