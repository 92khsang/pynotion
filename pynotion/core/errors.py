from enum import Enum


class ErrorCode(str, Enum):
    INVALID_JSON = "invalid_json"
    INVALID_REQUEST_URL = "invalid_request_url"
    INVALID_REQUEST = "invalid_request"
    INVALID_GRANT = "invalid_grant"
    VALIDATION_ERROR = "validation_error"
    MISSING_VERSION = "missing_version"
    UNAUTHORIZED = "unauthorized"
    RESTRICTED_RESOURCE = "restricted_resource"
    OBJECT_NOT_FOUND = "object_not_found"
    CONFLICT_ERROR = "conflict_error"
    RATE_LIMITED = "rate_limited"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    BAD_GATEWAY = "bad_gateway"
    SERVICE_UNAVAILABLE = "service_unavailable"
    DATABASE_CONNECTION_UNAVAILABLE = "database_connection_unavailable"
    GATEWAY_TIMEOUT = "gateway_timeout"


class NotionAPIError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status = status
        self.code = ErrorCode(code) if code in ErrorCode.__members__.values() else code
        self.message = message
        super().__init__(f"{status} {code}: {message}")


class NotionClientError(Exception):
    pass


class NotionTimeoutError(NotionClientError):
    pass


class NotionNetworkError(NotionClientError):
    pass
