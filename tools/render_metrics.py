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

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="230" viewBox="0 0 760 230" role="img" aria-label="GitHub statistics for Nitin3560">
  <style>
    .panel {{ fill: {bg}; stroke: {border}; stroke-width: 1.4; }}
    .name {{ fill: #39d353; font: 800 22px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .tag {{ fill: {muted}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .num {{ fill: {text}; font: 800 32px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: {muted}; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .rule {{ stroke: {line}; stroke-width: 1; }}
    .pill {{ fill: #10281b; stroke: #238636; stroke-width: 1; }}
    .pill-text {{ fill: #39d353; font: 800 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <rect x="1" y="1" width="758" height="228" rx="8" class="panel"/>
  <text x="32" y="46" class="name">Nitin3560</text>
  <text x="680" y="46" text-anchor="end" class="tag">at a glance</text>
  <line x1="32" y1="68" x2="728" y2="68" class="rule"/>
  <text x="42" y="116" class="num">4</text>
  <text x="42" y="139" class="label">Selected projects</text>
  <text x="208" y="116" class="num">{total:,}</text>
  <text x="208" y="139" class="label">Contributions (1y)</text>
  <text x="438" y="116" class="num">{longest}</text>
  <text x="438" y="139" class="label">Longest streak</text>
  <text x="608" y="116" class="num">{current}</text>
  <text x="608" y="139" class="label">Current streak</text>
  <rect x="42" y="172" width="170" height="31" rx="15" class="pill"/>
  <text x="127" y="192" text-anchor="middle" class="pill-text">MS CS @ UTA</text>
  <rect x="232" y="172" width="170" height="31" rx="15" class="pill"/>
  <text x="317" y="192" text-anchor="middle" class="pill-text">IEEE CSCN 2026</text>
  <rect x="422" y="172" width="220" height="31" rx="15" class="pill"/>
  <text x="532" y="192" text-anchor="middle" class="pill-text">Autonomy + Backend</text>
</svg>
'''
    write(ASSETS / f"card-stats-{suffix}.svg", svg)


def render_languages() -> None:
    width, height = 760, 142
    x = 32
    bars = []
    labels = []
    for index, (name, pct, color) in enumerate(LANGUAGES):
        bar_width = int(696 * pct / 100)
        bars.append(f'<rect x="{x}" y="54" width="{bar_width}" height="16" fill="{color}"/>')
        col = index % 3
        row = index // 3
        label_x = 40 + col * 230
        label_y = 102 + row * 24
        labels.append(
            f'<circle cx="{label_x}" cy="{label_y}" r="5" fill="{color}"/>'
            f'<text x="{label_x + 16}" y="{label_y + 5}" class="label">{html.escape(name)} {pct}%</text>'
        )
        x += bar_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Most used languages">
  <style>
    .title {{ fill: #39d353; font: 800 20px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .label {{ fill: #c9d1d9; font: 700 13px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .bar-bg {{ fill: #161b22; }}
  </style>
  <text x="32" y="31" class="title">core languages</text>
  <rect x="32" y="54" width="696" height="16" rx="4" class="bar-bg"/>
  <g>{''.join(bars)}</g>
  <g>{''.join(labels)}</g>
</svg>
'''
    write(ASSETS / "metrics.languages.svg", svg)


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

    average = total / max(1, len(days))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="930" height="430" viewBox="0 0 930 430" role="img" aria-label="3D isometric contribution calendar for Nitin3560">
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
