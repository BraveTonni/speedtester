"""HTTP-клиент на httpx: запросы с ожиданием полного тела."""

from typing import Self

import httpx

DEFAULT_TIMEOUT_SECONDS = 30.0


class HttpxClient:
    """Делает запросы и держит пул соединений httpx."""

    def __init__(
        self,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            timeout=timeout_seconds,
            follow_redirects=True,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
