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
        [
            "Full-stack job discovery and matching platform",
            "with scalable ingestion and optimized retrieval.",
        ],
        "Python",
        "#3572A5",
        "0",
        "0",
    ),
    (
        "TwinGuard",
        [
            "Autonomy assurance for UAV swarms: trust-gated",
            "control, behavior-tree supervision, and Nav2.",
        ],
        "C++",
        "#f34b7d",
        "1",
        "0",
    ),
    (
        "UAV Autonomy Research Suite",
        [
            "Fault-tolerant supervisory control for autonomous",
            "UAV swarms with CTDE-MAPPO and fault injection.",
        ],
        "Python",
        "#3572A5",
        "1",
        "0",
    ),
    (
        "YoMeets",
        [
            "Real-time AI meeting assistant that tracks actions,",
            "decisions, memory, and approved follow-ups.",
        ],
        "TypeScript",
        "#3178c6",
        "0",
        "0",
    ),
]

SKILLS = [
    ("C++", 92, ""),
    ("Python", 90, ""),
    ("Backend", 88, ""),
    ("DSA", 82, ""),
    ("Robotics", 78, ""),
    ("ML/RL", 74, ""),
    ("Databases", 80, ""),
    ("Systems", 86, ""),
]

LANGS = [
    ("Python", 100, "2.10 MB"),
    ("C++", 60, "1.25 MB"),
    ("Java", 29.1, "612 kB"),
    ("TypeScript", 19.5, "410 kB"),
    ("JavaScript", 11.0, "230 kB"),
    ("Shell", 4.6, "96 kB"),
    ("CMake", 2.4, "51 kB"),
    ("HTML", 1.1, "24 kB"),
]


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def project_card(name: str, description: list[str], language: str, color: str, stars: str, forks: str) -> str:
    width, height = 520, 162
    desc_nodes = "\n".join(
        f'  <text x="40" y="{72 + index * 22}" class="desc">{html.escape(line)}</text>'
        for index, line in enumerate(description)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(name)} project card">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
  </defs>
  <style>
    .panel {{ fill: url(#bg); stroke: #30363d; stroke-width: 1.2; }}
    .repo {{ fill: #8b949e; }}
    .title {{ fill: #39d353; font: 800 18px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .desc {{ fill: #e6edf3; font: 600 14px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .meta {{ fill: #8b949e; font: 600 13px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .lang-dot {{ fill: {color}; }}
    .muted {{ fill: #8b949e; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="panel"/>
  <path class="repo" d="M40 28h12a4 4 0 0 1 4 4v16l-6-3-6 3-6-3-6 3V32a4 4 0 0 1 4-4z"/>
  <text x="66" y="44" class="title">{html.escape(name)}</text>
{desc_nodes}
  <circle cx="40" cy="128" r="6" class="lang-dot"/>
  <text x="58" y="133" class="meta">{html.escape(language)}</text>
  <path class="muted" d="M206 121l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1z"/>
  <text x="230" y="133" class="meta">{html.escape(stars)}</text>
  <path class="muted" d="M286 121a4 4 0 1 0-4 4v8a8 8 0 0 0 8 8h6a4 4 0 1 0 0-4h-6a4 4 0 0 1-4-4v-8a4 4 0 0 0 0-4zm18 16a4 4 0 1 0 4 4 4 4 0 0 0-4-4z"/>
  <text x="316" y="133" class="meta">{html.escape(forks)}</text>
</svg>
'''


def radar_card(filename: str, title: str, rows: list[tuple[str, float, str]], *, show_values: bool = False) -> None:
    width, height = 520, 430
    center_x, center_y = 260, 226
    max_radius = 138
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

    for index, (label, value, detail) in enumerate(rows):
        angle = -math.pi / 2 + index * 2 * math.pi / len(rows)
        x = center_x + math.cos(angle) * max_radius
        y = center_y + math.sin(angle) * max_radius
        lx = center_x + math.cos(angle) * (max_radius + 48)
        ly = center_y + math.sin(angle) * (max_radius + 34)
        anchor = "middle"
        if math.cos(angle) > 0.35:
            anchor = "start"
        elif math.cos(angle) < -0.35:
            anchor = "end"
        points.append(f"{center_x + math.cos(angle) * max_radius * value / 100:.1f},{center_y + math.sin(angle) * max_radius * value / 100:.1f}")
        axes.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x:.1f}" y2="{y:.1f}" class="axis"/>')
        axes.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="label">{html.escape(label)}</text>')
        if show_values:
            axes.append(f'<text x="{lx:.1f}" y="{ly + 17:.1f}" text-anchor="{anchor}" class="value">{html.escape(detail)}</text>')

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
    .title {{ fill: #e6edf3; font: 800 15px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .ring {{ fill: none; stroke: #30363d; stroke-width: 1; }}
    .axis {{ stroke: #30363d; stroke-width: 0.9; }}
    .shape {{ fill: rgba(57, 211, 83, 0.26); stroke: #39d353; stroke-width: 2.4; }}
    .point {{ fill: #57e36d; }}
    .label {{ fill: #c9d1d9; font: 800 12px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .value {{ fill: #8b949e; font: 600 10px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; }}
    .center {{ fill: #39d353; opacity: 0.85; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="0" class="panel"/>
  <text x="{center_x}" y="44" text-anchor="middle" class="title">{html.escape(title)}</text>
  <g>{''.join(rings)}{''.join(axes)}</g>
  <polygon points="{' '.join(points)}" class="shape"/>
  <g>{''.join(f'<circle cx="{point.split(",")[0]}" cy="{point.split(",")[1]}" r="3.8" class="point"/>' for point in points)}</g>
  <circle cx="{center_x}" cy="{center_y}" r="3.5" class="center"/>
</svg>
'''
    write(ASSETS / filename, svg)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for project in PROJECTS:
        slug = project[0].lower().replace(" ", "-")
        write(ASSETS / f"card-{slug}.svg", project_card(*project))
    radar_card("radar-skills.svg", "Skill Radar", SKILLS)
    radar_card("radar-langs.svg", "Nitin3560 - language mix", LANGS, show_values=True)


if __name__ == "__main__":
    main()
