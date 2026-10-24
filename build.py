"""Builds index.html (the dev hub) from template.html + projects.json + footer.html.

Run:  python3 build.py
GitHub Pages serves the repo root, so the page lands at ./index.html as static HTML that
link-preview crawlers and search engines can read. The activity dashboard lives at activity/.
"""
import html
import json
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "projects.json")))
tpl = open(os.path.join(HERE, "template.html")).read()
FOOTER = open(os.path.join(HERE, "footer.html")).read()
e = html.escape

ICONS = {
    "android": ("Android", '<path fill="currentColor" d="M5.2 2.1a.4.4 0 01.55.13l.7 1.12A5 5 0 018 3.1c.55 0 1.07.09 1.55.25l.7-1.12a.4.4 0 11.68.42l-.66 1.06A4.4 4.4 0 0112.5 7H3.5a4.4 4.4 0 012.23-3.29l-.66-1.06a.4.4 0 01.13-.55zM6 5.4a.55.55 0 100 1.1.55.55 0 000-1.1zm4 0a.55.55 0 100 1.1.55.55 0 000-1.1zM3.5 8h9v4.5a1 1 0 01-1 1h-7a1 1 0 01-1-1V8z"/>'),
    "mac": ("macOS", '<g fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"><rect x="3" y="3.5" width="10" height="7" rx="1"/><path d="M1.5 12.5h13"/></g>'),
    "chrome": ("Chrome extension", '<g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="2.3"/><path d="M8 5.7h5.6M6 9.2L3.2 4.3M10 9.2l-2.8 4.8"/></g>'),
    "term": ("Command line", '<g fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="1.8" y="2.8" width="12.4" height="10.4" rx="1.6"/><path d="M4.6 6.2l2 1.8-2 1.8M8.4 10.2h3"/></g>'),
    "web": ("Web", '<g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="6"/><path d="M2 8h12M8 2c1.7 1.8 2.5 3.8 2.5 6S9.7 12.2 8 14M8 2C6.3 3.8 5.5 5.8 5.5 8s.8 4.2 2.5 6"/></g>'),
}


def plats(ps):
    return "".join(
        f'<svg class="pi pi-{k}" viewBox="0 0 16 16" role="img" aria-label="{ICONS[k][0]}"><title>{ICONS[k][0]}</title>{ICONS[k][1]}</svg>'
        for k in ps if k in ICONS)


def card(p):
    art = f'<div class="art"><img src="/thumbs/{e(p["thumb"])}" alt="{e(p["name"])}" loading="lazy" width="800" height="420"></div>'
    if p.get("years"):
        art = art.replace('">', f'"><span class="yrs" title="Active years, from the project\'s commit history">{e(p["years"])}</span>', 1)
    parts = ""
    if p.get("parts"):
        items = "".join(f'<li>{e(x["name"])}<span><i class="k">{e(x["kind"])} · </i><code>{e(x["repo"])}</code></span></li>' for x in p["parts"])
        names = ", ".join(x["name"] for x in p["parts"])
        parts = (f'<button class="parts" type="button" aria-label="{len(p["parts"])} parts: {e(names)}">'
                 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></svg>'
                 f'{len(p["parts"])} parts</button><div class="pop" role="tooltip"><b>Built from</b><ul>{items}</ul></div>')
    link = ""
    if p.get("url"):
        ext = "" if p["url"].startswith("/") else ' target="_blank" rel="noopener"'
        link = f'<a class="open" href="{e(p["url"])}"{ext}>{e(p.get("urlLabel", "Open"))}</a>'
    role = f'<span class="role {p["role"]}">{data["roles"][p["role"]]}</span>' if p.get("role") else ""
    return (f'<article class="card">{art}<div class="cbody"><div class="ctop"><h3>{e(p["name"])}</h3>{role}</div>'
            f'<p>{e(p["desc"])}</p><div class="cfoot"><span class="plats">{plats(p["plat"])}</span>'
            f'{parts}{link}</div></div></article>')


def head(g):
    # rule 27: context only, never a count of the work
    return (f'<div class="ghead"><div><h2>{e(g["title"])}</h2><p>{e(g["lede"])}</p></div>'
            f'<div class="ctx">{e(g["context"])}</div></div>')


MAX_ROW = 5  # cards side by side at desktop width
# Pack consecutive groups into as few rows as possible with counts as even as possible (rules 3, 25).
sizes = [len(g["projects"]) for g in data["groups"]]
best = None
for k in range(1, len(sizes) + 1):
    for cuts in combinations(range(1, len(sizes)), k - 1):
        bounds = [0, *cuts, len(sizes)]
        rs = [sizes[a:b] for a, b in zip(bounds, bounds[1:])]
        if any(sum(r) > MAX_ROW and len(r) > 1 for r in rs):
            continue
        score = max(sum(r) for r in rs) - min(sum(r) for r in rs)
        if best is None or score < best[0]:
            best = (score, bounds)
    if best:
        break
bounds = best[1]
rows = [data["groups"][a:b] for a, b in zip(bounds, bounds[1:])]

groups = []
for i, row in enumerate(rows):
    last = i == len(rows) - 1
    cls = "group" + (" last" if last else "")
    if len(row) == 1:
        g = row[0]
        body = f'    {head(g)}\n    <div class="cards" style="--n:{len(g["projects"])}">{"".join(card(p) for p in g["projects"])}</div>\n'
        groups.append(f'  <section class="{cls} solo" id="{g["id"]}"><div class="wrap">\n{body}  </div>\n{FOOTER if last else ""}  </section>')
    else:
        cols = " ".join(f"{len(g['projects'])}fr" for g in row)
        subs = "".join(
            f'<div class="subgroup" id="{g["id"]}" style="--n:{len(g["projects"])}">{head(g)}'
            f'<div class="cards">{"".join(card(p) for p in g["projects"])}</div></div>' for g in row)
        groups.append(f'  <section class="{cls} row-group"><div class="wrap"><div class="row" style="grid-template-columns:{cols}">{subs}</div></div>\n{FOOTER if last else ""}  </section>')

NAV = {"extensions": "Extensions", "tools": "Mac & MCP", "network": "Network", "activity": "Activity"}
nav = "".join(f'<a href="#{g["id"]}">{NAV.get(g["id"], g["title"])}</a>' for g in data["groups"])

desc = ("Developer tools by Sankha Cooray: Chrome extensions, a Claude usage meter, Shotlink and MCP servers, "
        "plus the shared plumbing behind sankhacooray.com.")
assert 120 <= len(desc) <= 160, len(desc)

out = tpl.replace("{{GROUPS}}", "\n".join(groups)).replace("{{NAV}}", nav).replace("{{DESC}}", e(desc))
open(os.path.join(HERE, "index.html"), "w").write(out)
print("built index.html:", " | ".join("+".join(g["id"] for g in r) for r in rows))
