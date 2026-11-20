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


@dataclass(frozen=True)
class Report:
    """Отчёт по прогону: агрегаты по успешным запросам."""

    target: Target
    samples: tuple[FetchResult, ...]

    @property
    def _ok(self) -> tuple[FetchResult, ...]:
        """Успешные запросы: по ним считается вся статистика."""
        return tuple(sample for sample in self.samples if sample.ok)

    @property
    def successful(self) -> int:
        return len(self._ok)

    @property
    def failed(self) -> int:
        return len(self.samples) - self.successful

    @property
    def total_bytes(self) -> int:
        return sum(sample.bytes_downloaded for sample in self._ok)

    @property
    def total_seconds(self) -> float:
        return sum(sample.elapsed_seconds for sample in self._ok)

    @property
    def avg_seconds(self) -> float:
        if not self.successful:
            return 0.0

        return self.total_seconds / self.successful

    @property
    def mb_per_s(self) -> float:
        """Мегабайт/с: суммарные байты / суммарное время."""
        if not self.total_seconds:
            return 0.0

        return self.total_bytes / self.total_seconds / 1_000_000

    @property
    def mbps(self) -> float:
        """Мегабит/с: суммарные биты / суммарное время."""
        return self.mb_per_s * 8
