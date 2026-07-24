# Mingzhe Li · Academic Homepage

Personal academic site hosted on GitHub Pages.

**Live:** https://mzli112358.github.io

## Structure

```
.
├── index.html              # About · Research Interests · News
├── research.html           # Research directions & experience
├── publications.html       # Publications
├── projects.html           # Selected projects
├── photomate.html          # PhotoMate project page
├── HackathonCV/            # Latest CV (web + PDF)
├── _build_pages.py         # Regenerates academic pages
├── assets/css/
│   ├── main.css            # AcademicPages / Minimal Mistakes
│   ├── academicons.css
│   └── site.css            # Site extras (cards, lang, masthead)
└── .github/workflows/deploy.yml
```

## Edit content

1. Update copy in `_build_pages.py`
2. Run `python _build_pages.py`
3. Commit and push `main`

PhotoMate and HackathonCV pages are edited directly.

## Local preview

```bash
python -m http.server 8000
```

Open http://localhost:8000

## Deploy

Push to `main` triggers GitHub Pages via Actions (with `.nojekyll`).
