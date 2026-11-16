# 中英双语维护约定 / Bilingual Maintenance

## 机制 / Mechanism

全站采用**单文件内双语**：同一 HTML 里用 `.lang-zh` / `.lang-en` 成对书写，右上角或侧栏按钮切换；选择写入 `localStorage.site-lang`，跨页保持。

All pages use **in-file bilingual content** with paired `.lang-zh` / `.lang-en` nodes and a toggle button. Choice is stored in `localStorage.site-lang`.

首次访问默认显示英文；访客手动切换后，继续记住已有语言选择。静态 HTML 的 `lang` 和按钮初始状态也必须为英文，避免脚本加载前显示中文。CV 页面首次默认打开英文 PDF，仍保留三语切换和独立的 PDF 语言偏好。

First-time visitors see English by default; returning visitors retain their saved language choice. Static HTML language and toggle states must also start in English. The CV viewer initially opens the English PDF and preserves its separate three-language PDF preference.

共享脚本：`assets/js/lang-switch.js`  
共享样式：`assets/css/site.css`（`html[lang=...] .lang-zh/.lang-en`）

## 强制规则 / Hard Rule

> **改中文必改英文；改英文必改中文。同一提交内完成。**  
> **Edit ZH ⇒ edit EN. Edit EN ⇒ edit ZH. Same commit.**

学术主站页面请改 `tools/_build_pages.py` 后运行 `python tools/_build_pages.py`，不要只改生成后的 HTML。  
For academic pages, edit `tools/_build_pages.py` then regenerate; do not edit generated HTML alone.

独立页（`projects/photomate.html`、`projects/furniture-print.html`、`projects/billiards.html`、`projects/ink-gravity.html`、`CV/index.html`）直接编辑文件内成对文案。  
Standalone pages: edit paired strings in those HTML files directly.

## 注释标记 / Comment Markers

在成对文案旁使用：

```html
<!-- BILINGUAL PAIR: about-lead
     ZH ↔ EN must stay in sync.
     修改中文时请同步修改英文；修改英文时请同步修改中文。 -->
```
