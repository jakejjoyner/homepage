#!/usr/bin/env python3
"""Generate /portfolio/llms.txt from projects.json. Runs as part of build.py."""
import json
from pathlib import Path

P = Path("/home/jjoyner/homepage/portfolio")
data = json.loads((P / "projects.json").read_text())

lines = ["# Jake Joyner — Projects", ""]
site = data.get("site", {})
if site.get("subtitle"):
    lines.append(f"> {site['subtitle']}")
    lines.append("")

for p in sorted(data["projects"], key=lambda p: (p.get("shipped",""), p.get("id","")), reverse=True):
    lines.append(f"## {p['title']} ({p.get('status','?')})")
    lines.append(f"")
    lines.append(p.get("tagline", ""))
    lines.append("")
    if p.get("description"):
        lines.append(p["description"])
        lines.append("")
    if p.get("stack"):
        lines.append(f"**Stack:** {', '.join(p['stack'])}")
        lines.append("")
    if p.get("links"):
        lines.append("**Links:**")
        for l in p["links"]:
            lines.append(f"- {l['label']}: {l['href']}")
        lines.append("")
    lines.append(f"_shipped {p.get('shipped','?')} · updated {p.get('updated','?')}_")
    lines.append("")
    lines.append("---")
    lines.append("")

(P / "llms.txt").write_text("\n".join(lines))
print(f"  ✓ wrote {P / 'llms.txt'}")
