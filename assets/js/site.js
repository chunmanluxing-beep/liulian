/* 流涟旅拍 · 渐进增强脚本
   原则:关掉 JS 全站仍可完整浏览 —— 灯箱用 :target(纯 CSS)、
   滑动用 scroll-snap(纯 CSS)、语言用两套静态页面互链。
   这里只做三件锦上添花的事:语言记忆、灯箱键盘操作、滑动条到边提示。 */
(function () {
  'use strict';

  /* ① 语言记忆:点过语言切换就记住;下次进来若与当前页不符,跳到记住的那套。 */
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
  } catch (e) { /* 隐私模式下 localStorage 不可用:直接跳过,页面照常 */ }

  /* ② 灯箱键盘操作:Esc 关闭、左右方向键翻页(鼠标/触摸本来就能用) */
  document.addEventListener('keydown', function (ev) {
    var box = document.querySelector('.lb:target');
    if (!box) return;
    if (ev.key === 'Escape') {
      var x = box.querySelector('.lb-x');
      if (x) { location.replace(x.getAttribute('href')); }
    } else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
      var sel = ev.key === 'ArrowLeft' ? '.lb-prev' : '.lb-next';
      var a = box.querySelector(sel);
      if (a) { ev.preventDefault(); location.replace(a.getAttribute('href')); }
    }
  });

  /* ③ 滑动条滑到最后一屏时,把「左右滑动」提示淡掉,减少噪声 */
  var bars = document.querySelectorAll('.swipe');
  for (var j = 0; j < bars.length; j++) {
    (function (bar) {
      var hint = bar.parentNode.querySelector('.swipe-hint');
      if (!hint) return;
      bar.addEventListener('scroll', function () {
        var atEnd = bar.scrollLeft + bar.clientWidth >= bar.scrollWidth - 4;
        hint.style.opacity = atEnd ? '.35' : '';
      }, { passive: true });
    })(bars[j]);
  }
})();
