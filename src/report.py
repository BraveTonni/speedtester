"""Сущности замера: адрес, итог одного запроса и отчёт."""

from dataclasses import dataclass
from typing import Self
from urllib.parse import urlparse


class InvalidTargetError(ValueError):
    """Адрес для запросов задан некорректно."""


@dataclass(frozen=True)
class Target:
    """Адрес, к которому стучимся."""

    url: str

    @classmethod
    def parse(cls, raw: str) -> Self:
        value = raw.strip()
        parsed = urlparse(value)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise InvalidTargetError(
                f"нужен http(s)-адрес вида https://host/path, "
                f"получено: {raw!r}"
            )

        return cls(url=value)


@dataclass(frozen=True)
class FetchResult:
    """Итог одного запроса: время, объём, статус и описание сбоя."""

    elapsed_seconds: float
    bytes_downloaded: int
    status_code: int | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None
