import pytest
from conftest import failed_result, ok_result

from src.report import InvalidTargetError, Report, Target


def test_target_rejects_non_http_url() -> None:
    with pytest.raises(InvalidTargetError):
        Target.parse("example.com/big.jpg")


def test_target_accepts_http_url() -> None:
    target = Target.parse("  https://example.com/big.jpg  ")

    assert target.url == "https://example.com/big.jpg"


def test_report_counts_success_and_failure() -> None:
    report = Report(
        target=Target(url="https://example.com/x"),
        samples=(ok_result(), failed_result(), ok_result()),
    )

    assert report.successful == 2
    assert report.failed == 1


def test_report_stats_use_only_successful_samples() -> None:
    report = Report(
        target=Target(url="https://example.com/x"),
        samples=(ok_result(size=1_000_000, elapsed=1.0), failed_result()),
    )

    assert report.total_bytes == 1_000_000
    assert report.total_seconds == pytest.approx(1.0)
    assert report.avg_seconds == pytest.approx(1.0)
    assert report.mb_per_s == pytest.approx(1.0)
    assert report.mbps == pytest.approx(8.0)


def test_report_speed_is_zero_without_success() -> None:
    report = Report(
        target=Target(url="https://example.com/x"),
        samples=(failed_result(), failed_result()),
    )

    assert report.successful == 0
    assert report.avg_seconds == 0.0
    assert report.mbps == 0.0
