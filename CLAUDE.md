# stephensironi-site

Static portfolio for stephensironi.com (CNAME at repo root, GitHub Pages). Plain HTML/CSS, no build step.

## Pages
All pages are hand-edited HTML: `index` (home, 6 featured paintings), `everyday`, `gatherings`, `portraits` (the three galleries), `about`, `contact` (inquiry form posts to Formspree), `404`, plus `sitemap.xml` and `robots.txt`.

`paintings-data.csv` is a reference record of every painting (title, gallery, location, medium, price, description, availability). Nothing reads it; the old generator and `gallery.html` were retired because they predated the move from location-based to style-based galleries. Keep it in sync by hand if paintings change.

## Images
- `images/originals/` (359M) is gitignored. Backed up (one-time copy, Nov 4 2026) to `~/Dropbox/stephensironi-site/originals/`. Re-sync after changes: `rsync -a --exclude .DS_Store images/originals/ ~/Dropbox/stephensironi-site/originals/`
- `images/paintings/{everyday,gatherings,portraits}/` are the committed web versions.

## Deploy
Push to `main`.

## Shared code
- `css/site.css` (all pages), `css/inner.css` (every page except home), `css/gallery.css` (gatherings + portraits), `js/site.js` (menu toggle + page fade, all pages). Page-specific styles stay inline in each page.
- The nav and mobile menu markup is still copied into each page (no build step), so a nav change means editing all 7 HTML files (index, about, contact, everyday, gatherings, portraits, 404).
- Inner pages carry JSON-LD that references the `#artist` and `#website` ids defined on the home page.
