# dev.sankhacooray.com

See README.md for build, preview and deploy (GitHub Pages from `main`: `python3 build.py`, commit, `git push`).

## Lighthouse
<!-- lighthouse-optimized: 2026-10-31 -->
- Baseline mobile: performance 69, accessibility 100, best-practices 100, SEO 100 (desktop perf 100, a11y 100 bar one brand-name finding).
- Fixed: non-blocking Google Fonts (print/onload + noscript); brand link aria-label removed so its name matches the visible text; hero collage and card thumbs served as WebP with 400w/800w `srcset` (`build.py` uses `thumbs/<name>.webp` + `-400.webp` when present). After re-rendering a thumb JPG, regenerate both: `cwebp -q 80 -m 6 x.jpg -o x.webp; cwebp -q 80 -m 6 -resize 400 0 x.jpg -o x-400.webp`.
- Left: cache TTL (GitHub Pages fixes it at 10 min); shared scripts / gtag handled centrally.
