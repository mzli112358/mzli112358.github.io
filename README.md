# Mingzhe Li · Academic Homepage

**Live:** https://mzli112358.github.io

个人学术主页（GitHub Pages）。中英双语单文件切换。

## 快速导航

| 内容 | 路径 |
| --- | --- |
| 关于 / 动态 | `index.html` |
| 研究 | `research.html` |
| 论文 | `publications.html` |
| 项目列表 | `projects.html` |
| PhotoMate | `projects/photomate.html`（短链 `photomate.html`） |
| 室内米级协作臂 3D 打印 | `projects/furniture-print.html`（短链 `furniture-print.html`） |
| 学术简历 | `CV/` |
| 目录说明 | [docs/STRUCTURE.md](docs/STRUCTURE.md) |
| 双语约定 | [docs/BILINGUAL.md](docs/BILINGUAL.md) |

## 待做（产品意向）

- **活动记录页 / Activities**（**方案 A，2026-07-30 已定**）：**先只留素材，暂不做页面**——不改导航、不建独立 HTML、不动 `_build_pages.py`。出席/证书等继续写在父库 [`履历背景/活动记录.md`](../履历背景/活动记录.md)；日后若要上线再另开任务。

## 怎么改内容

1. **学术主站四页**：编辑 [`tools/_build_pages.py`](tools/_build_pages.py)，然后：

```bash
python tools/_build_pages.py
```

2. **项目页**：直接编辑 `projects/photomate.html`、`projects/furniture-print.html`（改中文必改英文）。
3. **简历**：替换 `CV/*-0725.pdf`（或新日期文件名），同步改 `CV/index.html` 引用。

## 本地预览

```bash
python -m http.server 8000
```

打开 http://localhost:8000

## 部署

推送到子模块仓库 `main`；GitHub Actions 发布 Pages（含 `.nojekyll`）。

父仓库 `lmz-obsidian-private` 需更新 submodule 指针后一并提交。
