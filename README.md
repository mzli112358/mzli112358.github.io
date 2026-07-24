# 个人学术主页

这是 Mingzhe Li 的个人学术主页，托管在 GitHub Pages 上。网站展示了个人简介、研究成果、论文发表和项目作品集。

## 🌐 访问地址

网站地址：https://mzli112358.github.io

## 📁 项目结构

```
.
├── index.html              # 主页（个人简介、研究、项目、论文）
├── photomate.html          # PhotoMate 具身智能摄影师项目页
├── README.md               # 项目说明文档
├── assets/                 # 静态资源目录
│   ├── css/                # 样式文件
│   │   ├── main.css        # 主样式表
│   │   └── academicons.css # 学术图标样式
│   ├── js/                 # JavaScript 文件
│   │   ├── load-components.js # 组件加载脚本
│   │   ├── main.min.js     # 主脚本
│   │   ├── plotly.min.js   # Plotly 数据可视化库
│   │   ├── polyfill.min.js # Polyfill 库
│   │   └── tex-mml-chtml.js # MathJax 数学公式渲染
│   └── images/             # 图片资源
│       ├── headphoto.png   # 个人头像
│       └── ...             # 其他图片资源
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions 部署配置
```

## 🚀 技术栈

- **前端框架**：纯 HTML/CSS/JavaScript
- **部署方式**：GitHub Pages + GitHub Actions
- **数学公式**：MathJax 支持 LaTeX 数学公式渲染
- **数据可视化**：Plotly.js

## 🛠️ 本地开发

1. **克隆仓库**
   ```bash
   git clone https://github.com/mzli112358/mzli112358.github.io.git
   cd mzli112358.github.io
   ```

2. **本地预览**
   
   由于使用了动态组件加载，建议使用本地服务器预览：
   
   ```bash
   # 使用 Python 3
   python -m http.server 8000
   
   # 或使用 Node.js
   npx http-server
   
   # 或使用 PHP
   php -S localhost:8000
   ```
   
   然后在浏览器中访问 `http://localhost:8000`

## 📝 添加新内容

### 修改主页内容

直接编辑 `index.html` 文件，主页包含以下部分：
- **个人简介** (About Me)
- **新闻动态** (News)
- **论文发表** (Publications)
- **项目作品** (Selected Projects)
- **工作经历** (Experience)
- **荣誉奖项** (Honors & Awards)

### 添加图片资源

将图片文件放置在 `assets/images/` 目录下，然后在 HTML 中引用：
```html
<img src="assets/images/your-image.png" alt="描述">
```

## 🔄 自动部署

项目使用 GitHub Actions 实现自动部署：

- 当代码推送到 `main` 或 `master` 分支时，自动触发部署
- 部署过程会创建 `.nojekyll` 文件，确保 GitHub Pages 正确处理静态文件
- 部署完成后，网站会自动更新

## 📄 许可证

本项目为个人主页，保留所有权利。

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/mzli112358/mzli112358.github.io/issues)
- 个人主页: https://mzli112358.github.io

---

*最后更新：2025年12月27日*
