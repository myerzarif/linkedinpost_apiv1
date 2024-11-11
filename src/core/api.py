from fastapi import FastAPI
import httpx
from typing import Dict, Any
from models.enums import HttpMethod, HttpContentType


class RestAPI:
    def __init__(self):
        # Initialize the HTTP client (You can configure timeouts, base URL, etc. here)
        self.client = httpx.Client(timeout=8)

    async def send_request(self,
                           url: str,
                           method: HttpMethod,
                           content_type: HttpContentType = None,
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
                response = await self.client.put(url, json=json, params=params, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method")

            # Log the request and response
            await self._log_request_and_response(method, url, content_type, params, json, data, response)
            return response

        except Exception as e:
            # Log the error
            await self._log_request_and_response(method, url, content_type, params, json, data, None, e)
            raise e  # Reraise the exception if needed
