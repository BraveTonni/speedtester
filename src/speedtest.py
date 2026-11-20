"""Сценарий замера: последовательные запросы."""

from src.http_client import HttpxClient
from src.report import Report, Target


class SpeedTestService:
    """Делает N последовательных запросов и собирает отчёт.

    Сбои не прерывают прогон: неудачный запрос попадает в отчёт со
    своим текстом ошибки, статистика считается только по успешным.
    """

    def __init__(self, client: HttpxClient) -> None:
        self._client = client

    def run(self, target: Target, requests: int = 10) -> Report:
        if requests < 1:
            raise ValueError("количество запросов должно быть не меньше 1")

        samples = tuple(
            self._client.fetch(target.url) for _ in range(requests)
        )

        return Report(target=target, samples=samples)
