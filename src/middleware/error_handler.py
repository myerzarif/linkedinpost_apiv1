from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any
import logging
import traceback
from bson.errors import InvalidId
from pymongo.errors import PyMongoError
from beanie.exceptions import DocumentNotFound
from pydantic import ValidationError

logger = logging.getLogger("app")

class APIErrorHandler:
    async def __call__(
        self,
        request: Request,
        call_next
    ) -> Union[JSONResponse, Any]:
        try:
            return await call_next(request)
            
        except DocumentNotFound as e:
            logger.warning(f"Document not found: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "error": "Resource not found",
                    "detail": str(e)
                }
            )
            
        except InvalidId as e:
            logger.warning(f"Invalid MongoDB ObjectId: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Invalid identifier format",
                    "detail": "The provided ID is not in the correct format"
                }
            )
            
        except PyMongoError as e:
            logger.error(f"MongoDB Error: {str(e)}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Database error",
                    "detail": "An error occurred while processing your request"
                }
            )
            
        except ValidationError as e:
            logger.warning(f"Validation error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": "Validation error",
                    "detail": e.errors()
                }
            )
            
        except Exception as e:
            # Log the full traceback for unexpected errors
            logger.error(
                f"Unexpected error: {str(e)}\n"
                f"Route: {request.url.path}\n"
                f"Method: {request.method}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            
            # In development, you might want to return the actual error
            debug_mode = request.app.state.settings.DEBUG
            error_detail = str(e) if debug_mode else "An unexpected error occurred"
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "detail": error_detail,
                    # Include request ID if you implement request tracking
                    "request_id": request.state.request_id if hasattr(request.state, 'request_id') else None
                }
            )