import pytest
from conftest import FakeClient, failed_result, ok_result

from src.report import Target
from src.speedtest import SpeedTestService


def _service(client: FakeClient) -> SpeedTestService:
    return SpeedTestService(client)


def test_runs_requested_number_of_requests() -> None:
    client = FakeClient(ok_result())
    report = _service(client).run(
        Target.parse("https://example.com/x"), requests=10
    )

    assert client.calls == 10
    assert len(report.samples) == 10
    assert report.total_bytes == 10_000_000
    assert report.avg_seconds == pytest.approx(1.0)
    assert report.mbps == pytest.approx(8.0)
    assert report.mb_per_s == pytest.approx(1.0)


def test_failed_request_does_not_stop_run() -> None:
    client = FakeClient(failed_result(), ok_result(), failed_result())
    report = _service(client).run(
        Target.parse("https://example.com/x"), requests=3
    )

    assert client.calls == 3
    assert len(report.samples) == 3
    assert report.successful == 1
    assert report.failed == 2


def test_rejects_zero_requests() -> None:
    with pytest.raises(ValueError):
        _service(FakeClient(ok_result())).run(
            Target.parse("https://example.com/x"), requests=0
        )
