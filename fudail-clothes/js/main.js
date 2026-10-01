// Fudail Clothes – small enhancements; the site works without JS.
(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Sluiten' : 'Menu';
      nav.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Date fields: no dates in the past
  var d = new Date();
  var today = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  document.querySelectorAll('input[data-min-today]').forEach(function (el) { el.min = today; });

  // Prefill the item from /reserveren?collectie=...
  var item = document.getElementById('r-item');
  var names = { basics: 'Streetwear basics: ', jassen: 'Jas: ', denim: 'Jeans: ', sneakers: 'Sneakers/accessoires: ' };
  var key = new URLSearchParams(location.search).get('collectie');
  if (item && names[key] && !item.value) item.value = names[key];
  var outfitParam = new URLSearchParams(location.search).get('outfit');
  if (item && outfitParam && !item.value) item.value = outfitParam.slice(0, 200);

  // Loading state on submit (reset when the page comes back from the back/forward cache)
  document.querySelectorAll('form[data-netlify]').forEach(function (form) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    var label = btn.textContent;
    form.addEventListener('submit', function () {
      btn.disabled = true;
      btn.textContent = btn.getAttribute('data-loading-text') || label;
    });
    window.addEventListener('pageshow', function () {
      btn.disabled = false;
      btn.textContent = label;
    });
  });

  // Outfit builder ("Stel je outfit samen")
  var picker = document.querySelector('[data-outfit]');
  if (picker) {
    var S = {
      hoodie: 'M37 15q13-14 26 0l8 4 14 16 4 38-10 2-4-28-2 47H27l-2-47-4 28-10-2 4-38 14-16Z',
      tee: 'M34 14 44 9q6 9 12 0l10 5 20 16-10 14-8-6v54H32V38l-8 6-10-14Z',
      jacket: 'M36 10l14 8 14-8 10 6 14 18 2 40-10 2-4-26-2 46H28l-2-46-4 26-10-2 2-40 14-18Z',
      jeans: 'M29 8h42l5 90H56L50 42l-6 56H24Z',
      sneaker: 'M8 66q2-16 14-16l18 2 12-12q9 4 14 12l22 8q8 4 4 12H8ZM6 76h88v8H6Z'
    };
    var OPTIONS = {
      top: [
        { n: 'Heavy hoodie, groen', p: 49, c: '#1d5446', s: 'hoodie' },
        { n: 'Boxy tee, wit', p: 29, c: '#ffffff', s: 'tee' },
        { n: 'Puffer jas, roze', p: 119, c: '#d81b6a', s: 'jacket' },
        { n: 'Coach jacket, zwart', p: 89, c: '#22302b', s: 'jacket' }
      ],
      bottom: [
        { n: 'Baggy jeans, blauw', p: 69, c: '#3b5b8c', s: 'jeans' },
        { n: 'Cargo broek, zwart', p: 59, c: '#22302b', s: 'jeans' },
        { n: 'Jogger, grijs', p: 39, c: '#9aa5a0', s: 'jeans' }
      ],
      shoes: [
        { n: 'Sneaker, wit', p: 89, c: '#ffffff', s: 'sneaker' },
        { n: 'Sneaker, roze', p: 99, c: '#ff8fbf', s: 'sneaker' },
        { n: 'Skate shoe, zwart', p: 75, c: '#22302b', s: 'sneaker' }
      ]
    };
    var state = { top: 0, bottom: 0, shoes: 0 };
    var euro = function (v) {
      return '€ ' + (Math.round(v * 100) / 100).toFixed(2).replace('.', ',').replace(',00', '');
    };
    var link = picker.querySelector('[data-outfit-link]');
    var base = link.getAttribute('href').split('?')[0];
    var live = picker.querySelector('[data-live]');

    var render = function (changed) {
      var total = 0, names = [];
      Object.keys(state).forEach(function (slot) {
        var o = OPTIONS[slot][state[slot]];
        var row = picker.querySelector('[data-slot="' + slot + '"]');
        row.querySelector('[data-name]').textContent = o.n;
        row.querySelector('[data-price]').textContent = euro(o.p);
        var svg = document.querySelector('[data-svg="' + slot + '"]');
        svg.style.color = o.c;
        svg.querySelector('[data-shape]').setAttribute('d', S[o.s]);
        if (slot === changed) {
          svg.classList.remove('is-new'); void svg.getBoundingClientRect(); svg.classList.add('is-new');
          live.textContent = o.n + ', ' + euro(o.p);
        }
        total += o.p; names.push(o.n);
      });
      picker.querySelector('[data-total]').textContent = euro(total);
      picker.querySelector('[data-student]').textContent = euro(total * 0.9);
      link.setAttribute('href', base + '?outfit=' + encodeURIComponent(names.join(' + ')));
    };

    picker.querySelectorAll('.pick').forEach(function (row) {
      var slot = row.getAttribute('data-slot');
      row.querySelectorAll('.pick-btn').forEach(function (btn) {
        btn.hidden = false;
        btn.addEventListener('click', function () {
          var len = OPTIONS[slot].length;
          state[slot] = (state[slot] + Number(btn.getAttribute('data-dir')) + len) % len;
          render(slot);
        });
      });
    });
    render();
  }

  // Countdown to the Friday drop (16:00, live until 19:00), in the visitor's local time
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var label = cd.querySelector('[data-cd-label]');
    var boxes = cd.querySelector('[data-cd-boxes]');
    var pad = function (n) { return String(n).padStart(2, '0'); };
    var nextDrop = function (now) {
      var t = new Date(now);
      t.setHours(16, 0, 0, 0);
      t.setDate(t.getDate() + ((5 - t.getDay() + 7) % 7));
      if (t - now <= -3 * 3600e3) t.setDate(t.getDate() + 7);
      return t;
    };
    var tick = function () {
      var now = new Date();
      var diff = nextDrop(now) - now;
      if (diff <= 0) {
        cd.classList.add('is-live');
        label.textContent = 'De drop is nu live in de winkel';
        boxes.hidden = true;
        return;
      }
      cd.classList.remove('is-live');
      label.textContent = 'Volgende drop over';
      boxes.hidden = false;
      var sec = Math.floor(diff / 1000);
      var days = Math.floor(sec / 86400);
      cd.querySelector('[data-cd="d"]').textContent = days;
      cd.querySelector('[data-cd-dl]').textContent = days === 1 ? 'dag' : 'dagen';
      cd.querySelector('[data-cd="h"]').textContent = pad(Math.floor(sec % 86400 / 3600));
      cd.querySelector('[data-cd="m"]').textContent = pad(Math.floor(sec % 3600 / 60));
      cd.querySelector('[data-cd="s"]').textContent = pad(sec % 60);
    };
    cd.hidden = false;
    tick();
    setInterval(tick, 1000);
  }
})();
