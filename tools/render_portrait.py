#!/usr/bin/env python3
"""Render the README hero portrait from the GitHub profile photo."""

from __future__ import annotations

import colorsys
import io
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

USERNAME = "Nitin3560"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "portrait.svg"
AVATAR_URL = f"https://github.com/{USERNAME}.png?size=640"


def fetch_avatar() -> Image.Image:
    local_source = os.getenv("PORTRAIT_SOURCE")
    if local_source:
        return Image.open(local_source).convert("RGB")

    request = urllib.request.Request(
        AVATAR_URL,
        headers={"User-Agent": f"{USERNAME}-profile-portrait-renderer"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    return Image.open(io.BytesIO(payload)).convert("RGB")


def color_for(pixel: tuple[int, int, int]) -> str:
    r, g, b = pixel
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    s = min(1.0, s * 1.18 + 0.06)
    v = min(1.0, max(0.14, v * 0.95))
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r2 * 255):02x}{int(g2 * 255):02x}{int(b2 * 255):02x}"


def main() -> None:
    source = ImageOps.fit(fetch_avatar(), (360, 360), method=Image.Resampling.LANCZOS)
    source = source.filter(ImageFilter.SHARPEN)

    width, height = 420, 390
    dot_step = 6
    dot_radius = 2.05
    offset_x, offset_y = 30, 6
    center_x, center_y = 210, 182
    radius_x, radius_y = 178, 174
    dots: list[str] = []

    for y in range(0, 360, dot_step):
        for x in range(0, 360, dot_step):
            px = offset_x + x
            py = offset_y + y
            nx = (px - center_x) / radius_x
            ny = (py - center_y) / radius_y
            dist = nx * nx + ny * ny
            if dist > 1.0:
                continue

            fade = max(0.0, min(1.0, (1.0 - dist) * 2.2))
            if fade < 0.24:
                continue

            color = color_for(source.getpixel((x, y)))
            opacity = 0.46 + fade * 0.54
            dots.append(
                f'<circle cx="{px}" cy="{py}" r="{dot_radius:.2f}" fill="{color}" opacity="{opacity:.2f}"/>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Dot matrix profile portrait for Nitin Singh Rathore">
  <defs>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="portraitClip">
      <ellipse cx="{center_x}" cy="{center_y}" rx="{radius_x}" ry="{radius_y}"/>
    </clipPath>
  </defs>
  <g filter="url(#softGlow)">
    {''.join(dots)}
  </g>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(dots)} dots")


if __name__ == "__main__":
    main()
