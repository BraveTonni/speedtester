import argparse
import sys

from src.formatting import format_report
from src.http_client import DEFAULT_TIMEOUT_SECONDS, HttpxClient
from src.report import InvalidTargetError, Target
from src.speedtest import SpeedTestService


def main(argv: list[str] | None = None) -> int:
    # аргументы
    parser = argparse.ArgumentParser(
        prog="speedtester",
        description=(
            "Замер скорости скачивания: последовательные запросы "
            "к адресу, среднее время и скорость."
        ),
    )
    parser.add_argument("url", help="например https://example.com/big.jpg")
    parser.add_argument(
        "-n",
        "--requests",
        type=int,
        default=10,
        metavar="N",
        help="количество последовательных запросов (по умолчанию 10)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        metavar="SEC",
        help="таймаут одного запроса в секундах (по умолчанию 30)",
    )
    args = parser.parse_args(argv)

    if args.requests < 1:
        parser.error("--requests должен быть не меньше 1")

    if args.timeout <= 0:
        parser.error("--timeout должен быть положительным")

    # спидтест
    try:
        target = Target.parse(args.url)
    except InvalidTargetError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)

        return 1

    with HttpxClient(args.timeout) as client:
        report = SpeedTestService(client).run(target, args.requests)

    # отчет
    if not report.successful:
        print(
            f"Ошибка: не удался ни один из {len(report.samples)} запросов",
            file=sys.stderr,
        )

        return 1

    print(format_report(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
