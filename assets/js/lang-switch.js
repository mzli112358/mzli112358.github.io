/**
 * Site-wide ZH/EN toggle.
 * - Persists choice in localStorage key `site-lang` (`zh-CN` | `en`)
 * - Expects buttons #langZh / #langEn (may appear multiple times; all are synced)
 * - Content visibility uses CSS: html[lang=...] .lang-zh / .lang-en
 *
 * BILINGUAL RULE / 双语规则:
 *   ZH ↔ EN are paired. Edit one language ⇒ update the other in the same commit.
 *   修改任一语言文案时，必须同步修改对应另一语言。
 */
(function () {
  var STORAGE_KEY = 'site-lang';

  function applyLang(lang) {
    var root = document.documentElement;
    var isZh = lang === 'zh-CN';
    root.lang = isZh ? 'zh-CN' : 'en';

    document.querySelectorAll('#langZh, [data-lang-btn="zh"]').forEach(function (btn) {
      btn.classList.toggle('is-active', isZh);
      btn.setAttribute('aria-pressed', String(isZh));
    });
    document.querySelectorAll('#langEn, [data-lang-btn="en"]').forEach(function (btn) {
      btn.classList.toggle('is-active', !isZh);
      btn.setAttribute('aria-pressed', String(!isZh));
    });

    try {
      localStorage.setItem(STORAGE_KEY, isZh ? 'zh-CN' : 'en');
    } catch (e) {}
  }

  function bind() {
    document.querySelectorAll('#langZh, [data-lang-btn="zh"]').forEach(function (btn) {
      btn.addEventListener('click', function () { applyLang('zh-CN'); });
    });
    document.querySelectorAll('#langEn, [data-lang-btn="en"]').forEach(function (btn) {
      btn.addEventListener('click', function () { applyLang('en'); });
    });

    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    if (saved === 'en' || saved === 'zh-CN') {
      applyLang(saved);
    } else {
      applyLang(document.documentElement.lang === 'en' ? 'en' : 'zh-CN');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();
