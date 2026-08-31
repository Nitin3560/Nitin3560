#!/usr/bin/env python3
"""Render local README cards used by the GitHub profile."""

from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

PROJECTS = [
    (
        "CareerOS",
        "Job matching and retrieval platform",
        "FastAPI / Postgres / Redis / Python",
        "Async ingestion, normalized jobs, cached matching",
    ),
    (
        "TwinGuard",
        "Autonomy assurance for UAV swarms",
        "C++17 / ROS 2 / PX4 / Gazebo",
        "Trust-gated control, planning, supervision",
    ),
    (
        "UAV Autonomy Research Suite",
        "Fault-aware control and multi-agent RL",
        "Python / RLlib / Docker / ROS 2",
        "30-seed fault injection and evaluation",
    ),
    (
        "YoMeets",
        "Real-time AI meeting assistant",
        "TypeScript / Postgres / pgvector",
        "Live actions, decisions, memory, follow-ups",
    ),
]

SKILLS = [
    ("Backend", 92),
    ("C++", 88),
    ("Python", 94),
    ("Autonomy", 90),
    ("Robotics", 84),
    ("ML/RL", 82),
]

LANGS = [
    ("Python", 95),
    ("C++", 88),
    ("Java", 76),
    ("TypeScript", 70),
    ("Shell", 62),
    ("SQL", 78),
]


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def project_card(name: str, focus: str, stack: str, detail: str) -> str:
    width, height = 420, 178
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(name)} project card">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="58%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#0f1f1d"/>
    </linearGradient>
  </defs>
  <style>
    .panel {{ fill: url(#bg); stroke: #30363d; stroke-width: 1.2; }}
    .title {{ fill: #39d353; font: 700 22px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .focus {{ fill: #e6edf3; font: 700 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .detail {{ fill: #8b949e; font: 600 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .stack {{ fill: #39d353; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .dot {{ fill: #39d353; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="panel"/>
  <circle cx="28" cy="30" r="5" class="dot"/>
  <text x="44" y="37" class="title">{html.escape(name)}</text>
  <text x="28" y="75" class="focus">{html.escape(focus)}</text>
  <text x="28" y="105" class="detail">{html.escape(detail)}</text>
  <text x="28" y="144" class="stack">{html.escape(stack)}</text>
</svg>
'''


def radar_card(filename: str, title: str, rows: list[tuple[str, int]]) -> None:
    width, height = 420, 320
    center_x, center_y = 210, 196
    max_radius = 74
    points = []
    axes = []
    rings = []

    for level in range(1, 5):
        radius = max_radius * level / 4
        ring_points = []
        for index in range(len(rows)):
            angle = -math.pi / 2 + index * 2 * math.pi / len(rows)
            ring_points.append(f"{center_x + math.cos(angle) * radius:.1f},{center_y + math.sin(angle) * radius:.1f}")
        rings.append(f'<polygon points="{" ".join(ring_points)}" class="ring"/>')

    for index, (label, value) in enumerate(rows):
        angle = -math.pi / 2 + index * 2 * math.pi / len(rows)
        x = center_x + math.cos(angle) * max_radius
        y = center_y + math.sin(angle) * max_radius
        lx = center_x + math.cos(angle) * (max_radius + 42)
        ly = center_y + math.sin(angle) * (max_radius + 30)
        points.append(f"{center_x + math.cos(angle) * max_radius * value / 100:.1f},{center_y + math.sin(angle) * max_radius * value / 100:.1f}")
        axes.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x:.1f}" y2="{y:.1f}" class="axis"/>')
        axes.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" class="label">{html.escape(label)}</text>')

    short_title = title.removeprefix("cat ").removesuffix(".json")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="62%" stop-color="#08111f"/>
      <stop offset="100%" stop-color="#0d1f18"/>
    </linearGradient>
  </defs>
  <style>
    .panel {{ fill: url(#bg); stroke: #30363d; stroke-width: 1.2; }}
    .title {{ fill: #39d353; font: 800 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .sub {{ fill: #8b949e; font: 700 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .ring {{ fill: none; stroke: #30363d; stroke-width: 1; }}
    .axis {{ stroke: #30363d; stroke-width: 0.9; }}
    .shape {{ fill: rgba(57, 211, 83, 0.24); stroke: #39d353; stroke-width: 2.4; }}
    .label {{ fill: #c9d1d9; font: 800 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .center {{ fill: #39d353; opacity: 0.85; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="panel"/>
  <text x="26" y="40" class="title">~/ {html.escape(short_title)}</text>
  <text x="26" y="60" class="sub">self-rated operating range</text>
  <g>{''.join(rings)}{''.join(axes)}</g>
  <polygon points="{' '.join(points)}" class="shape"/>
  <circle cx="{center_x}" cy="{center_y}" r="3.5" class="center"/>
</svg>
'''
    write(ASSETS / filename, svg)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for project in PROJECTS:
        slug = project[0].lower().replace(" ", "-")
        write(ASSETS / f"card-{slug}.svg", project_card(*project))
    radar_card("radar-skills.svg", "cat skill-radar.json", SKILLS)
    radar_card("radar-langs.svg", "cat language-radar.json", LANGS)


if __name__ == "__main__":
    main()
