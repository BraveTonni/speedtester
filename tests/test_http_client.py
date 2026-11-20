import httpx

from src.http_client import HttpxClient


def _client(handler) -> HttpxClient:
    return HttpxClient(transport=httpx.MockTransport(handler))


def test_fetch_returns_full_body_size() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"x" * 1000)

    with _client(handler) as client:
        result = client.fetch("https://example.com/img")

    assert result.ok
    assert result.status_code == 200
    assert result.bytes_downloaded == 1000
    assert result.elapsed_seconds >= 0


def test_fetch_marks_http_error_status() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404)

    with _client(handler) as client:
        result = client.fetch("https://example.com/missing")

    assert not result.ok
    assert result.status_code == 404
    assert "HTTP 404" in result.error


def test_fetch_marks_network_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    with _client(handler) as client:
        result = client.fetch("https://example.com")

    assert not result.ok
    assert "ConnectError" in result.error
    assert result.bytes_downloaded == 0


def test_fetch_marks_invalid_url() -> None:
    with _client(lambda request: httpx.Response(200)) as client:
        result = client.fetch("https://example.com:abc")

    assert not result.ok
    assert "InvalidURL" in result.error
