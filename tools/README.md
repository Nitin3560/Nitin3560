# Profile Asset Tools

This directory contains the small scripts used to refresh the generated SVG assets in the profile README.

## Setup

Install the script dependencies from the repository root:

```bash
python3 -m pip install -r tools/requirements-daily.txt
```

## Regenerate Assets

Fetch the latest public GitHub contribution data:

```bash
python3 tools/pull_contributions.py
```

Regenerate the profile graphics:

```bash
python3 tools/render_metrics.py
python3 tools/render_graph.py
python3 tools/render_profile_cards.py
python3 tools/render_portrait.py
```

`render_portrait.py` uses the GitHub profile photo by default. To render from a local image instead, set `PORTRAIT_SOURCE` to the image path before running the script.
