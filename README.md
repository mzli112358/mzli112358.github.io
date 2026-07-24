# Mingzhe Li · Academic Homepage

Personal academic site hosted on GitHub Pages.

**Live:** https://mzli112358.github.io

## Bilingual / 中英双语

All pages are bilingual in **one HTML file** with a 中文 / EN toggle (`.lang-zh` / `.lang-en` + `assets/js/lang-switch.js`).

**Hard rule:** edit Chinese ⇒ edit English; edit English ⇒ edit Chinese (same commit).  
详见 [BILINGUAL.md](BILINGUAL.md)。

## Structure

```
.
├── index.html              # About · Research Interests · News
├── research.html           # Research directions & experience
├── publications.html       # Publications
├── projects.html           # Selected projects
├── photomate.html          # PhotoMate project page (bilingual)
├── HackathonCV/            # CV viewer chrome (bilingual; PDF is ZH)
├── BILINGUAL.md            # ZH/EN maintenance contract
├── _build_pages.py         # Regenerates academic pages
├── assets/css/site.css
├── assets/js/lang-switch.js
└── .github/workflows/deploy.yml
```

## Edit content

1. Academic pages: edit `_build_pages.py` (paired ZH/EN), then `python _build_pages.py`
2. `photomate.html` / `HackathonCV/index.html`: edit paired strings in-file
3. Commit and push `main`

## Local preview

```bash
python -m http.server 8000
```

Open http://localhost:8000

## Deploy

Push to `main` triggers GitHub Pages via Actions (with `.nojekyll`).
