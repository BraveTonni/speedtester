"""Форматирование отчёта для вывода в консоль."""

from src.report import Report


def format_report(report: Report) -> str:
    """Отчёт в человекочитаемом виде; единицы - MB, Мбит/с, МБ/с (SI)."""
    lines = [
        "Замер скорости скачивания",
        f"  Цель:            {report.target.url}",
        f"  Запросов:        {len(report.samples)} (последовательно)",
        f"  Ошибок:          {report.failed}",
        f"  Объём:           {report.total_bytes / 1_000_000:.2f} MB",
        f"  Суммарное время: {report.total_seconds:.2f} s",
        f"  Среднее время:   {report.avg_seconds * 1000:.1f} ms/запрос",
        f"  Скорость:        {report.mbps:.2f} Мбит/с "
        f"({report.mb_per_s:.2f} МБ/с)",
    ]

    return "\n".join(lines)
