# speedtester

Консольный замер скорости интернета: делает последовательные запросы
к одному адресу, считает среднее время запроса, общий объём скачанного
и скорость скачивания.

## Запуск (uv)

```bash
uv sync                 # установить зависимости (httpx, pytest)
uv run main.py https://example.com/big.jpg
```

Опции:

```bash
uv run main.py <url> [-n N] [--timeout SEC]
```

- `<url>` - адрес, к которому стучимся (нужен `http://` или `https://`);
- `-n, --requests N` - количество последовательных запросов, по умолчанию `10`;
- `--timeout SEC` - таймаут одного запроса, по умолчанию `30`.

Пример:

```bash
uv run main.py https://speed.cloudflare.com/__down?bytes=25000000 -n 10
```

Тесты:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```
