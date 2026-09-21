    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* 1. 아이콘 */
    const ICONS = {
      file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
      link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>',
      mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>',
      pen: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18z"/><circle cx="11" cy="11" r="2"/></svg>',
      tistory: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="6" cy="6" r="2.5"/><circle cx="12" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="12" r="2.5"/><circle cx="12" cy="18" r="2.5"/></svg>',
      velog: '<svg viewBox="0 0 192 192" fill="currentColor"><path fill-rule="evenodd" d="M24 0h144c13.255 0 24 10.745 24 24v144c0 13.255-10.745 24-24 24H24c-13.255 0-24-10.745-24-24V24C0 10.745 10.745 0 24 0Zm25 57.92v7.56h18l13.68 77.04 17.82-1.26c17.52-22.2 29.34-38.82 35.46-49.86 6.24-11.16 9.36-20.46 9.36-27.9 0-4.44-1.32-7.8-3.96-10.08-2.52-2.28-5.7-3.42-9.54-3.42-7.2 0-13.2 3.06-18 9.18 4.68 3.12 7.86 5.7 9.54 7.74 1.8 1.92 2.7 4.5 2.7 7.74 0 5.4-1.62 11.52-4.86 18.36-3.12 6.84-6.54 12.9-10.26 18.18-2.4 3.36-5.46 7.5-9.18 12.42L88.06 57.2c-.96-4.8-3.96-7.2-9-7.2-2.28 0-6.66.96-13.14 2.88-6.48 1.8-12.12 3.48-16.92 5.04Z" clip-rule="evenodd"/></svg>',
      github: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.2.8-.6v-2c-3.2.7-3.9-1.4-3.9-1.4-.5-1.3-1.3-1.7-1.3-1.7-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8.1 3.1.8.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.3c0 .4.2.7.8.6 4.6-1.5 7.9-5.8 7.9-10.9C23.5 5.7 18.3.5 12 .5Z"/></svg>',
      play: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m10 9 5 3-5 3z" fill="currentColor"/></svg>',
      download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>'
    };
    document.querySelectorAll('[data-ic]').forEach(el => { const s = ICONS[el.dataset.ic]; if (s) { el.innerHTML = s; const g = el.querySelector('svg'); g.setAttribute('width', '100%'); g.setAttribute('height', '100%'); g.style.display = 'block'; } });

    /* 2. 언어 (KO/EN) - innerHTML(굵게 등 포함) 지원 */
    const langBtn = document.getElementById('langBtn');
    let lang = localStorage.getItem('lang-v5') || 'ko';
    function applyLang() {
      document.documentElement.lang = lang;
      langBtn.classList.toggle('on', lang === 'en');
      document.querySelectorAll('[data-ko]').forEach(el => { const v = el.getAttribute('data-' + lang); if (v != null) el.innerHTML = v; });
    }
    langBtn.addEventListener('click', () => { lang = lang === 'ko' ? 'en' : 'ko'; localStorage.setItem('lang-v5', lang); applyLang(); });
    applyLang();

    /* 3. 테마 */
    const themeBtn = document.getElementById('themeBtn');
    const st = localStorage.getItem('theme-v5'); if (st) document.documentElement.setAttribute('data-theme', st);
    themeBtn.addEventListener('click', () => { const n = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; document.documentElement.setAttribute('data-theme', n); localStorage.setItem('theme-v5', n); });

    /* 4. reveal */
    const io = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));

    /* 4-a. 카드 본문 그림 - 화면에 들어올 때 받아온다.
       모달은 열 때 주입하지만(9절) 카드 그림에는 여는 동작이 없다.
       접힌 카드의 .pc-figure 는 높이가 0 이라 교차하지 않으므로,
       펼치고 스크롤해 눈에 들어온 순간에만 요청이 나간다 - 초기 로딩은 0 건. */
    const figIO = new IntersectionObserver((es) => es.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.querySelectorAll('img[data-src]').forEach(img => {
        if (!img.getAttribute('src')) img.setAttribute('src', img.dataset.src);
      });
      figIO.unobserve(e.target);
    }), { rootMargin: '200px 0px' });
    document.querySelectorAll('.pc-figure').forEach(el => figIO.observe(el));

    /* 5. 카운터 */
    function cnt(el) { const t = +el.dataset.count, dec = +(el.dataset.dec || 0); if (reduce) { el.textContent = t.toFixed(dec); return; } const d = 1400, t0 = performance.now(); (function s(n) { const p = Math.min((n - t0) / d, 1); el.textContent = (t * (1 - Math.pow(1 - p, 3))).toFixed(dec); if (p < 1) requestAnimationFrame(s); })(t0); }
    const cIO = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { cnt(e.target); cIO.unobserve(e.target); } }), { threshold: .5 });
    document.querySelectorAll('[data-count]').forEach(el => cIO.observe(el));

    /* 6. 프로젝트 아코디언 */
    document.querySelectorAll('.pcard').forEach(c => c.querySelector('.pc-top').addEventListener('click', e => { if (e.target.closest('a,button')) return; c.classList.toggle('open'); }));
    document.querySelectorAll('.tl').forEach(t => { const h = t.querySelector('.tl-head'); if (h) h.addEventListener('click', e => { if (e.target.closest('a,button')) return; t.classList.toggle('on'); }); });

    /* 6-a. 하위 프로젝트 카드 (QMesh 안의 FinAllQ·InsuQ·MaintQ)
       stopPropagation 이 핵심 - 없으면 하위를 열 때 부모 QMesh 카드가 닫힌다. */
    document.querySelectorAll('.subcard').forEach(sc => {
      const top = sc.querySelector('.sub-top');
      if (!top) return;
      top.addEventListener('click', e => {
        if (e.target.closest('a,button')) return;
        e.stopPropagation();
        sc.classList.toggle('open');
      });
    });

    /* 6-c. 주소의 #id 로 카드 열기 - 인쇄본 «상세보기» 링크(#qmesh · #finallq …)가 여기로 온다.
       접힌 카드는 높이가 0 이라 스크롤 위치가 틀린다: 부모 카드와 하위 카드를 먼저 열고,
       펼침 애니메이션(.5s)이 끝난 뒤 스크롤한다. */
    const openFromHash = () => {
      const id = decodeURIComponent(location.hash.slice(1));
      const el = id && document.getElementById(id);
      if (!el || !el.matches('.pcard, .subcard')) return;
      el.closest('.pcard')?.classList.add('open');
      if (el.matches('.subcard')) el.classList.add('open');
      /* 스크롤 목표는 시작 순간에 정해진다. 그 뒤 위쪽 카드의 펼침·폰트 로드로 높이가 바뀌면
         실측 −43~+53px 어긋났다 - 멈춘 뒤 한 번 더 맞춘다. 그사이 사람이 스크롤하면 손대지 않는다. */
      let userMoved = false;
      ['wheel', 'touchstart', 'keydown'].forEach(ev => addEventListener(ev, () => { userMoved = true; }, { once: true, passive: true }));
      const fix = () => {
        if (userMoved) return;
        const off = el.getBoundingClientRect().top - (parseFloat(getComputedStyle(el).scrollMarginTop) || 0);
        if (Math.abs(off) > 4) el.scrollIntoView({ behavior: 'auto', block: 'start' });
      };
      setTimeout(() => {
        el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
        addEventListener('scrollend', fix, { once: true });
        setTimeout(fix, 2500);
      }, 560);
    };
    openFromHash();
    window.addEventListener('hashchange', openFromHash);

    /* 6-b. 기능 모달
       본문은 처음부터 DOM 에 있고 hidden 만 토글한다 - 복제하면 applyLang() 이
       닿지 않아 모달 안에서 KO/EN 전환이 죽는다. */
    (() => {
      const modal = document.getElementById('fmodal');
      if (!modal) return;
      const panes = [...modal.querySelectorAll('.fmodal-body > section')];
      let lastFocus = null;

      const open = id => {
        const pane = panes.find(p => p.id === id);
        if (!pane) return;
        lastFocus = document.activeElement;
        panes.forEach(p => { p.hidden = p !== pane; });
        /* GIF 는 열 때만 로드한다 - 초기 페이지 로딩에 영향을 주지 않는다. */
        pane.querySelectorAll('img[data-src]').forEach(img => {
          if (!img.getAttribute('src')) img.setAttribute('src', img.dataset.src);
        });
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
        modal.querySelector('.fmodal-card').scrollTop = 0;
        (modal.querySelector('.fmodal-x') || modal).focus();
      };

      const close = () => {
        modal.hidden = true;
        document.body.style.overflow = '';
        if (lastFocus) { lastFocus.focus(); lastFocus = null; }
      };

      document.querySelectorAll('.feat[data-modal], .metric[data-modal]').forEach(btn => {
        btn.addEventListener('click', e => { e.stopPropagation(); open(btn.dataset.modal); });
        /* 결과 숫자 칸은 div 라 Enter/Space 를 직접 받는다 */
        if (btn.matches('.metric')) btn.addEventListener('keydown', e => {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(btn.dataset.modal); }
        });
      });

      modal.addEventListener('click', e => { if (e.target === modal) close(); });
      modal.querySelector('.fmodal-x')?.addEventListener('click', close);
      document.addEventListener('keydown', e => {
        if (modal.hidden) return;
        if (e.key === 'Escape') { close(); return; }
        if (e.key !== 'Tab') return;
        /* 포커스 트랩 */
        const f = [...modal.querySelectorAll('button,[href],[tabindex]:not([tabindex="-1"])')]
          .filter(el => el.offsetParent !== null);
        if (!f.length) return;
        const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      });
    })();

    /* 7. 스크롤스파이 (상단 네비 active) */
    const navLinks = [...document.querySelectorAll('.nav-links a')];
    const secIO = new IntersectionObserver((es) => es.forEach(e => { if (e.isIntersecting) { const id = e.target.id; navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id)); } }), { rootMargin: '-45% 0px -50% 0px' });
    ['about', 'skill', 'career', 'projects', 'future', 'contact'].forEach(id => { const el = document.getElementById(id); if (el) secIO.observe(el); });

    /* 8. 앵커 스크롤 offset */
    document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href'); if (id.length < 2) return; const t = document.querySelector(id); if (!t) return; e.preventDefault(); scrollTo({ top: t.getBoundingClientRect().top + scrollY - 72, behavior: reduce ? 'auto' : 'smooth' }); }));

    /* 9. PDF 다운로드는 헤더의 <a id="pdfBtn" download>가 직접 처리 (미리 만들어둔 PDF 파일) */
    /* 수동 인쇄(Ctrl+P) 직전: 스크롤 안 된 섹션의 카운터가 0으로 찍히지 않도록 최종값 확정 + 모든 reveal 노출 */
    window.addEventListener('beforeprint', () => {
      document.querySelectorAll('[data-count]').forEach(el => { el.textContent = el.dataset.count; });
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    });

    /* 10. 연도 + 기준일 + 콘솔 */
    document.getElementById('year').textContent = new Date().getFullYear();

    /* 기준일 SSOT - 프로젝트 카드의 진행 상황 수치가 언제 것인지 밝힌다.
       레포를 다시 대조해 카드를 갱신할 때 이 한 줄만 고치면 히어로 배지와
       프로젝트 섹션이 함께 따라온다. 두 곳을 따로 고치다 갈라지는 일을 막는다. */
    const AS_OF = { y: 2026, m: 9, d: 13 };
    (() => {
      const p = n => String(n).padStart(2, '0');
      const short = { ko: `${p(AS_OF.y % 100)}.${p(AS_OF.m)} 기준`, en: `as of ${p(AS_OF.y % 100)}.${p(AS_OF.m)}` };
      const full = {
        ko: `진행 상황 기준일 · ${AS_OF.y}.${p(AS_OF.m)}.${p(AS_OF.d)}`,
        en: `Status as of ${AS_OF.y}-${p(AS_OF.m)}-${p(AS_OF.d)}`
      };
      document.querySelectorAll('.as-of').forEach(el => Object.assign(el.dataset, { ko: short.ko, en: short.en }));
      document.querySelectorAll('.sec-asof').forEach(el => Object.assign(el.dataset, { ko: full.ko, en: full.en }));
      /* applyLang()은 이 블록보다 먼저 한 번 돌았으므로 현재 언어로 다시 그린다.
         이후 언어 전환은 기존 토글이 갱신된 data-ko/data-en을 다시 읽는다. */
      const cur = document.documentElement.lang === 'en' ? 'en' : 'ko';
      document.querySelectorAll('.as-of').forEach(el => el.textContent = short[cur]);
      document.querySelectorAll('.sec-asof').forEach(el => el.textContent = full[cur]);
    })();
    console.log('%c★ Trusted AI Portfolio v5 ★', 'color:#3a5bd0;font-size:14px;font-weight:700');

    /* 11-0. 카드 그림은 반쪽 칸에 들어가 구성도 글자가 작다 - 누르면 원본을 새 탭으로 연다. */
    document.querySelectorAll('.pc-slide img').forEach(img => {
      img.addEventListener('click', e => {
        e.stopPropagation();
        const src = img.currentSrc || img.getAttribute('src') || img.dataset.src;
        if (src) window.open(src, '_blank', 'noopener');
      });
    });

    /* 11. 이미지 슬라이더 (pc-figure 멀티 이미지 < > 컨트롤) */
    document.querySelectorAll('.pc-figure').forEach(fig => {
      const slides = fig.querySelectorAll('.pc-slide');
      if (slides.length <= 1) return; // 1개 이하일 경우 < > 버튼 및 dot 생성하지 않음

      slides.forEach((s, idx) => s.classList.toggle('active', idx === 0));

      const prevBtn = document.createElement('button');
      prevBtn.className = 'pc-nav prev';
      prevBtn.setAttribute('aria-label', 'Previous image');
      prevBtn.innerHTML = '&lt;';

      const nextBtn = document.createElement('button');
      nextBtn.className = 'pc-nav next';
      nextBtn.setAttribute('aria-label', 'Next image');
      nextBtn.innerHTML = '&gt;';

      const dotsContainer = document.createElement('div');
      dotsContainer.className = 'pc-dots';

      slides.forEach((_, idx) => {
        const dot = document.createElement('span');
        dot.className = 'pc-dot' + (idx === 0 ? ' active' : '');
        dot.addEventListener('click', (e) => {
          e.stopPropagation();
          goToSlide(idx);
        });
        dotsContainer.appendChild(dot);
      });

      let current = 0;
      function goToSlide(index) {
        current = (index + slides.length) % slides.length;
        slides.forEach((s, idx) => s.classList.toggle('active', idx === current));
        dotsContainer.querySelectorAll('.pc-dot').forEach((d, idx) => d.classList.toggle('active', idx === current));
      }

      prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        goToSlide(current - 1);
      });

      nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        goToSlide(current + 1);
      });

      fig.appendChild(prevBtn);
      fig.appendChild(nextBtn);
      fig.appendChild(dotsContainer);
    });

    /* 12. 이미지 비율(가로 vs 세로) 자동 측정 및 wide 클래스 자동 토글 */
    function autoDetectImageAspects() {
      document.querySelectorAll('.pc-figure').forEach(fig => {
        const imgs = fig.querySelectorAll('img');
        imgs.forEach(img => {
          function check() {
            if (img.naturalWidth && img.naturalHeight) {
              // 이미지 가로 비율이 세로보다 크면 (width > height) wide 적용
              if (img.naturalWidth / img.naturalHeight > 1.15) {
                fig.classList.add('wide');
              } else {
                fig.classList.remove('wide');
              }
            }
          }
          if (img.complete) check();
          else img.addEventListener('load', check);
        });
      });
    }
    autoDetectImageAspects();
