# dev.sankhacooray.com

A live, three-lens view of what I'm making right now. All data comes from the GitHub GraphQL API via a small Apps Script proxy ([dev-sankhacooray-com-proxy](https://github.com/sankhacooray/dev-sankhacooray-com-proxy)) that caches for 1h.

## The three views

- **Lab** — tiled grid of every `*.sankhacooray.com` sub-site, a feed of the most recent commits across all repos, and a 365-day contribution canvas.
- **Cosmos** — each repo plotted as a star. Brightness = recency, size = activity. Drag to look around, hover to inspect.
- **Rhythm** — a polar clock showing the hour-of-day distribution of recent commits.

Toggle between them with the pill switcher (or `#lab`, `#cosmos`, `#rhythm` in the URL).

## Stack

- Single static `index.html`, no build step. Vanilla JS, SVG + Canvas.
- Data via [the Apps Script proxy](https://github.com/sankhacooray/dev-sankhacooray-com-proxy).
- Hosted on GitHub Pages, fronted by Cloudflare DNS (proxy off).

## Local development

```bash
python3 -m http.server 4080
# → http://localhost:4080
```
