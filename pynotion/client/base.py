from httpx import Headers

from .config import NotionClientConfig


class BaseClient:
    def __init__(self, config: NotionClientConfig):
        self.config = config

    def build_headers(self) -> Headers:
        return Headers(
            {
                "Authorization": f"Bearer {self.config.token}",
                "Notion-Version": self.config.version,
                "Content-Type": "application/json",
            }
        )

    def build_url(self, path: str) -> str:
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
