    (function () {
      var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

      /* 언어 (KO/EN) */
      var langBtn = document.getElementById('langBtn');
      var lang = localStorage.getItem('qmesh-lang') || 'ko';
      function applyLang() {
        document.documentElement.lang = lang;
        langBtn.textContent = lang === 'ko' ? 'KO' : 'EN';
        var nodes = document.querySelectorAll('[data-ko]');
        for (var i = 0; i < nodes.length; i++) {
          var v = nodes[i].getAttribute('data-' + lang);
          if (v != null) nodes[i].innerHTML = v;
        }
      }
      langBtn.addEventListener('click', function () {
        lang = lang === 'ko' ? 'en' : 'ko';
        localStorage.setItem('qmesh-lang', lang);
        applyLang();
      });
      applyLang();

      /* 테마 */
      var themeBtn = document.getElementById('themeBtn');
      var saved = localStorage.getItem('qmesh-theme');
      if (saved) document.documentElement.setAttribute('data-theme', saved);
      themeBtn.addEventListener('click', function () {
        var cur = document.documentElement.getAttribute('data-theme');
        if (!cur) cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        var next = cur === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('qmesh-theme', next);
      });

      /* reveal - 앵커(#scenarios 등)로 바로 들어와도 빈 화면이 보이지 않게,
         IO 콜백을 기다리지 않고 뷰포트 안의 요소는 즉시 노출한다 */
      var reveals = [].slice.call(document.querySelectorAll('.reveal'));
      function revealVisible() {
        reveals.forEach(function (el) {
          if (el.classList.contains('in')) return;
          var r = el.getBoundingClientRect();
          if (r.top < innerHeight && r.bottom > 0) el.classList.add('in');
        });
      }
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0, rootMargin: '0px 0px -6% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
      revealVisible();
      addEventListener('load', revealVisible);
      addEventListener('hashchange', function () { requestAnimationFrame(revealVisible); });

      /* GIF 지연 로딩 - 클릭해야 내려받는다 */
      document.querySelectorAll('.gif-shell').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var img = new Image();
          img.src = btn.dataset.src;
          img.alt = btn.dataset.alt || '';
          img.loading = 'lazy';
          btn.replaceWith(img);
        });
      });

      /* 스크롤스파이 */
      var navLinks = [].slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
      var secIO = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          var id = e.target.id;
          navLinks.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + id); });
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      ['why', 'topology', 'agents', 'scenarios', 'principles', 'status'].forEach(function (id) {
        var el = document.getElementById(id); if (el) secIO.observe(el);
      });

      /* 앵커 offset */
      document.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('href');
          if (id.length < 2) return;
          var t = document.querySelector(id);
          if (!t) return;
          e.preventDefault();
          scrollTo({ top: t.getBoundingClientRect().top + scrollY - 68, behavior: reduce ? 'auto' : 'smooth' });
        });
      });

      document.getElementById('year').textContent = new Date().getFullYear();
    })();
