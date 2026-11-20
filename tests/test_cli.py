import httpx
import pytest
from conftest import failed_result, ok_result

from main import main
from src.http_client import HttpxClient


@pytest.fixture(autouse=True)
def _stub_fetch(monkeypatch: pytest.MonkeyPatch) -> None:
    # Подменяем сам запрос: CLI-тесты не должны ходить в сеть.
    def fetch(self: HttpxClient, url: str) -> httpx.Response:
        return ok_result()

    monkeypatch.setattr(HttpxClient, "fetch", fetch)


def test_successful_run_prints_report(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["https://example.com/x", "-n", "3"])

    out = capsys.readouterr().out

    assert code == 0
    assert "3.00 MB" in out
    assert "8.00 Мбит/с" in out
    assert "Ошибок:          0" in out


def test_invalid_url_returns_1(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["ftp://example.com/x"])

    captured = capsys.readouterr()

    assert code == 1
    assert "Ошибка" in captured.err


def test_all_requests_failed_returns_1(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fetch(self: HttpxClient, url: str) -> httpx.Response:
        return failed_result()

    monkeypatch.setattr(HttpxClient, "fetch", fetch)

    code = main(["https://example.com/x", "-n", "3"])

    captured = capsys.readouterr()

    assert code == 1
    assert "Ошибка" in captured.err


def test_zero_requests_exits_with_code_2() -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["https://example.com/x", "-n", "0"])

    assert excinfo.value.code == 2


def test_negative_timeout_exits_with_code_2() -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["https://example.com/x", "--timeout", "-1"])

    assert excinfo.value.code == 2
