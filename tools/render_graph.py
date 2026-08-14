#!/usr/bin/env python3
"""Render the animated contribution calendar SVG."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "contributions.json"
OUT = ROOT / "graph.svg"

LEVELS = ["#101827", "#134e4a", "#0f766e", "#22d3ee", "#a7f3d0"]
WEEKDAYS = ["Mon", "Wed", "Fri"]


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"]
    by_week: dict[int, list[dict[str, object]]] = defaultdict(list)
    start = date.fromisoformat(days[0]["date"])
    for day in days:
        dt = date.fromisoformat(day["date"])
        week = (dt - start).days // 7
        by_week[week].append(day)

    cell, gap = 12, 4
    left, top = 64, 56
    width, height = 930, 214
    squares = []
    for week in sorted(by_week):
        for day in by_week[week]:
            dt = date.fromisoformat(day["date"])
            weekday = dt.weekday()
            x = left + week * (cell + gap)
            y = top + ((weekday + 1) % 7) * (cell + gap)
            level = int(day["level"])
            delay = week * 0.025
            squares.append(
                f'''<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[level]}" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.28s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="0 6;0 0" begin="{delay:.3f}s" dur="0.28s" fill="freeze"/>
    </rect>'''
            )

    labels = []
    for offset, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        labels.append(f'<text x="24" y="{top + offset * (cell + gap) + 10}" class="axis">{label}</text>')

    legend = []
    legend_x = 694
    for index, color in enumerate(LEVELS):
        legend.append(f'<rect x="{legend_x + index * 20}" y="178" width="12" height="12" rx="3" fill="{color}"/>')

    top_day = payload.get("top_day", {})
    stats = (
        f'{payload["total"]:,} contributions | current streak {payload["current_streak"]}d | '
        f'longest {payload["longest_streak"]}d | busiest {payload["busiest_weekday"]}'
    )
    top_line = f'top day {top_day.get("date", "n/a")} : {top_day.get("count", 0)} contributions'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated GitHub contribution graph for Nitin3560">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="55%" stop-color="#08111f"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
  <style>
    .panel {{ fill: url(#bg); stroke: #38bdf8; stroke-width: 1.2; }}
    .title {{ fill: #e5f4ff; font: 700 17px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .axis {{ fill: #8aa4b8; font: 500 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .meta {{ fill: #b7c7d6; font: 600 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .accent {{ fill: #5eead4; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="panel"/>
  <text x="24" y="31" class="title">$ cat contributions.log</text>
  {''.join(labels)}
  <g>{''.join(squares)}</g>
  <text x="634" y="188" class="axis">less</text>
  {''.join(legend)}
  <text x="802" y="188" class="axis">more</text>
  <text x="24" y="184" class="meta">{stats}</text>
  <text x="24" y="204" class="accent">{top_line}</text>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
