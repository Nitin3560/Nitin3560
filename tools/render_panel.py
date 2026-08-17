#!/usr/bin/env python3
"""Render the terminal-style profile information panel."""

from __future__ import annotations

import html
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sysinfo.svg"

ROWS = [
    ("name", "Nitin Singh Rathore"),
    ("role", "MS CS @ UT Arlington | GTA"),
    ("focus", "Backend systems and APIs"),
    ("stack", "C++ | Python | Java | FastAPI"),
    ("data", "PostgreSQL | Redis | RQ"),
    ("systems", "Linux | Docker | GitHub Actions"),
    ("now", "Seeking Fall 2026 SWE roles"),
    ("plus", "Robotics | autonomy | ML"),
]


def main() -> None:
    preview = os.getenv("PREVIEW") == "1"
    width, height = 520, 344
    lines = []
    for index, (key, value) in enumerate(ROWS):
        y = 92 + index * 32
        delay = 0 if preview else 0.25 + index * 0.12
        lines.append(
            f'''
  <g opacity="{1 if preview else 0}">
    <animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.24s" fill="freeze"/>
    <text x="34" y="{y}" class="key">{html.escape(key)}</text>
    <text x="150" y="{y}" class="value">{html.escape(value)}</text>
  </g>'''
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Terminal profile summary for Nitin Singh Rathore">
  <defs>
    <linearGradient id="panel" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#08111f"/>
      <stop offset="52%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#0c1f25"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    .frame {{ fill: url(#panel); stroke: #2dd4bf; stroke-width: 1.4; }}
    .bar {{ fill: #101827; }}
    .dot-red {{ fill: #ff6b6b; }}
    .dot-yellow {{ fill: #ffd166; }}
    .dot-green {{ fill: #5eead4; }}
    .prompt {{ fill: #7dd3fc; font: 700 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .key {{ fill: #5eead4; font: 700 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .value {{ fill: #e5f4ff; font: 500 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .cursor {{ fill: #f8fafc; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="frame"/>
  <rect x="2" y="2" width="{width - 4}" height="46" rx="8" class="bar"/>
  <circle cx="24" cy="24" r="6" class="dot-red"/>
  <circle cx="44" cy="24" r="6" class="dot-yellow"/>
  <circle cx="64" cy="24" r="6" class="dot-green"/>
  <text x="90" y="30" class="prompt">$ whoami --verbose</text>
  <text x="34" y="66" class="prompt" filter="url(#glow)">profile://Nitin3560</text>
  {''.join(lines)}
  <rect x="34" y="316" width="9" height="18" class="cursor">
    <animate attributeName="opacity" values="1;1;0;0;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
