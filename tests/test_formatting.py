from conftest import ok_result

from src.formatting import format_report
from src.report import FetchResult, Report, Target


def _report() -> Report:
    return Report(
        target=Target(url="https://example.com/x.jpg"),
        samples=(
            FetchResult(1.0, 1_000_000, 200),
            FetchResult(1.0, 1_000_000, 200),
        ),
    )


def test_format_report_contains_key_numbers() -> None:
    text = format_report(_report())

    assert "https://example.com/x.jpg" in text
    assert "2.00 MB" in text
    assert "1000.0 ms/запрос" in text
    assert "8.00 Мбит/с" in text
    assert "1.00 МБ/с" in text


def test_format_report_counts_requests_and_errors() -> None:
    text = format_report(
        Report(
            target=Target(url="https://example.com/x"),
            samples=(ok_result(), ok_result(), ok_result()),
        )
    )

    assert "3 (последовательно)" in text
    assert "Ошибок:          0" in text
