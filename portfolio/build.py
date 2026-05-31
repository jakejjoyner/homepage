#!/usr/bin/env python3
"""Build ~/homepage/portfolio/index.html from projects.json + template.

Idempotent — safe to run any time. Ordered by `shipped` descending (newest first).

Usage:
  build.py           # rebuild
  build.py --check   # validate projects.json + report; don't write
"""
from __future__ import annotations
import argparse
import json
import sys
import html
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "projects.json"
INDEX = ROOT / "index.html"

STATUS_COLORS = {
    "alpha":    "#d29922",  # amber
    "beta":     "#58a6ff",  # blue
    "stable":   "#3fb950",  # green
    "archived": "#8b949e",  # muted
    "experiment": "#bc8cff",  # purple
}

PAGE_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="/theme.css" />
  <link rel="stylesheet" href="portfolio.css" />
  <script src="/theme.js" defer></script>
  <style>
    .page-note {{ color: var(--muted); font-size: 0.85rem; margin-top: 0.5rem; }}
    .chapters {{ margin-top: 2.5rem; }}
    .chapters h2 {{ font-size: 1.1rem; font-weight: 600; color: var(--heading); margin-bottom: 0.3rem; }}
    .chapters .chapters-sub {{ color: var(--muted); font-size: 0.85rem; margin-bottom: 0.8rem; }}
    .chapters ul {{ list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }}
    .chapters li {{ color: var(--muted); font-size: 0.9rem; }}
    .chapters a {{ color: var(--link); text-decoration: none; font-weight: 600; }}
    .chapters a:hover {{ color: var(--heading); }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{title}</h1>
      <p class="subtitle">{subtitle}</p>
      <p class="page-note">Mostly a record for myself. It's public in case anyone's genuinely interested, not to brag.</p>
    </header>
    <section class="projects">
{cards}
    </section>
    <section class="chapters">
      <h2>Chapters</h2>
      <p class="chapters-sub">Things I did before code.</p>
      <ul>
        <li><a href="/portfolio/drones/">FPV</a> — six years of racing, freestyle, and builds (ages 11-17)</li>
        <li><a href="/portfolio/guitar/">Guitar</a> — violin, School of Rock AllStars, LA venues</li>
      </ul>
    </section>
    <footer>
      <p class="footer-text">{footer}</p>
      <p class="footer-text"><a href="/">← jakejoyner.com</a></p>
    </footer>
  </main>
</body>
</html>
"""

CARD_TPL = """      <article class="project" data-status="{status}">
        <div class="project-head">
          <h2 class="project-title">{title}</h2>
          <span class="project-status" style="--status-color: {status_color};">{status}</span>
        </div>
        <p class="project-tagline">{tagline}</p>
        <p class="project-desc">{description}</p>
        <div class="project-stack">{stack_tags}</div>
        <div class="project-links">{links}</div>
        <div class="project-meta">shipped {shipped} · updated {updated}</div>
      </article>
"""


def render_card(p: dict) -> str:
    status = p.get("status", "alpha")
    status_color = STATUS_COLORS.get(status, "#8b949e")
    stack = p.get("stack", []) or []
    stack_tags = "".join(
        f'<span class="stack-tag">{html.escape(t)}</span>' for t in stack
    )
    links = "".join(
        f'<a class="project-link" href="{html.escape(l["href"])}" target="_blank" rel="noopener noreferrer">{html.escape(l["label"])}</a>'
        for l in (p.get("links") or [])
    )
    return CARD_TPL.format(
        title=html.escape(p.get("title", "(untitled)")),
        status=html.escape(status),
        status_color=status_color,
        tagline=html.escape(p.get("tagline", "")),
        description=html.escape(p.get("description", "")),
        stack_tags=stack_tags,
        links=links,
        shipped=html.escape(p.get("shipped", "")),
        updated=html.escape(p.get("updated", "")),
    )


def validate(data: dict) -> list[str]:
    errs = []
    if "projects" not in data:
        errs.append("missing 'projects' key")
        return errs
    seen_ids = set()
    for i, p in enumerate(data["projects"]):
        if "id" not in p:
            errs.append(f"project[{i}]: missing id")
            continue
        if p["id"] in seen_ids:
            errs.append(f"project[{i}]: duplicate id {p['id']!r}")
        seen_ids.add(p["id"])
        for required in ("title", "tagline", "status"):
            if required not in p:
                errs.append(f"project {p['id']}: missing {required}")
        for l in p.get("links", []):
            if "label" not in l or "href" not in l:
                errs.append(f"project {p['id']}: malformed link {l}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not PROJECTS.exists():
        print(f"ERROR: {PROJECTS} not found", file=sys.stderr)
        return 1

    data = json.loads(PROJECTS.read_text())
    errs = validate(data)
    if errs:
        for e in errs:
            print(f"  ✗ {e}", file=sys.stderr)
        return 2
    print(f"  ✓ projects.json valid ({len(data.get('projects', []))} projects)")

    if args.check:
        return 0

    # Sort by `shipped` desc, then `updated` desc, then id
    projects = sorted(
        data["projects"],
        key=lambda p: (p.get("shipped", ""), p.get("updated", ""), p.get("id", "")),
        reverse=True,
    )
    cards = "\n".join(render_card(p) for p in projects)
    site = data.get("site", {})
    out = PAGE_TPL.format(
        title=html.escape(site.get("title", "Portfolio")),
        subtitle=html.escape(site.get("subtitle", "")),
        footer=html.escape(site.get("footer_text", "")),
        cards=cards,
    )
    INDEX.write_text(out)
    print(f"  ✓ wrote {INDEX} ({len(out)} bytes)")

    # Also refresh llms.txt for agent consumers
    import subprocess
    subprocess.run([str(ROOT / "build-llms.py")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
