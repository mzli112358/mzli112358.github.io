/**
 * Site-wide image lightbox.
 *
 * Click any content image → it opens full screen on a dark overlay.
 * Close with the × button, Esc, or a click on the empty area around the image.
 *
 * No dependencies and no per-page markup: this file injects its own CSS and
 * overlay. Drop one <script> tag on a page and every image in it is zoomable.
 *
 * Skipped on purpose: images inside links (so navigation still works), the
 * masthead, the footer, and anything marked data-no-lightbox.
 */
(function () {
  if (window.__imgLightbox) return;
  window.__imgLightbox = true;

  var CSS = [
    '.lb-root{position:fixed;inset:0;z-index:99999;display:none;align-items:center;justify-content:center;',
    'padding:clamp(12px,3vw,40px);background:rgba(9,11,13,.96);opacity:0;transition:opacity .18s ease;}',
    '.lb-root.is-open{display:flex;opacity:1;}',
    '.lb-img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;border-radius:4px;',
    'box-shadow:0 18px 60px rgba(0,0,0,.6);opacity:0;transition:opacity .18s ease;}',
    '.lb-img.is-loaded{opacity:1;}',
    '.lb-close{position:absolute;top:14px;right:16px;width:44px;height:44px;display:inline-flex;',
    'align-items:center;justify-content:center;margin:0;padding:0;font-size:26px;line-height:1;',
    "font-family:inherit;color:#f4f4f4;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.3);",
    'border-radius:999px;cursor:pointer;}',
    '.lb-close:hover,.lb-close:focus-visible{background:rgba(255,255,255,.24);outline:none;}',
    'img.lb-zoomable{cursor:zoom-in;}',
    'body.lb-open{overflow:hidden !important;}',
    '@media (max-width:520px){.lb-close{top:10px;right:10px;width:40px;height:40px;font-size:23px;}}'
  ].join('');

  var box, big, closeBtn, lastFocus = null;

  function build() {
    var style = document.createElement('style');
    style.id = 'lb-style';
    style.textContent = CSS;
    document.head.appendChild(style);

    box = document.createElement('div');
    box.className = 'lb-root';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', '图片预览 / Image preview');

    closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'lb-close';
    closeBtn.setAttribute('aria-label', '关闭 / Close');
    closeBtn.innerHTML = '&times;';

    big = document.createElement('img');
    big.className = 'lb-img';
    big.alt = '';

    box.appendChild(closeBtn);
    box.appendChild(big);
    document.body.appendChild(box);
  }

  function isOpen() {
    return box && box.classList.contains('is-open');
  }

  function open(img) {
    var src = img.getAttribute('data-full-src') || img.getAttribute('data-src') ||
              img.currentSrc || img.src;
    if (!src) return;
    lastFocus = document.activeElement;
    big.classList.remove('is-loaded');
    big.alt = img.alt || '';
    big.src = src;
    if (big.complete) big.classList.add('is-loaded');
    box.classList.add('is-open');
    document.body.classList.add('lb-open');
    // keep the page from shifting left when the scrollbar disappears
    var gap = window.innerWidth - document.documentElement.clientWidth;
    if (gap > 0) document.body.style.paddingRight = gap + 'px';
    closeBtn.focus();
  }

  function close() {
    if (!isOpen()) return;
    box.classList.remove('is-open');
    document.body.classList.remove('lb-open');
    document.body.style.paddingRight = '';
    big.classList.remove('is-loaded');
    big.removeAttribute('src');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
    lastFocus = null;
  }

  /* Images that should not open: links keep navigating, chrome stays inert. */
  function eligible(img) {
    if (!img || img.tagName !== 'IMG') return false;
    if (box && box.contains(img)) return false;
    if (img.getAttribute('data-no-lightbox') !== null) return false;
    if (img.closest('[data-no-lightbox], .masthead, footer, .site-footer-bar')) return false;
    if (img.closest('a')) return false;
    if (img.getAttribute('aria-hidden') === 'true') return false;
    return true;
  }

  function decorate() {
    var imgs = document.querySelectorAll('img');
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      if (!eligible(img) || img.classList.contains('lb-zoomable')) continue;
      img.classList.add('lb-zoomable');
      img.setAttribute('tabindex', '0');
      img.setAttribute('data-lb-ready', '1');
    }
  }

  function onClick(e) {
    if (isOpen()) return; // the overlay handles its own clicks
    var img = e.target && e.target.closest ? e.target.closest('img') : null;
    if (!eligible(img)) return;
    e.preventDefault();
    open(img);
  }

  function onKey(e) {
    var key = e.key || '';
    if (isOpen()) {
      if (key === 'Escape' || key === 'Esc' || e.keyCode === 27) {
        e.preventDefault();
        close();
      }
      return;
    }
    if ((key === 'Enter' || key === ' ' || key === 'Spacebar') && e.target && e.target.tagName === 'IMG') {
      if (!eligible(e.target)) return;
      e.preventDefault();
      open(e.target);
    }
  }

  function init() {
    build();
    decorate();
    // some images are injected or swapped in after first paint
    window.addEventListener('load', decorate);

    document.addEventListener('click', onClick);
    document.addEventListener('keydown', onKey);

    big.addEventListener('load', function () { big.classList.add('is-loaded'); });
    box.addEventListener('click', function (e) {
      // close on the × button or on the empty area around the image
      if (e.target === box || e.target === closeBtn) close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
