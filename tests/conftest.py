"""Общие фейки для тестов."""

from src.report import FetchResult


class FakeClient:
    """Клиент-подстановка: отдаёт заданные исходы по порядку.

    Когда сценарий исчерпан - повторяет последний исход.
    """

    def __init__(self, *outcomes: FetchResult) -> None:
        if not outcomes:
            raise ValueError("нужен хотя бы один исход")
        self._outcomes = list(outcomes)
        self.calls = 0

    def fetch(self, url: str) -> FetchResult:
        self.calls += 1

        if len(self._outcomes) > 1:
            return self._outcomes.pop(0)

        return self._outcomes[0]


def ok_result(size: int = 1_000_000, elapsed: float = 1.0) -> FetchResult:
    return FetchResult(
        elapsed_seconds=elapsed, bytes_downloaded=size, status_code=200
    )


def failed_result(error: str = "boom") -> FetchResult:
    return FetchResult(elapsed_seconds=0.5, bytes_downloaded=0, error=error)
