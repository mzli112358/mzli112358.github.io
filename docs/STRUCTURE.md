# 站点目录结构 / Site Structure

```
mzli112358.github.io/
├── index.html, research.html, publications.html, projects.html   # 学术主站（由 tools/_build_pages.py 生成）
├── photomate.html, furniture-print.html                          # 短链 → projects/*
├── HackathonCV/index.html                                        # 旧链 → CV/
├── projects/
│   ├── photomate.html                                            # PhotoMate 项目页
│   └── furniture-print.html                                      # 室内米级协作臂 3D 打印
├── CV/
│   ├── index.html                                                # 学术简历查看器（中/英 PDF）
│   ├── Mingzhe_Li_CV-0725.pdf
│   ├── 李明哲_简历-0725.pdf
│   └── archive/                                                  # 星尘黑客松旧简历等
├── tools/
│   └── _build_pages.py                                           # 生成学术页；改完后运行
├── docs/
│   ├── BILINGUAL.md
│   └── STRUCTURE.md
├── assets/                                                       # css / js / images
├── .github/workflows/deploy.yml
└── README.md
```

## 编辑规则

1. **学术四页**：只改 `tools/_build_pages.py`，再 `python tools/_build_pages.py`。
2. **项目独立页**：直接改 `projects/*.html` 内中英成对文案。
3. **简历 PDF**：更新 `CV/` 下带日期的 PDF，并改 `CV/index.html` 中的文件名与 `?v=` 缓存参数。
4. 旧 URL（`photomate.html`、`HackathonCV/`）保留跳转，勿删短链。

## 待规划

- **Activities / 活动记录**独立页：**方案 A（2026-07-30）= 只留素材、暂不做页**；素材在父库 `履历背景/活动记录.md`。未实现前不要在导航里挂空链。
