#!/usr/bin/env python3
"""Render self-hosted metrics SVGs for the profile README."""

from __future__ import annotations

import html
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ASSETS / "contributions.json"

GREEN = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
LANGUAGES = [
    ("Python", 36, "#3572A5"),
    ("C++", 24, "#f34b7d"),
    ("Java", 16, "#b07219"),
    ("TypeScript", 11, "#3178c6"),
    ("JavaScript", 8, "#f1e05a"),
    ("Shell", 5, "#89e051"),
]


def read_payload() -> dict[str, object]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def render_stats(payload: dict[str, object], suffix: str, *, dark: bool) -> None:
    total = int(payload["total"])
    current = int(payload["current_streak"])
    longest = int(payload["longest_streak"])
    bg = "#0d1117" if dark else "#ffffff"
    border = "#30363d" if dark else "#d0d7de"
    text = "#e6edf3" if dark else "#24292f"
    muted = "#8b949e" if dark else "#57606a"
    line = "#30363d" if dark else "#d8dee4"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="224" viewBox="0 0 680 224" role="img" aria-label="GitHub statistics for Nitin3560">
  <style>
    .panel {{ fill: {bg}; stroke: {border}; stroke-width: 1.4; }}
    .name {{ fill: #39d353; font: 800 21px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .tag {{ fill: {muted}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .num {{ fill: {text}; font: 800 33px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: {muted}; font: 600 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .rule {{ stroke: {line}; stroke-width: 1; }}
  </style>
  <rect x="1" y="1" width="678" height="222" rx="8" class="panel"/>
  <text x="32" y="46" class="name">Nitin3560</text>
  <text x="548" y="46" text-anchor="end" class="tag">at a glance</text>
  <line x1="32" y1="68" x2="648" y2="68" class="rule"/>
  <text x="32" y="112" class="num">4</text>
  <text x="32" y="136" class="label">Selected repos</text>
  <text x="236" y="112" class="num">{total:,}</text>
  <text x="236" y="136" class="label">Contributions (1y)</text>
  <text x="478" y="112" class="num">2026</text>
  <text x="478" y="136" class="label">MS graduation</text>
  <text x="32" y="180" class="num">{current}</text>
  <text x="32" y="204" class="label">Current streak</text>
  <text x="236" y="180" class="num">{longest}</text>
  <text x="236" y="204" class="label">Longest streak</text>
  <text x="478" y="180" class="num">IEEE</text>
  <text x="478" y="204" class="label">CSCN accepted</text>
</svg>
'''
    write(ASSETS / f"card-stats-{suffix}.svg", svg)


def render_languages() -> None:
    width, height = 680, 190
    x = 32
    bars = []
    labels = []
    for name, pct, color in LANGUAGES:
        bar_width = int(616 * pct / 100)
        bars.append(f'<rect x="{x}" y="65" width="{bar_width}" height="17" fill="{color}"/>')
        label_y = 116 + len(labels) * 24
        labels.append(
            f'<circle cx="{x + 6}" cy="{label_y}" r="5" fill="{color}"/>'
            f'<text x="{x + 18}" y="{label_y + 5}" class="label">{html.escape(name)} {pct}%</text>'
        )
        x += bar_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Most used languages">
  <style>
    .title {{ fill: #39d353; font: 800 20px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #c9d1d9; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .bar-bg {{ fill: #161b22; }}
  </style>
  <text x="32" y="34" class="title">8 languages</text>
  <rect x="32" y="65" width="616" height="17" rx="4" class="bar-bg"/>
  <g>{''.join(bars)}</g>
  <g>{''.join(labels)}</g>
</svg>
'''
    write(ASSETS / "metrics.languages.svg", svg)


def render_achievements(payload: dict[str, object]) -> None:
    total = int(payload["total"])
    longest = int(payload["longest_streak"])
    top_day = payload.get("top_day", {})
    top_count = int(top_day.get("count", 0)) if isinstance(top_day, dict) else 0
    items = [
        ("Commit Engine", f"{total:,} contributions in one year"),
        ("Long Runner", f"{longest}-day longest streak"),
        ("Peak Day", f"{top_count} contributions on the top day"),
    ]
    cards = []
    for index, (title, detail) in enumerate(items):
        x = 28 + index * 210
        cards.append(
            f'''<g>
  <rect x="{x}" y="44" width="190" height="118" rx="8" class="card"/>
  <text x="{x + 18}" y="82" class="badge">◆</text>
  <text x="{x + 44}" y="82" class="title">{html.escape(title)}</text>
  <text x="{x + 18}" y="124" class="detail">{html.escape(detail)}</text>
</g>'''
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="190" viewBox="0 0 680 190" role="img" aria-label="GitHub achievements">
  <style>
    .card {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.2; }}
    .badge {{ fill: #39d353; font: 800 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .title {{ fill: #e6edf3; font: 800 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .detail {{ fill: #8b949e; font: 700 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <g>{''.join(cards)}</g>
</svg>
'''
    write(ASSETS / "metrics.achievements.svg", svg)


def iso_point(col: int, row: int, cell: float = 9.5) -> tuple[float, float]:
    return 120 + (col - row) * cell * 0.82, 170 + (col + row) * cell * 0.42


def cube(x: float, y: float, h: float, color: str) -> str:
    half_w = 8
    half_h = 4.5
    full_h = 9
    top = f"{x:.1f},{y - h:.1f} {x + half_w:.1f},{y - h + half_h:.1f} {x:.1f},{y - h + full_h:.1f} {x - half_w:.1f},{y - h + half_h:.1f}"
    left = f"{x - half_w:.1f},{y - h + half_h:.1f} {x:.1f},{y - h + full_h:.1f} {x:.1f},{y + full_h:.1f} {x - half_w:.1f},{y + half_h:.1f}"
    right = f"{x:.1f},{y - h + full_h:.1f} {x + half_w:.1f},{y - h + half_h:.1f} {x + half_w:.1f},{y + half_h:.1f} {x:.1f},{y + full_h:.1f}"
    return f'<polygon points="{left}" fill="#0f5132"/><polygon points="{right}" fill="#238636"/><polygon points="{top}" fill="{color}"/>'


def render_isocalendar(payload: dict[str, object]) -> None:
    days = sorted(payload["days"], key=lambda item: item["date"])
    start = date.fromisoformat(days[0]["date"])
    total = int(payload["total"])
    current = int(payload["current_streak"])
    longest = int(payload["longest_streak"])
    top_day = payload.get("top_day", {})
    top_count = int(top_day.get("count", 0)) if isinstance(top_day, dict) else 0

    cells = []
    flat = []
    for day in days:
        dt = date.fromisoformat(day["date"])
        week = (dt - start).days // 7
        weekday = dt.weekday()
        level = int(day["level"])
        count = int(day["count"])
        color = GREEN[level]
        x, y = iso_point(week, weekday)
        if count:
            cells.append(cube(x, y, min(36, 4 + count * 0.55), color))
        else:
            top = f"{x:.1f},{y:.1f} {x + 8:.1f},{y + 4.5:.1f} {x:.1f},{y + 9:.1f} {x - 8:.1f},{y + 4.5:.1f}"
            cells.append(f'<polygon points="{top}" fill="#d1d5db" opacity="0.92"/>')

        fx = 58 + week * 12
        fy = 472 + weekday * 12
        flat.append(f'<rect x="{fx}" y="{fy}" width="9" height="9" rx="2" fill="{color}"/>')

    weekday_counts = Counter()
    for day in days:
        weekday_counts[str(day["weekday"])] += int(day["count"])
    average = total / max(1, len(days))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="930" height="590" viewBox="0 0 930 590" role="img" aria-label="3D isometric contribution calendar for Nitin3560">
  <style>
    .heading {{ fill: #39d353; font: 700 30px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .meta-title {{ fill: #39d353; font: 700 23px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .meta {{ fill: #8b949e; font: 600 20px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .track {{ fill: #014421; }}
  </style>
  <text x="58" y="58" class="heading">$ contributions.calendar</text>
  <text x="520" y="104" class="meta-title">Commits streaks</text>
  <text x="520" y="137" class="meta">Current streak {current} days</text>
  <text x="520" y="168" class="meta">Best streak {longest} days</text>
  <text x="520" y="222" class="meta-title">Commits per day</text>
  <text x="520" y="255" class="meta">Highest in a day at {top_count}</text>
  <text x="520" y="286" class="meta">Average per day at ~{average:.2f}</text>
  <g>{''.join(cells)}</g>
  <g>{''.join(flat)}</g>
  <rect x="58" y="558" width="550" height="14" class="track"/>
</svg>
'''
    write(ASSETS / "metrics.isocalendar.svg", svg)


def main() -> None:
    payload = read_payload()
    render_isocalendar(payload)
    render_stats(payload, "dark", dark=True)
    render_stats(payload, "light", dark=False)
    render_languages()
    render_achievements(payload)


if __name__ == "__main__":
    main()
