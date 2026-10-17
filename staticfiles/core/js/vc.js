/* VC — Interacciones: header, menú móvil, hero rotativo, paneles y carrusel. Sin dependencias. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', function () {
    /* Header: sombra al hacer scroll + menú móvil */
    var header = document.getElementById('vcHeader');
    var burger = document.getElementById('vcBurger');
    if (header) {
      var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 40); };
      window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    }
    if (header && burger) {
      burger.addEventListener('click', function () {
        var open = header.classList.toggle('is-open');
        burger.setAttribute('aria-expanded', String(open));
        burger.textContent = open ? '✕' : '☰';
      });
      header.querySelectorAll('.vc-mobile-nav a').forEach(function (a) {
        a.addEventListener('click', function () { header.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); burger.textContent = '☰'; });
      });
    }

    /* Mensajes Django: se ocultan solos */
    document.querySelectorAll('.vc-toast').forEach(function (t) { setTimeout(function () { t.remove(); }, 6000); });

    /* Hero rotativo */
    var hero = document.getElementById('vcHero');
    if (hero) {
      var slides = hero.querySelectorAll('.vc-hero__slide');
      var tabs = hero.querySelectorAll('.vc-hero__tab');
      var ms = parseInt(hero.getAttribute('data-interval'), 10) || 6500;
      hero.style.setProperty('--vc-slide-ms', ms + 'ms');
      var idx = 0, timer = null;
      var show = function (i) {
        idx = (i + slides.length) % slides.length;
        slides.forEach(function (s, k) { s.classList.toggle('is-active', k === idx); s.setAttribute('aria-hidden', String(k !== idx)); });
        tabs.forEach(function (t, k) {
          t.classList.remove('is-active');
          if (k === idx) { void t.offsetWidth; t.classList.add('is-active'); } // reinicia la barra de progreso
        });
      };
      var start = function () { if (reduce) { hero.classList.add('is-paused'); return; } clearInterval(timer); timer = setInterval(function () { show(idx + 1); }, ms); };
      tabs.forEach(function (t, k) { t.addEventListener('click', function () { show(k); start(); }); });
      document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(timer); else start(); });
      start();
    }

    /* Paneles de especialidades */
    var panels = document.querySelectorAll('#vcPanels .vc-panel');
    var activate = function (p) {
      panels.forEach(function (x) { var on = x === p; x.classList.toggle('is-active', on); x.setAttribute('aria-expanded', String(on)); });
    };
    panels.forEach(function (p) {
      p.addEventListener('mouseenter', function () { if (window.matchMedia('(hover: hover)').matches) activate(p); });
      p.addEventListener('click', function () { activate(p); });
      p.addEventListener('focus', function () { activate(p); });
      p.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(p); } });
    });

    /* Carrusel de proyectos */
    var wrap = document.getElementById('vcProjects');
    if (wrap) {
      var imgs = wrap.querySelectorAll('.vc-projects__media img');
      var items = wrap.querySelectorAll('.vc-project');
      var thumbs = wrap.querySelectorAll('.vc-thumb');
      var tag = document.getElementById('vcProjTag');
      var num = document.getElementById('vcProjNum');
      var cur = 0;
      var go = function (i) {
        cur = (i + items.length) % items.length;
        imgs.forEach(function (im, k) { im.classList.toggle('is-active', k === cur); });
        items.forEach(function (it, k) { it.classList.toggle('is-active', k === cur); });
        thumbs.forEach(function (th, k) { th.classList.toggle('is-active', k === cur); th.setAttribute('aria-pressed', String(k === cur)); });
        if (num) num.textContent = '0' + (cur + 1);
        if (tag) { tag.setAttribute('data-i18n', items[cur].getAttribute('data-tag')); if (window.VCi18n) window.VCi18n.apply(); }
      };
      var prev = document.getElementById('vcPrev'), next = document.getElementById('vcNext');
      if (prev) prev.addEventListener('click', function () { go(cur - 1); });
      if (next) next.addEventListener('click', function () { go(cur + 1); });
      thumbs.forEach(function (th) { th.addEventListener('click', function () { go(parseInt(th.getAttribute('data-proj'), 10)); }); });
      wrap.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    }

    /* Filtros por categoría (Proyectos y Blog) */
    document.querySelectorAll('[data-filter-group]').forEach(function (group) {
      var name = group.getAttribute('data-filter-group');
      var items = document.querySelectorAll('[data-filter-items="' + name + '"] [data-cat]');
      group.querySelectorAll('[data-filter]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var f = btn.getAttribute('data-filter');
          group.querySelectorAll('[data-filter]').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
          items.forEach(function (it) { it.hidden = !(f === 'all' || it.getAttribute('data-cat') === f); });
        });
      });
    });

    /* Denuncias: alternar datos de contacto */
    var anon = document.getElementById('vcAnon'), datos = document.getElementById('vcDatos');
    if (anon && datos) {
      var sync = function () {
        datos.hidden = anon.checked;
        if (anon.checked) datos.querySelectorAll('input').forEach(function (i) { i.value = ''; });
      };
      anon.addEventListener('change', sync); sync();
    }
  });
})();
