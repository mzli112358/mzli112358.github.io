# -*- coding: utf-8 -*-
"""
Generate academic-style bilingual static pages.

BILINGUAL / 双语 (see BILINGUAL.md):
  - One HTML file per page; toggle ZH/EN via .lang-zh / .lang-en + lang-switch.js
  - Edit ZH ⇒ edit EN (same commit). Edit EN ⇒ edit ZH.
  - 修改中文必须同步修改英文；修改英文必须同步修改中文。
  - Prefer editing THIS file, then: python _build_pages.py
"""
from pathlib import Path

# Site root is the parent of tools/
ROOT = Path(__file__).resolve().parent.parent

# HTML comment injected near bilingual blocks.
BILINGUAL_NOTE = """<!-- BILINGUAL PAIR / 双语成对
     ZH ↔ EN must stay in sync.
     修改中文时请同步修改英文；修改英文时请同步修改中文。
     See BILINGUAL.md -->"""


def head(title: str, description: str, canonical: str) -> str:
    return f"""<!doctype html>
<!--
  BILINGUAL PAGE / 双语页面
  Toggle: .lang-zh / .lang-en + assets/js/lang-switch.js
  RULE: edit Chinese ⇒ edit English; edit English ⇒ edit Chinese (same commit).
  规则：改中文必改英文，改英文必改中文（同一提交）。
  Source of truth for this page family: _build_pages.py → python _build_pages.py
-->
<html lang="zh-CN" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://mzli112358.github.io/{canonical}">
  <meta property="og:locale" content="en-US">
  <meta property="og:site_name" content="Mingzhe Li">
  <meta property="og:title" content="{title}">
  <meta property="og:url" content="https://mzli112358.github.io/{canonical}">
  <meta property="og:description" content="{description}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Mingzhe Li",
    "alternateName": "李明哲",
    "url": "https://mzli112358.github.io",
    "image": "https://mzli112358.github.io/assets/images/headphoto.png",
    "jobTitle": "Incoming M.Sc. student in Robotics and Autonomous Systems",
    "affiliation": {{
      "@type": "CollegeOrUniversity",
      "name": "University of Macau"
    }},
    "alumniOf": {{
      "@type": "CollegeOrUniversity",
      "name": "Beijing Normal-Hong Kong Baptist University"
    }},
    "sameAs": [
      "https://github.com/mzli112358",
      "https://scholar.google.com/citations?user=OJAy7EEAAAAJ"
    ],
    "knowsAbout": [
      "Embodied AI",
      "VLA",
      "3D Gaussian Splatting",
      "SLAM",
      "Robotics Systems"
    ]
  }}
  </script>
  <link rel="preload" href="assets/css/main.css" as="style">
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/academicons.css">
  <link rel="stylesheet" href="assets/css/site.css?v=20260725-masthead-fix">
  <link rel="icon" type="image/png" href="assets/images/headphoto.png">
  <style>
    /* Critical FOUC CSS only. Do NOT zero body padding here:
       AcademicPages uses a fixed .masthead; main.css / site.css must keep
       top clearance so .page__title is not covered. */
    html {{
      font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: #333;
      background: #fff;
    }}
    body {{ margin: 0; }}
    a {{ color: #007acc; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
  <script>
    document.documentElement.className = document.documentElement.className.replace(/\\bno-js\\b/g, '') + ' js ';
  </script>
</head>
"""


def masthead(active: str = "about") -> str:
    def item(key: str, href: str, zh: str, en: str) -> str:
        cls = "masthead__menu-item"
        if key == active:
            cls += " current"
        return f'''            <li class="{cls}"><a href="{href}"><span class="lang-zh">{zh}</span><span class="lang-en">{en}</span></a></li>'''

    items = "\n".join([
        item("about", "index.html", "关于", "About"),
        item("research", "research.html", "研究", "Research"),
        item("publications", "publications.html", "论文", "Publications"),
        item("projects", "projects.html", "项目", "Projects"),
        item("cv", "CV/", "简历", "CV"),
        item("photomate", "projects/photomate.html", "PhotoMate", "PhotoMate"),
    ])
    return f"""
  <!-- BILINGUAL: masthead labels below are ZH/EN pairs — keep both in sync. -->
  <div class="masthead">
    <div class="masthead__inner-wrap">
      <div class="masthead__menu">
        <nav id="site-nav" class="greedy-nav">
          <!-- First <button> must remain the hamburger for greedy-nav JS -->
          <button type="button" class="greedy-nav__toggle" aria-label="Toggle menu"><div class="navicon"></div></button>
          <ul class="visible-links">
            <li class="masthead__menu-item masthead__menu-item--lg">
              <a class="masthead__brand" href="index.html">
                <span class="masthead__brand-mark" aria-hidden="true"></span>
                Mingzhe Li
              </a>
            </li>
{items}
          </ul>
          <ul class="hidden-links hidden"></ul>
          <!-- Lang toggle: sibling of menus, left of hamburger — not inside visible-links -->
          <div class="lang-switch masthead-lang-switch" role="group" aria-label="Language / 语言">
            <button type="button" data-lang-btn="zh" class="is-active" aria-pressed="true">中文</button>
            <button type="button" data-lang-btn="en" aria-pressed="false">EN</button>
          </div>
        </nav>
      </div>
    </div>
  </div>
"""


def sidebar() -> str:
    return f"""
  <!-- BILINGUAL: sidebar identity — ZH ↔ EN pair; edit both. -->
  <div class="sidebar sticky">
    <div itemscope itemtype="https://schema.org/Person">
      <div class="author__avatar">
        <img src="assets/images/headphoto.png" id="sidebar-avatar" class="author__avatar preview-image" alt="Mingzhe Li" fetchpriority="high" data-full-src="assets/images/headphoto.png">
      </div>
      <div class="author__content">
        {BILINGUAL_NOTE}
        <h3 class="author__name"><span class="lang-zh">李明哲</span><span class="lang-en">Mingzhe Li</span></h3>
        <p class="author__bio lang-zh">澳门大学 RAS 硕士（拟入学）<br>具身智能 · 三维视觉 · 机器人系统</p>
        <p class="author__bio lang-en">Incoming M.Sc. RAS @ UMacau<br>Embodied AI · 3D Vision · Robotics</p>
      </div>
      <div class="author__urls-wrapper">
        <div class="lang-switch" role="group" aria-label="Language / 语言">
          <button type="button" data-lang-btn="zh" class="is-active" aria-pressed="true">中文</button>
          <button type="button" data-lang-btn="en" aria-pressed="false">EN</button>
        </div>
        <ul class="author__urls social-icons">
          <li class="lang-zh">深圳 / 澳门</li>
          <li class="lang-en">Shenzhen / Macau</li>
          <li>mc64655 [at] um [dot] edu [dot] mo</li>
          <li><a href="https://scholar.google.com/citations?user=OJAy7EEAAAAJ" target="_blank" rel="noopener noreferrer">Google Scholar</a></li>
          <li><a href="https://github.com/mzli112358" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          <li><a href="CV/" target="_blank" rel="noopener noreferrer"><span class="lang-zh">最新简历</span><span class="lang-en">Latest CV</span></a></li>
        </ul>
      </div>
    </div>
  </div>
"""


def footer_scripts() -> str:
    return """
  <div class="page__footer">
    <footer>
      <div class="site-footer-bar">
        <div class="page__footer-copyright">
          © 2026 Mingzhe Li · Powered by <a href="https://github.com/academicpages/academicpages.github.io" target="_blank" rel="noopener noreferrer">AcademicPages</a>
        </div>
        <div class="footer-visitor-map" aria-label="Visitor map">
          <script async defer type="text/javascript" id="mapmyvisitors" src="//mapmyvisitors.com/map.js?d=L2EvxI5IxPwlHLSJ8tvLwqVqeZIb3MyUf-OLupTd254&cl=ffffff&w=a"></script>
        </div>
      </div>
    </footer>
  </div>

  <div id="imageModal" class="image-modal">
    <div class="image-modal-overlay"></div>
    <div class="image-modal-container">
      <button class="image-modal-close" id="imageModalClose" type="button">&times;</button>
      <div class="image-modal-content">
        <img id="modalImage" src="" alt="Preview" class="modal-image">
      </div>
    </div>
  </div>

  <script>
    (function () {
      var previewImages = document.querySelectorAll('.preview-image');
      var modal = document.getElementById('imageModal');
      var modalImage = document.getElementById('modalImage');
      var closeBtn = document.getElementById('imageModalClose');
      var overlay = document.querySelector('.image-modal-overlay');
      if (!previewImages.length || !modal || !modalImage) return;
      function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
      previewImages.forEach(function (img) {
        img.addEventListener('click', function () {
          modalImage.src = this.getAttribute('data-full-src') || this.src;
          modalImage.alt = this.alt;
          modal.classList.add('active');
          document.body.style.overflow = 'hidden';
        });
      });
      if (closeBtn) closeBtn.addEventListener('click', closeModal);
      if (overlay) overlay.addEventListener('click', closeModal);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeModal();
      });
    })();
  </script>
  <script src="assets/js/main.min.js"></script>
  <script src="assets/js/lang-switch.js"></script>
</body>
</html>
"""


def page(title, description, canonical, active, page_title_zh, page_title_en, content):
    return (
        head(title, description, canonical)
        + "<body>\n"
        + masthead(active)
        + '  <div id="main" role="main">\n'
        + sidebar()
        + """    <article class="page" itemscope itemtype="https://schema.org/CreativeWork">
      <div class="page__inner-wrap">
        <header>
"""
        + BILINGUAL_NOTE
        + """
          <h1 class="page__title lang-zh" itemprop="headline">"""
        + page_title_zh
        + """</h1>
          <h1 class="page__title lang-en" itemprop="headline">"""
        + page_title_en
        + """</h1>
        </header>
        <section class="page__content" itemprop="text">
"""
        + f"\n{BILINGUAL_NOTE}\n"
        + "<!-- PAGE BODY: every visible copy block below should be a ZH/EN pair. -->\n"
        + content
        + """
        </section>
      </div>
    </article>
  </div>
"""
        + footer_scripts()
    )


# ---------- page contents ----------

index_content = r"""
          <!-- BILINGUAL PAIR: about — ZH ↔ EN sync required / 改一语必改另一语 -->
          <div class="lang-zh">
            <p>我是面向<strong>机器人系统、具身智能与三维视觉</strong>的研究者与工程开发者，具备从本体设计、硬件原型、感知导航、遥操作数据采集到 <strong>VLA</strong> 训练与任务智能体的端到端经验。目前在<strong>原力无限（INFIFORCE）深圳研究院</strong>参与家庭服务机器人研发，并为香港大学陈佳玉助理教授 <strong>Agentic Intelligence Lab</strong> 核心研究实习生。</p>
            <p>本科毕业于北师香港浸会大学<strong>数据科学</strong>，已录取<strong>澳门大学机器人与自主系统（RAS）理学硕士</strong>（2026 年秋）。参与 <strong>ICML 2025</strong> 论文；本科期间创立 <strong>Navigator Robotics Lab</strong>（约 35 人），带队获 RoboMaster 工程挑战赛辽宁站第一名。</p>
            <p>更多见 <a href="research.html">研究</a>、<a href="projects.html">项目</a>、<a href="https://github.com/mzli112358">GitHub</a> 与 <a href="CV/">简历</a>。</p>
          </div>
          <div class="lang-en">
            <p>I am a researcher-engineer working on <strong>robotics systems, embodied AI, and 3D vision</strong>, with end-to-end experience from hardware prototyping and perception to <strong>VLA</strong> training and task agents. I currently work at the <strong>INFIFORCE Shenzhen Research Institute</strong> on home-service robots, and as a core research intern in Prof. Jiayu Chen’s <strong>Agentic Intelligence Lab</strong> at HKU.</p>
            <p>B.Sc. in <strong>Data Science</strong> (BNBU/UIC); incoming <strong>M.Sc. in Robotics and Autonomous Systems</strong> at the <strong>University of Macau</strong> (Fall 2026). Contributor to an <strong>ICML 2025</strong> paper; during undergrad founded <strong>Navigator Robotics Lab</strong> (~35 members) with 1st Place in the RoboMaster Regional Engineer Challenge.</p>
            <p>See <a href="research.html">Research</a>, <a href="projects.html">Projects</a>, <a href="https://github.com/mzli112358">GitHub</a>, and <a href="CV/">CV</a>.</p>
          </div>

          <hr>
          <h2 id="research-interests" class="lang-zh">研究方向</h2>
          <h2 id="research-interests-en" class="lang-en">Research Interests</h2>
          <p class="section-note lang-zh">点击卡片查看对应研究与项目细节。</p>
          <p class="section-note lang-en">Click a card for details and related projects.</p>
          <div class="interest-grid">
            <a class="interest-card" href="research.html#spatial">
              <h3 class="lang-zh">空间智能 / 3DGS</h3>
              <h3 class="lang-en">Spatial Intelligence / 3DGS</h3>
              <p class="lang-zh">几何一致重建 · SLAM · 机器人规划</p>
              <p class="lang-en">Geometry-consistent reconstruction · SLAM · planning</p>
            </a>
            <a class="interest-card" href="research.html#vla">
              <h3 class="lang-zh">具身智能 / VLA</h3>
              <h3 class="lang-en">Embodied AI / VLA</h3>
              <p class="lang-zh">遥操作采集 · 策略微调 · 长程智能体</p>
              <p class="lang-en">Teleop data · policy fine-tuning · long-horizon agents</p>
            </a>
            <a class="interest-card" href="research.html#systems">
              <h3 class="lang-zh">机器人系统工程</h3>
              <h3 class="lang-en">Robotics Systems</h3>
              <p class="lang-zh">硬件原型 · ROS · 真机联调</p>
              <p class="lang-en">Prototyping · ROS · real-robot integration</p>
            </a>
            <a class="interest-card" href="research.html#agents">
              <h3 class="lang-zh">场景 App / 任务智能体</h3>
              <h3 class="lang-en">Scene Apps / Task Agents</h3>
              <p class="lang-zh">状态机编排 · PhotoMate · 移动打印</p>
              <p class="lang-en">FSM · PhotoMate · mobile printing</p>
            </a>
            <a class="interest-card" href="research.html#cad">
              <h3 class="lang-zh">语言模型 × CAD</h3>
              <h3 class="lang-en">LLM × Parametric CAD</h3>
              <p class="lang-zh">代码生成 · LoRA · 神经符号约束</p>
              <p class="lang-en">Code generation · LoRA · neuro-symbolic constraints</p>
            </a>
            <a class="interest-card" href="research.html#llm">
              <h3 class="lang-zh">LLM 智能体</h3>
              <h3 class="lang-en">LLM Agents</h3>
              <p class="lang-zh">RAG · 多智能体 · 工业/知识产权</p>
              <p class="lang-en">RAG · multi-agent · industry / IP</p>
            </a>
          </div>
          <p><a href="research.html"><span class="lang-zh">查看研究页 →</span><span class="lang-en">See Research page →</span></a></p>

          <hr>
          <h2 id="news" class="lang-zh">动态</h2>
          <h2 id="news-en" class="lang-en">News</h2>
          <ul class="news-list">
            <li class="lang-zh"><strong>[2026.07]</strong> 启动 <a href="projects/furniture-print.html">室内米级协作臂 3D 打印</a> 项目（进行中，预计至 2027.01）。</li>
            <li class="lang-en"><strong>[2026.07]</strong> Started <a href="projects/furniture-print.html">indoor meter-scale collaborative-arm 3D printing</a> (ongoing, expected through Jan 2027).</li>
            <li class="lang-zh"><strong>[2026.07.08–11]</strong> 探月 Physical AI 黑客松：完成 <a href="projects/photomate.html">PhotoMate</a> 软件链；真机执行权限未开放。<a href="https://github.com/mzli112358/PhotoMate-Moonbot-Hackthon">代码</a></li>
            <li class="lang-en"><strong>[2026.07.08–11]</strong> Tanyue Physical AI Hackathon: <a href="projects/photomate.html">PhotoMate</a> software stack delivered; real-robot APIs unavailable. <a href="https://github.com/mzli112358/PhotoMate-Moonbot-Hackthon">Code</a></li>
            <li class="lang-zh"><strong>[2026.03]</strong> 加入 INFIFORCE 深圳研究院，并加入港大陈佳玉助理教授 Agentic Intelligence Lab（预计至 2026.09）。</li>
            <li class="lang-en"><strong>[2026.03]</strong> Joined INFIFORCE Shenzhen + Prof. Jiayu Chen’s Agentic Intelligence Lab at HKU (expected through Sep 2026).</li>
            <li class="lang-zh"><strong>[2026.03]</strong> 录取澳门大学 RAS 理学硕士（2026 秋）。</li>
            <li class="lang-en"><strong>[2026.03]</strong> Admitted to M.Sc. RAS, University of Macau (Fall 2026).</li>
          </ul>
          <details class="past-news">
            <summary><span class="lang-zh">更早动态（2025–2024）</span><span class="lang-en">Past News (2025–2024)</span></summary>
            <ul class="news-list">
              <li class="lang-zh"><strong>[2025.11]</strong> 毕业设计：动态环境鲁棒单目 SLAM 与目标跟踪。</li>
              <li class="lang-en"><strong>[2025.11]</strong> FYP: Robust Monocular SLAM in Dynamic Environments.</li>
              <li class="lang-zh"><strong>[2025.10]</strong> ICML 2025 Poster：上下文学习示范选择。</li>
              <li class="lang-en"><strong>[2025.10]</strong> ICML 2025 Poster: demonstration selection for in-context learning.</li>
              <li class="lang-zh"><strong>[2025.06]</strong> 威世博 / 小美知识产权：LLM 工程实习。</li>
              <li class="lang-en"><strong>[2025.06]</strong> LLM Engineer Intern at WISPRO / Xiaomei IP.</li>
              <li class="lang-zh"><strong>[2024.04]</strong> RoboMaster 工程挑战赛辽宁站第一名。</li>
              <li class="lang-en"><strong>[2024.04]</strong> 1st Place, RoboMaster Regional Engineer Challenge (Liaoning).</li>
            </ul>
          </details>

          <hr>
          <h2 id="education" class="lang-zh">教育经历</h2>
          <h2 id="education-en" class="lang-en">Education</h2>
          <ul class="edu-list lang-zh">
            <li>
              <strong>澳门大学</strong> — 机器人与自主系统理学硕士（拟入学）
              <span class="edu-date">2026.08 – 2028.06</span>
            </li>
            <li>
              <strong>北师香港浸会大学</strong> — 数据科学理学学士（荣誉）
              <span class="edu-date">2022.08 – 2026.06</span>
            </li>
          </ul>
          <ul class="edu-list lang-en">
            <li>
              <strong>University of Macau</strong> — Incoming M.Sc. in Robotics and Autonomous Systems
              <span class="edu-date">Aug 2026 – Jun 2028</span>
            </li>
            <li>
              <strong>BNBU / UIC</strong> — B.Sc. (Honours) in Data Science
              <span class="edu-date">Aug 2022 – Jun 2026</span>
            </li>
          </ul>

          <hr>
          <h2 id="selected-pub" class="lang-zh">精选论文</h2>
          <h2 id="selected-pub-en" class="lang-en">Selected Publication</h2>
          <div class="paper-card">
            <div class="paper-title">Demonstration Selection for In-Context Learning via Reinforcement Learning</div>
            <p class="paper-meta">Xubin Wang, Jianfei Wu, Yichen Yuan, Deyu Cai, <strong>Mingzhe Li</strong>, Weijia Jia · <em>ICML 2025</em></p>
            <p class="paper-links">
              <a class="pdf-link" href="https://arxiv.org/abs/2412.03966" target="_blank" rel="noopener noreferrer">PDF</a>
              <a href="https://icml.cc/virtual/2025/poster/43807" target="_blank" rel="noopener noreferrer">ICML</a>
              <a class="poster-link" href="https://icml.cc/media/PosterPDFs/ICML%202025/43807.png?t=1751372196.593105" target="_blank" rel="noopener noreferrer">Poster</a>
            </p>
          </div>
          <p><a href="publications.html"><span class="lang-zh">全部论文 →</span><span class="lang-en">All publications →</span></a></p>

          <hr>
          <h2 id="honors" class="lang-zh">荣誉与奖项</h2>
          <h2 id="honors-en" class="lang-en">Honors &amp; Awards</h2>
          <ul class="news-list">
            <li class="lang-zh"><strong>一等奖</strong>，RoboMaster 机甲大师高校联盟赛工程挑战赛辽宁站，2024</li>
            <li class="lang-en"><strong>1st Place</strong>, RoboMaster University League Engineer Challenge (Liaoning), 2024</li>
            <li class="lang-zh"><strong>Honorable Mention</strong>，MCM，2024</li>
            <li class="lang-en"><strong>Honorable Mention</strong>, MCM, 2024</li>
            <li class="lang-zh"><strong>二等奖</strong>，粤港澳大湾区杯 AI for Science，2024</li>
            <li class="lang-en"><strong>2nd Prize</strong>, Greater Bay Area Cup AI for Science, 2024</li>
            <li class="lang-zh"><strong>一等奖</strong>，华中杯数学建模竞赛，2023</li>
            <li class="lang-en"><strong>1st Prize</strong>, Huazhong Cup Mathematical Modeling, 2023</li>
          </ul>

"""

research_content = r"""
          <p class="lang-zh section-note">当前主线：空间表征与具身执行的交汇——让三维重建服务机器人操作，让 VLA / 任务智能体在真机上可靠运行。</p>
          <p class="lang-en section-note">Current focus: connecting spatial representations with embodied execution—3D reconstruction for robot interaction, and reliable VLA / task-agent stacks on real hardware.</p>

          <h2 id="spatial"><span class="lang-zh">空间智能 / 3DGS · SLAM</span><span class="lang-en">Spatial Intelligence / 3DGS · SLAM</span></h2>
          <p class="lang-zh">几何一致 · 实时重建 · 碰撞与规划</p>
          <p class="lang-en">Geometry consistency · real-time reconstruction · collision &amp; planning</p>
          <ul class="lang-zh">
            <li><strong>IsoGS-SLAM</strong>（2025.12–2026.04）：将隐式几何约束引入 3DGS，提升法向连续性与可交互表面。</li>
            <li><strong>动态环境单目 SLAM</strong>（FYP）：YOLO 语义掩码 + ORB-SLAM3，抑制动态特征干扰。</li>
          </ul>
          <ul class="lang-en">
            <li><strong>IsoGS-SLAM</strong> (Dec 2025–Apr 2026): implicit geometric constraints for 3DGS surface consistency.</li>
            <li><strong>Dynamic monocular SLAM</strong> (FYP): YOLO masking + ORB-SLAM3.</li>
          </ul>

          <h2 id="vla"><span class="lang-zh">具身智能 / VLA</span><span class="lang-en">Embodied AI / VLA</span></h2>
          <p class="lang-zh">遥操作 · ACT / OpenPI · 跨本体适配</p>
          <p class="lang-en">Teleoperation · ACT / OpenPI · cross-embodiment</p>
          <ul class="lang-zh">
            <li>INFIFORCE + 港大 Agentic Intelligence Lab：家庭服务机器人闭环（部署—采集—训练—执行反馈）。</li>
            <li>平台：Piper、Nero、OpenArm、Franka、星海图 R1；LeRobot / ACT / OpenPI π₀.₅。</li>
          </ul>
          <ul class="lang-en">
            <li>INFIFORCE + HKU Agentic Intelligence Lab: home-service robot loop (deploy–collect–train–execute).</li>
            <li>Platforms: Piper, Nero, OpenArm, Franka, Galaxea R1; LeRobot / ACT / OpenPI π₀.₅.</li>
          </ul>

          <h2 id="systems"><span class="lang-zh">机器人系统工程</span><span class="lang-en">Robotics Systems Engineering</span></h2>
          <p class="lang-zh">机械 · 电控 · ROS · 整机联调</p>
          <p class="lang-en">Mechanics · electronics · ROS · integration</p>
          <ul class="lang-zh">
            <li>从 0 到 1 原型：结构、PCB、装配、CAN、驱动与联调。</li>
            <li>Navigator Robotics Lab：35 人实验室建设与 RoboMaster 竞赛交付。</li>
          </ul>
          <ul class="lang-en">
            <li>Zero-to-one prototyping: structure, PCB, assembly, CAN, drivers.</li>
            <li>Navigator Robotics Lab: 35-member lab + RoboMaster delivery.</li>
          </ul>

          <h2 id="agents"><span class="lang-zh">场景 App / 任务智能体</span><span class="lang-en">Scene Apps / Task Agents</span></h2>
          <p class="lang-zh">显式状态机 · 多模态交互 · 体验交付</p>
          <p class="lang-en">Explicit FSM · multimodal interaction · experience delivery</p>
          <ul class="lang-zh">
            <li><a href="projects/photomate.html"><strong>PhotoMate</strong></a>：S0–S6 拍照 Agent（FastAPI + Qwen-Omni + React）；探月完成软件链。</li>
            <li><a href="projects/furniture-print.html"><strong>室内米级协作臂 3D 打印</strong></a>：移动操作打印 + 语音/Agent → STL → 切片执行（进行中）。</li>
            <li>长程任务智能体：导航定位、任务规划与执行链路。</li>
          </ul>
          <ul class="lang-en">
            <li><a href="projects/photomate.html"><strong>PhotoMate</strong></a>: S0–S6 photo agent (FastAPI + Qwen-Omni + React); software validated at Tanyue.</li>
            <li><a href="projects/furniture-print.html"><strong>Indoor meter-scale arm printing</strong></a>: mobile manipulative AM + voice/agent → STL → slice/execute (ongoing).</li>
            <li>Long-horizon agents: navigation, planning, and execution chains.</li>
          </ul>

          <h2 id="cad"><span class="lang-zh">语言模型 × 参数化 CAD</span><span class="lang-en">LLM × Parametric CAD</span></h2>
          <p class="lang-zh">合成数据 · LoRA · 符号约束</p>
          <p class="lang-en">Synthetic data · LoRA · symbolic constraints</p>
          <ul class="lang-zh">
            <li>~35k CadQuery 样本；DeepSeek Coder 6.7B LoRA；语法 / 执行 / 约束指标验证。</li>
          </ul>
          <ul class="lang-en">
            <li>~35k CadQuery samples; DeepSeek Coder 6.7B LoRA with syntax / execution / constraint metrics.</li>
          </ul>

          <h2 id="llm"><span class="lang-zh">LLM 智能体应用</span><span class="lang-en">LLM Agent Applications</span></h2>
          <p class="lang-zh">RAG · LangChain · 工业与知识产权</p>
          <p class="lang-en">RAG · LangChain · industry &amp; IP</p>
          <ul class="lang-zh">
            <li>专利文档多智能体（WISPRO）；工业协议微调与知识库（EpicHust）。</li>
          </ul>
          <ul class="lang-en">
            <li>Patent multi-agent systems (WISPRO); industrial-protocol fine-tuning (EpicHust).</li>
          </ul>

          <hr>
          <h2 id="experience"><span class="lang-zh">相关经历</span><span class="lang-en">Related Experience</span></h2>
          <h3 class="lang-zh">原力无限（INFIFORCE）深圳研究院 · 港大 Agentic Intelligence Lab</h3>
          <h3 class="lang-en">INFIFORCE Shenzhen · HKU Agentic Intelligence Lab</h3>
          <p class="lang-zh"><em>科研助理 / 核心研究实习生 · 2026.03 – 2026.09（预计）</em></p>
          <p class="lang-en"><em>Research Assistant / Core Research Intern · Mar 2026 – Sep 2026 (expected)</em></p>
          <ul class="lang-zh">
            <li>家庭服务机器人与 VLA：本体部署、数据采集、策略训练、长程任务执行。</li>
            <li>多平台适配与小团队工程管理 / 技术评审。</li>
          </ul>
          <ul class="lang-en">
            <li>Home-service robots &amp; VLA: deployment, data, training, long-horizon execution.</li>
            <li>Multi-platform adaptation; small-team engineering management.</li>
          </ul>
          <h3 class="lang-zh">BNBU Navigator Robotics Lab</h3>
          <h3 class="lang-en">BNBU Navigator Robotics Lab</h3>
          <p class="lang-zh"><em>创始人 / 技术负责人 · 2023.04 – 2025.08</em></p>
          <p class="lang-en"><em>Founder / Technical Lead · Apr 2023 – Aug 2025</em></p>
          <ul class="lang-zh">
            <li>本科期间从零组建校内机器人实验室；约 20 万元经费；RoboMaster 辽宁站第一名。</li>
          </ul>
          <ul class="lang-en">
            <li>Founded the student robotics lab during undergrad; ~RMB 200k funding; RoboMaster Liaoning 1st Place.</li>
          </ul>
"""

publications_content = r"""
          <p class="lang-zh">目前公开学术产出以 ICML 2025 合作为主；其他研究项目见 <a href="projects.html">项目</a> 页。</p>
          <p class="lang-en">Public academic output currently centers on an ICML 2025 collaboration; other research projects are listed under <a href="projects.html">Projects</a>.</p>

          <h2 id="y2025">2025</h2>
          <div class="paper-card">
            <div class="paper-title">Demonstration Selection for In-Context Learning via Reinforcement Learning</div>
            <p class="paper-meta">
              Xubin Wang, Jianfei Wu, Yichen Yuan, Deyu Cai, <strong>Mingzhe Li</strong>, Weijia Jia<br>
              <em>International Conference on Machine Learning (ICML)</em>, 2025 · Poster
            </p>
            <p class="paper-links">
              <a class="pdf-link" href="https://arxiv.org/abs/2412.03966" target="_blank" rel="noopener noreferrer">PDF</a>
              <a href="https://icml.cc/virtual/2025/poster/43807" target="_blank" rel="noopener noreferrer">ICML</a>
              <a class="poster-link" href="https://icml.cc/media/PosterPDFs/ICML%202025/43807.png?t=1751372196.593105" target="_blank" rel="noopener noreferrer">Poster</a>
            </p>
            <p class="lang-zh" style="color:#555;font-size:0.95rem;">提出 Relevance-Diversity Enhanced Selection (RDES)，用强化学习优化上下文学习示范选择，提升少样本文本分类与推理的泛化。</p>
            <p class="lang-en" style="color:#555;font-size:0.95rem;">Introduces Relevance-Diversity Enhanced Selection (RDES), an RL framework for selecting diverse demonstrations for in-context learning.</p>
            <img src="assets/images/icml_nano.png" data-full-src="assets/images/icml.png" alt="ICML 2025 Poster" class="preview-image" style="width:100%;height:auto;margin-top:0.75rem;">
            <pre style="margin-top:0.75rem;white-space:pre-wrap;font-size:0.85rem;background:#fff;border:1px solid #eee;padding:12px;border-radius:8px;">@misc{wang2025demonstrationselectionincontextlearning,
  title={Demonstration Selection for In-Context Learning via Reinforcement Learning},
  author={Xubin Wang and Jianfei Wu and Yichen Yuan and Deyu Cai and Mingzhe Li and Weijia Jia},
  year={2025},
  eprint={2412.03966},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2412.03966}
}</pre>
          </div>

"""

projects_content = r"""
          <div class="paper-card">
            <div class="paper-title"><a href="projects/furniture-print.html"><span class="lang-zh">1. 室内米级协作臂 3D 打印平台</span><span class="lang-en">1. Indoor Meter-Scale Collaborative-Arm 3D Printing</span></a></div>
            <p class="paper-meta lang-zh">进行中 · 2026.07–2027.01（预计）· 移动操作 · 定位融合 · 切片/G-code</p>
            <p class="paper-meta lang-en">In progress · Jul 2026–Jan 2027 (exp.) · mobile manip · localization fusion · slicing/G-code</p>
            <ul class="lang-zh">
              <li>瞄准 0.3–3 m 家具/室内尺度空白：消费级桌面打印太小，工业/建筑增材太贵或太大。</li>
              <li>协作臂 + 移动底盘 + 高精度室内定位；语音/Agent → STL → 切片 → 稳定打印。</li>
              <li><a href="projects/furniture-print.html">项目页 →</a></li>
            </ul>
            <ul class="lang-en">
              <li>Targets the awkward 0.3–3 m furniture/indoor gap between desktop and industrial/building AM.</li>
              <li>Collaborative arm + mobile base + fused indoor localization; voice/agent → STL → slice → print.</li>
              <li><a href="projects/furniture-print.html">Project page →</a></li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title"><a href="projects/photomate.html">2. PhotoMate 具身智能摄影师</a></div>
            <p class="paper-meta lang-zh">2026.07.08–11 · 探月 Physical AI 黑客松 · S0–S6 Agent</p>
            <p class="paper-meta lang-en">Jul 8–11, 2026 · Tanyue Physical AI Hackathon · S0–S6 agent</p>
            <ul class="lang-zh">
              <li>会说话的拍照服务：寻人、询问、取景、复核、二维码交付。</li>
              <li>完成 FastAPI / Qwen-Omni / React 软件链；真机执行权限未开放，未闭环。</li>
              <li><a href="https://github.com/mzli112358/PhotoMate-Moonbot-Hackthon">代码</a> · <a href="projects/photomate.html">项目页</a></li>
            </ul>
            <ul class="lang-en">
              <li>Conversational photography: search, ask, guide, review, QR delivery.</li>
              <li>Software stack completed; real-robot loop blocked by missing execution APIs.</li>
              <li><a href="https://github.com/mzli112358/PhotoMate-Moonbot-Hackthon">Repo</a> · <a href="projects/photomate.html">Page</a></li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">3. 家庭服务机器人与 VLA（INFIFORCE / AIL）</div>
            <div class="paper-title lang-en">3. Home-Service Robot &amp; VLA (INFIFORCE / AIL)</div>
            <p class="paper-meta">2026.03–2026.09 (exp.) · LeRobot · ACT / OpenPI · teleop</p>
            <ul class="lang-zh">
              <li>多臂平台集成、真实数据采集与策略微调；长程任务智能体链路。</li>
            </ul>
            <ul class="lang-en">
              <li>Multi-arm integration, real-world data, policy fine-tuning, long-horizon agents.</li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">4. IsoGS-SLAM：几何一致实时三维重建</div>
            <div class="paper-title lang-en">4. IsoGS-SLAM: Geometry-Consistent Real-Time 3D Reconstruction</div>
            <p class="paper-meta lang-zh">2025.12–2026.04 · 3DGS · SLAM · 解析法向 · CUDA</p>
            <p class="paper-meta lang-en">Dec 2025–Apr 2026 · 3DGS · SLAM · analytic normals · CUDA</p>
            <ul class="lang-zh">
              <li>针对 3DGS 表面几何与法向连续性不足，引入隐式几何约束与变分优化。</li>
            </ul>
            <ul class="lang-en">
              <li>Improves surface geometry and normal continuity in 3DGS via implicit constraints.</li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">5. 面向参数化 CAD 的专用语言模型</div>
            <div class="paper-title lang-en">5. Domain LM for Parametric CAD</div>
            <p class="paper-meta">2025.11–2026.03 · DeepSeek Coder · LoRA · CadQuery</p>
            <ul class="lang-zh">
              <li>~35,000 合成样本；95.5% 语法正确率、88.2% 执行成功率。</li>
            </ul>
            <ul class="lang-en">
              <li>~35,000 synthetic samples; 95.5% syntactic / 88.2% execution success.</li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">6. 动态环境鲁棒单目 SLAM（毕业设计）</div>
            <div class="paper-title lang-en">6. Robust Monocular SLAM (FYP)</div>
            <p class="paper-meta">2025.05–2025.11 · ORB-SLAM3 · YOLO · C++</p>
            <ul class="lang-zh">
              <li>语义掩码抑制动态特征，评估定位与目标跟踪。</li>
            </ul>
            <ul class="lang-en">
              <li>Semantic masking to suppress dynamic features; localization &amp; tracking evaluation.</li>
            </ul>
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">7. RoboMaster 实验室与竞赛机器人</div>
            <div class="paper-title lang-en">7. RoboMaster Lab &amp; Competition Robots</div>
            <p class="paper-meta">2023.04–2025.08 · team leadership · mechanical · ROS2</p>
            <ul class="lang-zh">
              <li>Navigator Robotics Lab；竞赛机器人全栈交付；辽宁站第一名。</li>
            </ul>
            <ul class="lang-en">
              <li>Navigator Robotics Lab; full-stack competition robots; Liaoning 1st Place.</li>
            </ul>
            <img src="assets/images/rm_nano.png" data-full-src="assets/images/RM.png" alt="RoboMaster Robotics Team" class="preview-image" style="width:100%;height:auto;margin-top:0.5rem;">
          </div>

          <div class="paper-card">
            <div class="paper-title lang-zh">8. 工业与知识产权 LLM 智能体</div>
            <div class="paper-title lang-en">8. LLM Agents for Industry &amp; IP</div>
            <p class="paper-meta">RAG · LangChain · multi-agent</p>
            <ul class="lang-zh">
              <li>数字工厂调度/质检；专利文档自动化审查与检索。</li>
            </ul>
            <ul class="lang-en">
              <li>Factory scheduling/defect agents; automated patent review and retrieval.</li>
            </ul>
          </div>
"""

pages = [
    (
        "index.html",
        "Mingzhe Li | Incoming M.Sc. RAS, University of Macau | Embodied AI, 3D Vision, Robotics",
        "Incoming M.Sc. in Robotics and Autonomous Systems at University of Macau. Embodied AI, VLA, 3DGS/SLAM, and robotics systems.",
        "",
        "about",
        "李明哲",
        "Mingzhe Li",
        index_content,
    ),
    (
        "research.html",
        "Research | Mingzhe Li",
        "Research interests: spatial intelligence, embodied AI / VLA, robotics systems, scene apps, LLM×CAD.",
        "research.html",
        "research",
        "研究",
        "Research",
        research_content,
    ),
    (
        "publications.html",
        "Publications | Mingzhe Li",
        "Publications by Mingzhe Li, including ICML 2025.",
        "publications.html",
        "publications",
        "论文",
        "Publications",
        publications_content,
    ),
    (
        "projects.html",
        "Projects | Mingzhe Li",
        "Selected projects: meter-scale 3D printing, PhotoMate, VLA, IsoGS-SLAM, CAD LM, RoboMaster.",
        "projects.html",
        "projects",
        "项目",
        "Projects",
        projects_content,
    ),
]

for fname, title, desc, canon, active, tzh, ten, content in pages:
    html = page(title, desc, canon, active, tzh, ten, content)
    (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, "bytes", len(html.encode("utf-8")))

print("done")
