"""HTTP-клиент на httpx: запросы с ожиданием полного тела."""

import time
from typing import Self

import httpx

from src.report import FetchResult

DEFAULT_TIMEOUT_SECONDS = 30.0

# Ловим обе ветки: InvalidURL не наследует HTTPError.
NETWORK_ERRORS = (httpx.HTTPError, httpx.InvalidURL)


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

    def fetch(self, url: str) -> FetchResult:
        """Скачивает ответ целиком; сбой уходит в поле error, не в raise."""
        started = time.perf_counter()

        try:
            response = self._client.get(url)
        except NETWORK_ERRORS as exc:
            return FetchResult(
                elapsed_seconds=time.perf_counter() - started,
                bytes_downloaded=0,
                error=f"{type(exc).__name__}: {exc}",
            )

        elapsed = time.perf_counter() - started

        if response.status_code >= 400:
            return FetchResult(
                elapsed_seconds=elapsed,
                bytes_downloaded=0,
                status_code=response.status_code,
                error=f"HTTP {response.status_code}",
            )

        return FetchResult(
            elapsed_seconds=elapsed,
            bytes_downloaded=len(response.content),
            status_code=response.status_code,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
