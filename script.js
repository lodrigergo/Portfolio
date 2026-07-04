/* ============ Nyelvváltó: HU ↔ EN statikus oldalak közt ============ */
const IS_EN = document.documentElement.lang === 'en';
document.getElementById('langBtn').addEventListener('click', () => {
  location.href = IS_EN ? './index.html' : './en.html';
});

/* ============ Váltakozó hero-szöveg ============ */
(function () {
  const el = document.getElementById('rotWord');
  const box = document.querySelector('.rotator');
  if (!el || !box || !box.dataset.words) return;
  const words = box.dataset.words.split('|');
  let i = 0;
  el.textContent = words[0];
  setInterval(() => {
    el.classList.remove('show');
    setTimeout(() => {
      i = (i + 1) % words.length;
      el.textContent = words[i];
      el.classList.add('show');
    }, 600);
  }, 3400);
})();

/* ============ Scroll reveal + skill bar ============ */
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('visible');
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

/* ============ Mobil menü ============ */
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');
burger.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
});
navLinks.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => {
    navLinks.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
  })
);

/* ============ Kapcsolati űrlap → valódi email küldés (Web3Forms) ============ */
(function () {
  /* >>> IDE ILLESZD BE a web3forms.com-ról kapott Access Key-t (a kötőjelekkel együtt) <<< */
  const ACCESS_KEY = 'c07f4c39-e477-4444-96cc-ed7cfb6ef5c4';

  const f = document.getElementById('contactForm');
  if (!f) return;
  const status = document.getElementById('cfStatus');
  const btn = f.querySelector('button[type="submit"]');
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const hu = !IS_EN;
    const n = (document.getElementById('cfName').value || '').trim();
    const em = (document.getElementById('cfEmail').value || '').trim();
    const m = (document.getElementById('cfMsg').value || '').trim();
    if (!ACCESS_KEY || ACCESS_KEY.indexOf('IDE-JON') === 0) {
      status.style.color = '#ff8a8a';
      status.textContent = hu
        ? 'Még nincs beállítva a Web3Forms kulcs (lásd a kódban).'
        : 'Web3Forms access key is not set yet (see the code).';
      return;
    }
    status.style.color = 'var(--muted)';
    status.textContent = hu ? 'Küldés…' : 'Sending…';
    if (btn) btn.disabled = true;
    try {
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          access_key: ACCESS_KEY,
          botcheck: document.getElementById('cfBot') ? document.getElementById('cfBot').checked : false,
          subject: '📨 Új üzenet a portfólióról — ' + (n || 'Névtelen'),
          from_name: 'Portfólió · ' + (n || 'Látogató'),
          replyto: em,
          'Név': n || '—',
          'E-mail cím': em || '—',
          'Üzenet': m || '—'
        })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || !data.success) throw new Error(data.message || 'fail');
      status.style.color = 'var(--accent-light)';
      status.textContent = hu ? 'Köszönöm! Az üzenet elküldve.' : 'Thank you! Your message has been sent.';
      f.reset();
    } catch (err) {
      status.style.color = '#ff8a8a';
      status.textContent = hu
        ? 'Hiba történt — írj közvetlenül: gergolodri6@gmail.com'
        : 'Something went wrong — email directly: gergolodri6@gmail.com';
    } finally {
      if (btn) btn.disabled = false;
    }
  });
})();

/* ============ Görgetés-progress bar + statisztika-számláló ============ */
(function () {
  const bar = document.getElementById('progress');
  function onScroll() {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const p = h > 0 ? (window.scrollY / h) * 100 : 0;
    if (bar) bar.style.width = p.toFixed(1) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll); onScroll();

  const stats = document.querySelector('.stats');
  if (stats && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        stats.classList.add('in');
        stats.querySelectorAll('.num').forEach(el => {
          const target = parseInt(el.dataset.target || '0', 10);
          const suf = el.dataset.suffix || '';
          const dur = 1200, start = performance.now();
          (function step(t) {
            const k = Math.min((t - start) / dur, 1);
            el.textContent = Math.round(target * (k * (2 - k))) + (k === 1 ? suf : '');
            if (k < 1) requestAnimationFrame(step);
          })(start);
        });
        obs.disconnect();
      });
    }, { threshold: 0.6, rootMargin: '0px 0px -12% 0px' });
    io.observe(stats);
  }
})();

/* ============ Görgetésre váltó háttér-jelenetek (ablak-görgetés) ============ */
(function () {
  const blocks = [document.getElementById('hero'), ...document.querySelectorAll('section')].filter(Boolean);
  const layers = [...document.querySelectorAll('#scene .layer')];
  function setScene(i) {
    const idx = Math.max(0, Math.min(i, layers.length - 1));
    layers.forEach((l, k) => l.classList.toggle('active', k === idx));
  }
  function onScroll() {
    const mark = window.scrollY + window.innerHeight * 0.34;
    let i = 0;
    blocks.forEach((b, k) => { if (b.offsetTop <= mark) i = k; });
    setScene(i);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();

/* ============ 3D HÁLÓZAT-GALAXIS — görgetésre átrepülsz rajta ============ */
(function () {
  const canvas = document.getElementById('bg3d');
  if (!canvas || !window.THREE) return;

  const isMobile = window.innerWidth < 760;
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !isMobile });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060a14, 0.0125);
  const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 400);
  camera.position.set(0, 0, 50);

  const N = isMobile ? 620 : 1300;
  const RX = 42, RY = 34, ZNEAR = 42, ZFAR = -176;
  const nodes = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    nodes[i * 3]     = (Math.random() - 0.5) * 2 * RX;
    nodes[i * 3 + 1] = (Math.random() - 0.5) * 2 * RY;
    nodes[i * 3 + 2] = ZNEAR + Math.random() * (ZFAR - ZNEAR);
  }

  const nodeGeo = new THREE.BufferGeometry();
  nodeGeo.setAttribute('position', new THREE.BufferAttribute(nodes, 3));
  const nodeMat = new THREE.PointsMaterial({
    color: 0x7de8f7, size: 0.75, transparent: true, opacity: 0.95,
    depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true, fog: true
  });
  const points = new THREE.Points(nodeGeo, nodeMat);

  // élek a közeli csomópontok közt — egyszer kiszámolva
  const LINK2 = 15 * 15, MAXPER = 3;
  const segs = [];
  for (let i = 0; i < N; i++) {
    let c = 0;
    const ax = nodes[i*3], ay = nodes[i*3+1], az = nodes[i*3+2];
    for (let j = i + 1; j < N && c < MAXPER; j++) {
      const dx = ax-nodes[j*3], dy = ay-nodes[j*3+1], dz = az-nodes[j*3+2];
      if (dx*dx + dy*dy + dz*dz < LINK2) { segs.push(ax,ay,az, nodes[j*3],nodes[j*3+1],nodes[j*3+2]); c++; }
    }
  }
  const lineGeo = new THREE.BufferGeometry();
  lineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(segs), 3));
  const lineMat = new THREE.LineBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending, fog: true });
  const lines = new THREE.LineSegments(lineGeo, lineMat);

  const galaxy = new THREE.Group();
  galaxy.add(points); galaxy.add(lines);
  scene.add(galaxy);

  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  let progress = 0, mx = 0, my = 0;
  function onScroll() { const max = document.documentElement.scrollHeight - window.innerHeight; progress = max > 0 ? clamp(window.scrollY / max, 0, 1) : 0; }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  window.addEventListener('mousemove', e => { mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5; });

  function resize() { const w = window.innerWidth, h = window.innerHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  window.addEventListener('resize', resize); resize();

  let curZ = 50;
  const clock = new THREE.Clock();
  (function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    const targetZ = 50 - 180 * progress;
    curZ += (targetZ - curZ) * 0.06;
    camera.position.z = curZ + Math.sin(t * 0.5) * 0.6;
    camera.position.x += (mx * 10 - camera.position.x) * 0.05;
    camera.position.y += (-my * 7 - camera.position.y) * 0.05;
    galaxy.rotation.z = t * 0.02;
    camera.lookAt(0, 0, camera.position.z - 40);
    renderer.render(scene, camera);
  })();
})();
