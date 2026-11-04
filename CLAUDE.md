# stephensironi-site

Static portfolio for stephensironi.com (CNAME at repo root, GitHub Pages). Plain HTML/CSS, no build step.

## Gallery pages
`index.html` (featured works) and `gallery.html` (full collection) are generated: edit `paintings-data.csv`, then run `python3 generate_gallery.py`. The script writes `index.html.backup` / `gallery.html.backup` first; those are gitignored, do not commit them.

## Images
- `images/originals/` (359M) is gitignored and exists only on this Mac. Back it up outside git.
- `images/paintings/` and `images/thumbnails/` are the web versions that are committed.

## Other pages
`about`, `contact`, `portraits`, `everyday`, `gatherings`, `404`, plus `sitemap.xml` and `robots.txt`. `landing-minimalist.html` is unlinked; confirm with Jeff before deleting.

## Deploy
Push to `main`.
