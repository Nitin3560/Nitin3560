#!/usr/bin/env python3
"""Render a self-drawing ASCII identity portrait."""

from __future__ import annotations

import html
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "portrait.svg"

ART = [
    "                  ..::--==++**##%%@@",
    "             .:-=+*#%%%%%%%%%%%%%%%%%",
    "          .:=*%%%%%#*+=--::..        ",
    "        .=#%%%%*-.                  ",
    "       :#%%%%+.     N I T I N       ",
    "      -%%%%#:       S I N G H       ",
    "     .%%%%%:        R A T H O R E   ",
    "     +%%%%+                         ",
    "     %%%%%.    software engineer    ",
    "     %%%%%.    backend systems      ",
    "     +%%%%+    APIs databases CI    ",
    "     .%%%%%:                        ",
    "      -%%%%#:        C++ PYTHON JAVA",
    "       :#%%%%+.      FASTAPI REDIS  ",
    "        .=#%%%%*-.                  ",
    "          .:=*%%%%%#*+=--::..      ",
    "             .:-=+*#%%%%%%%%%%%%%%%%",
    "                  ..::--==++**##%%@@",
]


def main() -> None:
    preview = os.getenv("PREVIEW") == "1"
    width, height = 420, 420
    x, y0, line_height = 24, 58, 18
    text_nodes = []
    clip_defs = []

    for index, row in enumerate(ART):
        y = y0 + index * line_height
        clip_id = f"line-{index}"
        delay = 0 if preview else index * 0.045
        clip_width = width - 48
        clip_defs.append(
            f'''<clipPath id="{clip_id}">
      <rect x="{x}" y="{y - 15}" width="{clip_width if preview else 0}" height="{line_height}">
        <animate attributeName="width" from="0" to="{clip_width}" begin="{delay:.3f}s" dur="0.5s" fill="freeze"/>
      </rect>
    </clipPath>'''
        )
        text_nodes.append(
            f'''<text x="{x}" y="{y}" clip-path="url(#{clip_id})">{html.escape(row)}</text>'''
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII identity portrait for Nitin Singh Rathore">
  <defs>
    <radialGradient id="scan" cx="50%" cy="18%" r="80%">
      <stop offset="0%" stop-color="#123f48"/>
      <stop offset="54%" stop-color="#08111f"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
    {''.join(clip_defs)}
  </defs>
  <style>
    .shell {{ fill: url(#scan); stroke: #38bdf8; stroke-width: 1.2; }}
    .label {{ fill: #7dd3fc; font: 700 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    text {{ fill: #5eead4; font: 700 13.5px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 0; }}
    .dim {{ fill: #64748b; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" class="shell"/>
  <text x="24" y="30" class="label">$ ./draw_identity --ascii</text>
  <g>{''.join(text_nodes)}</g>
  <text x="24" y="392" class="dim">render: local svg | motion: smil | badges: none</text>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
