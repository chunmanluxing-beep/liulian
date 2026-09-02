/* 流涟旅拍 · 渐进增强脚本(L2)
   原则:关掉 JS 全站仍可完整浏览 —— 灯箱与十地面板都走 :target(纯 CSS),
   滑动走 scroll-snap(纯 CSS),语言是两套静态页互链。
   这里只做增强:语言记忆、灯箱键盘、面板的焦点管理与 Esc。 */
(function () {
  'use strict';

  /* ① 语言记忆 */
  var KEY = 'liulian.lang';
  var here = document.documentElement.lang.indexOf('en') === 0 ? 'en' : 'zh';
  try {
    var links = document.querySelectorAll('[data-lang]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function () {
        try { localStorage.setItem(KEY, this.getAttribute('data-lang')); } catch (e) {}
      });
    }
    var saved = localStorage.getItem(KEY);
    if (saved && saved !== here && !location.hash) {
      var to = document.querySelector('[data-lang="' + saved + '"]');
      if (to) { location.replace(to.getAttribute('href')); return; }
    }
  } catch (e) { /* 隐私模式下直接跳过 */ }

  /* ② 灯箱键盘:Esc 关闭、左右翻页 */
  document.addEventListener('keydown', function (ev) {
    var box = document.querySelector('.lb:target');
    if (box) {
      if (ev.key === 'Escape') {
        var x = box.querySelector('.lb-x');
        if (x) { location.replace(x.getAttribute('href')); }
      } else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
        var a = box.querySelector(ev.key === 'ArrowLeft' ? '.lb-prev' : '.lb-next');
        if (a) { ev.preventDefault(); location.replace(a.getAttribute('href')); }
      }
      return;
    }
    /* ③ 面板 Esc 关闭 */
    if (ev.key === 'Escape') {
      var pn = document.querySelector('.panel:target, .panel.open');
      if (pn) { closePanel(pn); }
    }
  });

  /* ③ 十地面板:接管打开/关闭,做焦点管理(:target 机制保留为无 JS 回退) */
  var lastTrigger = null;

  function openPanel(pn, trigger) {
    var cur = document.querySelector('.panel.open');
    if (cur && cur !== pn) { cur.classList.remove('open'); }
    pn.classList.add('open');
    lastTrigger = trigger || null;
    var c = pn.querySelector('.pclose');
    if (c) { c.focus({ preventScroll: true }); }
  }
  function closePanel(pn) {
    pn.classList.remove('open');
    if (location.hash === '#' + pn.id) {
      history.replaceState(null, '', location.pathname + '#areas');
    }
    if (lastTrigger && lastTrigger.focus) { lastTrigger.focus({ preventScroll: true }); }
    lastTrigger = null;
  }

  document.addEventListener('click', function (ev) {
    var a = ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    /* 打开面板的链接(地图点 / chip) */
    if (href.indexOf('#pn-') === 0) {
      var pn = document.getElementById(href.slice(1));
      if (pn) { ev.preventDefault(); openPanel(pn, a); }
      return;
    }
    /* 面板内的关闭(✕ / 遮罩)与出口(预订) */
    var inPanel = a.closest('.panel');
    if (inPanel && (a.classList.contains('pclose') || a.classList.contains('pmask'))) {
      ev.preventDefault(); closePanel(inPanel); return;
    }
    if (inPanel && href === '#contact') {
      closePanel(inPanel); /* 不 preventDefault:继续跳到联系区 */
    }
  });

  /* 面板打开时把焦点圈在面板内(基本合格的焦点管理) */
  document.addEventListener('focusin', function (ev) {
    var pn = document.querySelector('.panel.open');
    if (pn && !pn.contains(ev.target)) {
      var c = pn.querySelector('.pclose');
      if (c) { c.focus({ preventScroll: true }); }
    }
  });
})();
