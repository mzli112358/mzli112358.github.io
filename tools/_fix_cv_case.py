# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parent.parent
repls = [
    ('href="cv/"', 'href="CV/"'),
    ("href='cv/'", "href='CV/'"),
    ("../cv/", "../CV/"),
    ("`cv/`", "`CV/`"),
    ("cv/index.html", "CV/index.html"),
    ('item("cv", "cv/"', 'item("cv", "CV/"'),
    ("mzli112358.github.io/cv/", "mzli112358.github.io/CV/"),
    ("url=../cv/", "url=../CV/"),
    ("replace('../cv/')", "replace('../CV/')"),
    ("旧链 → cv/", "旧链 → CV/"),
    ("├── cv/", "├── CV/"),
    ("| `cv/`", "| `CV/`"),
    ("替换 `cv/", "替换 `CV/"),
    ("学术简历 | `cv/`", "学术简历 | `CV/`"),
    ("独立页（`projects/photomate.html`、`projects/furniture-print.html`、`cv/index.html`）",
     "独立页（`projects/photomate.html`、`projects/furniture-print.html`、`CV/index.html`）"),
]

for p in root.rglob("*"):
    if not p.is_file() or ".git" in p.parts:
        continue
    if p.suffix.lower() not in {".html", ".py", ".md", ".css", ".js", ".yml", ".txt"}:
        continue
    if p.name.startswith("_fix_cv_case"):
        continue
    t = p.read_text(encoding="utf-8")
    orig = t
    for a, b in repls:
        t = t.replace(a, b)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print("updated", p.relative_to(root))
