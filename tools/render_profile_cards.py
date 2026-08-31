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
        "Job discovery, matching, ingestion, retrieval",
        "FastAPI / PostgreSQL / Redis / Python",
        "3,000+ normalized postings, cached matching, async workers",
    ),
    (
        "TwinGuard",
        "Autonomy assurance for UAV swarms",
        "C++17 / ROS 2 / PX4 / Gazebo",
        "Trust-gated control, planning, supervision, CI validation",
    ),
    (
        "UAV Autonomy Research Suite",
        "Fault-aware supervisory control and multi-agent RL",
        "Python / RLlib / Docker / ROS 2",
        "30-seed fault injection across wind, sensors, and comms",
    ),
    (
        "Traceback AI",
        "Root-cause analysis for distributed microservices",
        "FastAPI / Graphs / Anomaly Detection",
        "Telemetry ranking surfaced causes in top-3 for 87% of cases",
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
    .focus {{ fill: #e6edf3; font: 600 14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .detail {{ fill: #8b949e; font: 500 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .stack {{ fill: #58a6ff; font: 700 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
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
    width = height = 400
    center = 200
    max_radius = 128
    points = []
    axes = []
    rings = []

    for level in range(1, 5):
        radius = max_radius * level / 4
        ring_points = []
        for index in range(len(rows)):
            angle = -math.pi / 2 + index * 2 * math.pi / len(rows)
            ring_points.append(f"{center + math.cos(angle) * radius:.1f},{center + math.sin(angle) * radius:.1f}")
        rings.append(f'<polygon points="{" ".join(ring_points)}" class="ring"/>')

    for index, (label, value) in enumerate(rows):
        angle = -math.pi / 2 + index * 2 * math.pi / len(rows)
        x = center + math.cos(angle) * max_radius
        y = center + math.sin(angle) * max_radius
        lx = center + math.cos(angle) * (max_radius + 34)
        ly = center + math.sin(angle) * (max_radius + 28)
        points.append(f"{center + math.cos(angle) * max_radius * value / 100:.1f},{center + math.sin(angle) * max_radius * value / 100:.1f}")
        axes.append(f'<line x1="{center}" y1="{center}" x2="{x:.1f}" y2="{y:.1f}" class="axis"/>')
        axes.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" class="label">{html.escape(label)}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#0f1f1d"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
  </defs>
  <style>
    .panel {{ fill: url(#bg); stroke: #30363d; stroke-width: 1.2; }}
    .title {{ fill: #39d353; font: 700 17px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .ring {{ fill: none; stroke: #30363d; stroke-width: 1; }}
    .axis {{ stroke: #30363d; stroke-width: 1; }}
    .shape {{ fill: rgba(57, 211, 83, 0.22); stroke: #39d353; stroke-width: 2; }}
    .label {{ fill: #c9d1d9; font: 700 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="panel"/>
  <text x="24" y="34" class="title">$ {html.escape(title)}</text>
  <g>{''.join(rings)}{''.join(axes)}</g>
  <polygon points="{' '.join(points)}" class="shape"/>
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
