"""Application-level HTTP errors."""

from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, message: str, code: str = "app_error", status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class ModelNotReadyError(AppError):
    def __init__(self, message: str = "Risk model is not loaded") -> None:
        super().__init__(message, code="model_not_ready", status_code=503)


class NotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="not_found", status_code=404)


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": exc.code, "detail": exc.message},
    )


def http_503(detail: str) -> HTTPException:
    return HTTPException(status_code=503, detail=detail)
