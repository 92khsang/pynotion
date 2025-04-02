import httpx

from .errors import (
    NotionAPIError,
    NotionNetworkError,
    NotionTimeoutError,
)


def handle_response(response: httpx.Response) -> dict:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError:
        try:
            error_data = response.json()
            raise NotionAPIError(
                status=response.status_code,
                code=error_data.get("code", "unknown_error"),
                message=error_data.get("message", "Unknown error"),
            )
        except ValueError:
            raise NotionAPIError(
                status=response.status_code,
                code="invalid_response",
                message="Response was not valid JSON",
            )
    return response.json()


def handle_http_error(e: Exception):
    if isinstance(e, httpx.TimeoutException):
        raise NotionTimeoutError("Request timed out") from e
    elif isinstance(e, httpx.RequestError):
        raise NotionNetworkError("Network error occurred") from e
    else:
        raise
