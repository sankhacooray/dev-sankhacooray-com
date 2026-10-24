# dev

**[dev.sankhacooray.com](https://dev.sankhacooray.com)** — the developer-tools hub in the sankhacooray.com network:
Chrome extensions (Config Copilot, Tab Export), Mac, Android and MCP tools (Claude Meter, Shotlink, Outlook MCP),
the network's own plumbing (shared components, link previews, visitor badge), and the live GitHub **Activity** view.

Hosted on **GitHub Pages** from the root of `main` (custom domain via `CNAME`, Cloudflare DNS with proxy off).
No Worker and no `/api/og`: card thumbnails are files in `thumbs/`.
The VS Code workspace for the hub and its projects is `../dev-sankhacooray-com.code-workspace`.

## Files

| Path | Purpose |
|------|---------|
| `projects.json` | The hub's content: groups, projects, parts, years, live links |
| `template.html` | Page template (CSS + JS inline) |
| `footer.html` | One-line footer, placed in the last section |
| `build.py` | Renders `index.html` from the three files above, as static HTML for crawlers |
| `index.html` | **Generated** hub page. Don't edit by hand |
| `activity/` | The GitHub activity dashboard (the old dev.sankhacooray.com home): lab tiles, code cosmos (`#cosmic`), year canvas. Data from [dev-sankhacooray-com-proxy](https://github.com/sankhacooray/dev-sankhacooray-com-proxy) |
| `assets/` | The activity dashboard's icons and share image |
| `thumbs/` | Card thumbnails, 800×420 |
| `thumbs-src/` | HTML sources for the designed thumbnails (Config Copilot, Outlook MCP, visitor badge) |
| `og.png` | 1200×630 share image, rendered from `og/og.html` |
| `icon.svg`, `icon-*.png`, `apple-touch-icon.png`, `manifest.webmanifest` | Hub icons + PWA manifest (`og/icon-*.svg` are the maskable and full-bleed sources) |

Every card is **Mine** (built and run by me under BSCLab and sankhacooray). Only live sites and public
repositories are linked; several repositories are private and appear only as names in a card's parts list.

## Edit, preview, deploy

```
python3 build.py
python3 -m http.server 4805 --bind 127.0.0.1
git add -A && git commit -m "…" && git push      # GitHub Pages publishes main
```

Share image or a designed thumbnail: edit the HTML, then render it (bump `?v=N` on `og:image`/`twitter:image`
in `template.html` after changing `og.png`):

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=6000 \
  --allow-file-access-from-files --screenshot=og.png "file://$PWD/og/og.html"
```

Designed thumbnails render the same way from `thumbs-src/<name>.html`, then
`magick <shot>.png -resize 800x420 -quality 88 thumbs/<name>.jpg`.

After pushing, curl `/`, `/activity/`, `og.png`, the icons and the manifest to confirm 200s and content types.
