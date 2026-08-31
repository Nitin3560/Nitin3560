#!/usr/bin/env python3
"""Fetch public GitHub contribution calendar data for the profile graph."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import UTC, date, datetime
from pathlib import Path

import httpx
from lxml import html

USERNAME = "Nitin3560"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "contributions.json"


def contribution_count(label: str) -> int:
    if label.startswith("No contributions"):
        return 0
    match = re.search(r"([\d,]+)\s+contributions?", label)
    return int(match.group(1).replace(",", "")) if match else 0


def streaks(days: list[dict[str, object]]) -> tuple[int, int]:
    ordered = sorted(days, key=lambda item: item["date"])
    longest = current = 0
    for day in ordered:
        if int(day["count"]) > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    current = 0
    latest_active = len(ordered) - 1
    while latest_active >= 0 and int(ordered[latest_active]["count"]) == 0:
        latest_active -= 1

    for day in reversed(ordered[: latest_active + 1]):
        if int(day["count"]) == 0:
            break
        current += 1
    return current, longest


def main() -> None:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = httpx.get(
        url,
        timeout=30,
        follow_redirects=True,
        headers={"User-Agent": f"{USERNAME}-profile-readme"},
    )
    response.raise_for_status()

    root = html.fromstring(response.text)
    cells = root.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " ContributionCalendar-day ")]')
    labels = root.xpath("//tool-tip/text()")

    days: list[dict[str, object]] = []
    for cell, label in zip(cells, labels):
        cell_date = cell.get("data-date")
        if not cell_date:
            continue
        label = " ".join(label.split())
        count = contribution_count(label)
        days.append(
            {
                "date": cell_date,
                "count": count,
                "level": int(cell.get("data-level", "0")),
                "weekday": date.fromisoformat(cell_date).strftime("%A"),
            }
        )

    total_text = " ".join(root.xpath('string(//*[@id="js-contribution-activity-description"])').split())
    total_match = re.search(r"([\d,]+)\s+contributions", total_text)
    total = int(total_match.group(1).replace(",", "")) if total_match else sum(int(day["count"]) for day in days)

    current, longest = streaks(days)
    weekday_counts = Counter()
    for day in days:
        weekday_counts[str(day["weekday"])] += int(day["count"])

    top_day = max(days, key=lambda item: int(item["count"])) if days else {"date": "", "count": 0}
    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "busiest_weekday": weekday_counts.most_common(1)[0][0] if weekday_counts else "",
        "top_day": top_day,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(days)} days and {total:,} contributions")


if __name__ == "__main__":
    main()
