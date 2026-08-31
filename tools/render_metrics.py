#!/usr/bin/env python3
"""Render self-hosted metrics SVGs for the profile README."""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ASSETS / "contributions.json"

GREEN = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
LANGUAGES = [
    ("Python", "2.10 MB", 44.0, "#3572A5"),
    ("C++", "1.25 MB", 26.2, "#f34b7d"),
    ("Java", "612 kB", 12.8, "#b07219"),
    ("TypeScript", "410 kB", 8.6, "#3178c6"),
    ("JavaScript", "230 kB", 4.8, "#f1e05a"),
    ("Shell", "96 kB", 2.0, "#89e051"),
    ("CMake", "51 kB", 1.1, "#DA3434"),
    ("HTML", "24 kB", 0.5, "#e34c26"),
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
    public_repos = 14
    followers = 1
    total_stars = 7
    bg = "#0d1117" if dark else "#ffffff"
    border = "#30363d" if dark else "#d0d7de"
    text = "#e6edf3" if dark else "#24292f"
    muted = "#8b949e" if dark else "#57606a"
    line = "#30363d" if dark else "#d8dee4"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="224" viewBox="0 0 680 224" role="img" aria-label="GitHub statistics for Nitin3560">
  <style>
    .panel {{ fill: {bg}; stroke: {border}; stroke-width: 1.4; }}
    .name {{ fill: #39d353; font: 800 20px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .tag {{ fill: {muted}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .num {{ fill: {text}; font: 800 33px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: {muted}; font: 600 14px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .rule {{ stroke: {line}; stroke-width: 1; }}
  </style>
  <rect x="1" y="1" width="678" height="222" rx="8" class="panel"/>
  <text x="32" y="46" class="name">Nitin3560</text>
  <text x="548" y="46" text-anchor="end" class="tag">at a glance</text>
  <line x1="32" y1="68" x2="648" y2="68" class="rule"/>
  <text x="32" y="112" class="num">{total_stars}</text>
  <text x="32" y="136" class="label">Total stars</text>
  <text x="250" y="112" class="num">{public_repos}</text>
  <text x="250" y="136" class="label">Public repos</text>
  <text x="468" y="112" class="num">{followers}</text>
  <text x="468" y="136" class="label">Followers</text>
  <text x="32" y="180" class="num">{total:,}</text>
  <text x="32" y="204" class="label">Contributions (1y)</text>
  <text x="250" y="180" class="num">{current}</text>
  <text x="250" y="204" class="label">Current streak</text>
  <text x="468" y="180" class="num">{longest}</text>
  <text x="468" y="204" class="label">Longest streak</text>
</svg>
'''
    write(ASSETS / f"card-stats-{suffix}.svg", svg)


def render_languages() -> None:
    width, height = 680, 250
    x = 32
    bars = []
    labels = []
    for index, (name, size, pct, color) in enumerate(LANGUAGES):
        bar_width = int(616 * pct / 100)
        bars.append(f'<rect x="{x}" y="82" width="{bar_width}" height="12" fill="{color}"/>')
        col = index % 2
        row = index // 2
        label_x = 44 + col * 330
        label_y = 126 + row * 27
        labels.append(
            f'<circle cx="{label_x}" cy="{label_y}" r="5" fill="{color}"/>'
            f'<text x="{label_x + 22}" y="{label_y + 5}" class="lang">{html.escape(name)}</text>'
            f'<text x="{label_x + 154}" y="{label_y + 5}" class="size">{html.escape(size)}</text>'
            f'<text x="{label_x + 252}" y="{label_y + 5}" class="pct">{pct:.2f}%</text>'
        )
        x += bar_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Most used languages">
  <style>
    .title {{ fill: #0969da; font: 500 22px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .subtitle {{ fill: #0969da; font: 500 20px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .lang {{ fill: #8b949e; font: 600 17px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .size {{ fill: #8b949e; font: 500 15px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .pct {{ fill: #8b949e; font: 500 15px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .bar-bg {{ fill: #161b22; }}
  </style>
  <text x="32" y="34" class="title">8 Languages</text>
  <text x="340" y="66" text-anchor="middle" class="subtitle">Most used languages</text>
  <rect x="32" y="82" width="616" height="12" rx="5" class="bar-bg"/>
  <g>{''.join(bars)}</g>
  <g>{''.join(labels)}</g>
</svg>
'''
    write(ASSETS / "metrics.languages.svg", svg)


def iso_point(col: int, row: int, cell: float = 13.2) -> tuple[float, float]:
    return 128 + (col - row) * cell * 0.82, 202 + (col + row) * cell * 0.42


def cube(x: float, y: float, h: float, color: str) -> str:
    half_w = 11
    half_h = 6
    full_h = 12
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
    for day in days:
        dt = date.fromisoformat(day["date"])
        week = (dt - start).days // 7
        weekday = dt.weekday()
        level = int(day["level"])
        count = int(day["count"])
        color = GREEN[level]
        x, y = iso_point(week, weekday)
        if count:
            cells.append(cube(x, y, min(48, 6 + count * 0.68), color))
        else:
            top = f"{x:.1f},{y:.1f} {x + 11:.1f},{y + 6:.1f} {x:.1f},{y + 12:.1f} {x - 11:.1f},{y + 6:.1f}"
            cells.append(f'<polygon points="{top}" fill="#d1d5db" opacity="0.92"/>')

    average = total / max(1, len(days))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="520" viewBox="0 0 1180 520" role="img" aria-label="3D isometric contribution calendar for Nitin3560">
  <style>
    .heading {{ fill: #39d353; font: 700 30px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .meta-title {{ fill: #39d353; font: 700 23px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .meta {{ fill: #8b949e; font: 600 20px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .track {{ fill: #014421; }}
  </style>
  <text x="82" y="58" class="heading">$ contributions.calendar</text>
  <text x="790" y="112" class="meta-title">Commits streaks</text>
  <text x="790" y="145" class="meta">Current streak {current} days</text>
  <text x="790" y="176" class="meta">Best streak {longest} days</text>
  <text x="790" y="238" class="meta-title">Commits per day</text>
  <text x="790" y="271" class="meta">Highest in a day at {top_count}</text>
  <text x="790" y="302" class="meta">Average per day at ~{average:.2f}</text>
  <g>{''.join(cells)}</g>
</svg>
'''
    write(ASSETS / "metrics.isocalendar.svg", svg)


def main() -> None:
    payload = read_payload()
    render_isocalendar(payload)
    render_stats(payload, "dark", dark=True)
    render_stats(payload, "light", dark=False)
    render_languages()


if __name__ == "__main__":
    main()
