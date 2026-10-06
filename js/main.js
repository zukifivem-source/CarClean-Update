/* CarClean Midden-Groningen: site behaviour. No dependencies, ~4 KB gzipped.
   Every feature checks for its own markup, so one file serves all pages. */
(function () {
  'use strict';
  var d = document;
  var root = d.documentElement;
  root.classList.add('js');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (sel, ctx) { return (ctx || d).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || d).querySelectorAll(sel)); };
  var euro = function (n) {
    return '€' + n.toLocaleString('nl-NL', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 });
  };
  var store = {
    set: function (k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
    get: function (k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } },
    del: function (k) { try { sessionStorage.removeItem(k); } catch (e) { /* ignore */ } }
  };

  /* 1. Header state on scroll ------------------------------------------- */
  var header = $('[data-header]');
  if (header) {
    var ticking = false;
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
    }, { passive: true });
    onScroll();
  }

  /* 2. Mobile menu -------------------------------------------------------- */
  var toggle = $('[data-menu-toggle]');
  var menu = $('[data-menu]');
  if (toggle && menu) {
    var setMenu = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('is-open', open);
      d.body.classList.toggle('menu-open', open);
      if (open) { var first = $('a', menu); if (first) first.focus(); }
    };
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); toggle.focus(); }
    });
    var mq = window.matchMedia('(min-width: 1040px)');
    var onMq = function (e) { if (e.matches) setMenu(false); };
    if (mq.addEventListener) mq.addEventListener('change', onMq); else if (mq.addListener) mq.addListener(onMq);
  }

  /* 3. Reveal on scroll + count-up ---------------------------------------- */
  var countUp = function (el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduceMotion || !target) return;
    var start = null;
    var dur = 1400;
    var step = function (t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString('nl-NL') + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  var revealEls = $$('.reveal');
  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (el.hasAttribute('data-delay')) el.style.setProperty('--d', el.getAttribute('data-delay') + 'ms');
        el.classList.add('is-in');
        if (el.hasAttribute('data-count')) countUp(el);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealEls.concat(counters).forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* 4. Live opening status (Europe/Amsterdam) ------------------------------ */
  var statusEls = $$('[data-open-status]');
  var hours = $('[data-hours]');
  if (statusEls.length || hours) {
    var OPEN = 8 * 60, CLOSE = 17 * 60;
    var now = (function () {
      try {
        var parts = new Intl.DateTimeFormat('en-GB', {
          timeZone: 'Europe/Amsterdam', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
        }).formatToParts(new Date());
        var get = function (t) { return (parts.filter(function (p) { return p.type === t; })[0] || {}).value; };
        var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
        return { day: day, min: parseInt(get('hour'), 10) * 60 + parseInt(get('minute'), 10) };
      } catch (e) {
        var n = new Date();
        return { day: n.getDay(), min: n.getHours() * 60 + n.getMinutes() };
      }
    })();
    var weekday = now.day >= 1 && now.day <= 5;
    var isOpen = weekday && now.min >= OPEN && now.min < CLOSE;
    var label;
    if (isOpen) label = 'Nu open · tot 17:00';
    else if (weekday && now.min < OPEN) label = 'Gesloten · opent om 08:00';
    else if (now.day >= 1 && now.day <= 4) label = 'Gesloten · morgen vanaf 08:00';
    else label = 'Gesloten · maandag vanaf 08:00';

    statusEls.forEach(function (el) {
      var dot = $('.dot', el);
      var txt = $('[data-open-text]', el);
      if (dot) dot.classList.add(isOpen ? 'dot--live' : 'dot--closed');
      if (txt) txt.textContent = label;
    });
    if (hours) {
      var row = $('[data-day="' + now.day + '"]', hours);
      if (row) row.classList.add('is-today');
    }
  }

  /* 5. Before/after compare slider ---------------------------------------- */
  $$('[data-compare]').forEach(function (box) {
    var range = $('[data-compare-range]', box);
    if (!range) return;
    var set = function () { box.style.setProperty('--pos', range.value + '%'); };
    range.addEventListener('input', set);
    set();
  });

  /* 6. Price calculator (services page) ----------------------------------- */
  var calc = $('[data-calc]');
  if (calc) {
    var sumEl = $('[data-calc-sum]', calc);
    var linesEl = $('[data-calc-lines]', calc);
    var linkEl = $('[data-calc-link]', calc);
    var update = function () {
      var pkg = $('input[name="pakket"]:checked', calc);
      var extras = $$('input[name="extra"]:checked', calc);
      var total = 0;
      var html = '';
      [pkg].concat(extras).forEach(function (inp) {
        if (!inp) return;
        var price = parseFloat(inp.getAttribute('data-price')) || 0;
        total += price;
        html += '<li><span>' + inp.getAttribute('data-label') + '</span><span>' +
          (price ? euro(price) : 'in overleg') + '</span></li>';
      });
      sumEl.textContent = euro(total);
      linesEl.innerHTML = html;
      var q = '?dienst=' + encodeURIComponent(pkg ? pkg.value : '');
      if (extras.length) q += '&extra=' + encodeURIComponent(extras.map(function (e) { return e.value; }).join(','));
      linkEl.setAttribute('href', linkEl.getAttribute('href').split('?')[0] + q);
    };
    calc.addEventListener('change', update);
    calc.addEventListener('submit', function (e) { e.preventDefault(); });
    update();
  }

  /* 7. Sub-navigation highlight (services page) --------------------------- */
  var subnav = $('[data-subnav]');
  if (subnav && 'IntersectionObserver' in window) {
    var links = $$('a', subnav);
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove('is-active'); });
        var a = byId[entry.target.id];
        if (a) {
          a.classList.add('is-active');
          var ul = subnav;
          ul.scrollTo({ left: a.offsetLeft - ul.clientWidth / 2 + a.clientWidth / 2, behavior: reduceMotion ? 'auto' : 'smooth' });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) { var s = d.getElementById(id); if (s) spy.observe(s); });
  }

  /* 7b. Old anchors (/diensten.html#boten etc.) → new section ids ------- */
  var legacy = { 'haal-breng': 'haal-en-breng', dealers: 'zakelijk', wagenpark: 'zakelijk', vracht: 'groot-materieel', boten: 'groot-materieel', agrarisch: 'groot-materieel' };
  var oldHash = location.hash.slice(1);
  if (legacy[oldHash] && !d.getElementById(oldHash)) {
    var target = d.getElementById(legacy[oldHash]);
    if (target) {
      history.replaceState(null, '', '#' + legacy[oldHash]);
      // wait for images/fonts so the offset is final
      window.addEventListener('load', function () { target.scrollIntoView(); });
    }
  }

  /* 8. Prefill forms from the URL ----------------------------------------- */
  var params = new URLSearchParams(location.search);
  var selectById = function (select, id) {
    if (!select || !id) return null;
    var opt = $('option[data-id="' + id.replace(/[^a-z0-9-]/gi, '') + '"]', select);
    if (opt) { select.value = opt.value; return opt; }
    return null;
  };
  var booking = $('#booking');
  if (booking) {
    var dienst = $('#dienst', booking);
    var hidden = $('[data-samenstelling]', booking);
    var chip = $('[data-summary]', booking);
    var extraIds = (params.get('extra') || '').split(',').filter(Boolean);
    var extraNames = { koplampen: 'koplampen polijsten', velgen: 'velgen coating', ozon: 'ozonbehandeling', remklauwen: 'remklauwen spuiten', haalbreng: 'haal & breng' };
    var extraLabels = extraIds.map(function (x) { return extraNames[x]; }).filter(Boolean);
    // The hidden field and chip always mirror the current select, plus any extras from the calculator
    var syncSummary = function () {
      var opt = dienst.options[dienst.selectedIndex];
      var summary = opt && opt.value ? opt.textContent + (extraLabels.length ? ' + ' + extraLabels.join(', ') : '') : '';
      hidden.value = summary;
      $('[data-summary-text]', chip).textContent = 'Gekozen: ' + summary + '. Je kunt dit hieronder nog aanpassen.';
      chip.classList.toggle('is-visible', !!summary && (fromUrl || extraLabels.length > 0));
    };
    var fromUrl = !!selectById(dienst, params.get('dienst'));
    dienst.addEventListener('change', syncSummary);
    syncSummary();
    // Date: no past dates; gentle note for weekends
    var date = $('[data-date-min]', booking);
    if (date) {
      var t = new Date();
      date.min = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
      var hint = $('[data-date-hint]', booking);
      var base = hint ? hint.textContent : '';
      date.addEventListener('change', function () {
        if (!hint || !date.value) return;
        var day = new Date(date.value + 'T12:00:00').getDay();
        hint.textContent = (day === 0 || day === 6)
          ? 'Dat is een weekenddag. Particulier? Dan stellen we samen een doordeweekse dag voor.'
          : base;
      });
    }
  }
  selectById($('[data-prefill="onderwerp"]'), params.get('onderwerp'));

  /* 9. Form validation + hand-off to the thank-you page ------------------- */
  $$('form[data-validate]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    var fields = $$('.field input, .field select, .field textarea', form);
    var check = function (el) {
      var ok = el.checkValidity();
      var field = el.closest('.field');
      if (field) field.classList.toggle('has-error', !ok);
      el.setAttribute('aria-invalid', String(!ok));
      return ok;
    };
    fields.forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value) check(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
      el.addEventListener('change', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
    });
    form.addEventListener('submit', function (e) {
      var firstBad = null;
      fields.forEach(function (el) { if (!check(el) && !firstBad) firstBad = el; });
      if (firstBad) {
        e.preventDefault();
        firstBad.focus({ preventScroll: true });
        (firstBad.closest('.field') || firstBad).scrollIntoView({ block: 'center', behavior: reduceMotion ? 'auto' : 'smooth' });
        return;
      }
      var name = (form.elements.naam && form.elements.naam.value || '').trim().split(/\s+/)[0];
      var svc = form.elements.dienst ? form.elements.dienst.value : '';
      store.set('cc-thanks', { name: name, service: svc, type: form.getAttribute('data-form-type') });
      var btn = $('button[type="submit"]', form);
      if (btn) {
        btn.setAttribute('data-label', btn.firstChild.textContent);
        btn.setAttribute('aria-busy', 'true');
        btn.firstChild.textContent = 'Versturen… ';
      }
    });
  });

  // Coming back with the Back button (bfcache) must not leave buttons stuck on "Versturen…"
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    $$('button[aria-busy="true"]').forEach(function (btn) {
      btn.removeAttribute('aria-busy');
      if (btn.hasAttribute('data-label')) btn.firstChild.textContent = btn.getAttribute('data-label');
    });
  });

  /* 10. Personalised thank-you ------------------------------------------- */
  var thanksName = $('[data-thanks-name]');
  if (thanksName) {
    var info = store.get('cc-thanks');
    if (info) {
      if (info.name) thanksName.textContent = ' ' + info.name.slice(0, 40);
      var lead = $('[data-thanks-lead]');
      if (lead && info.type === 'afspraak' && info.service) {
        lead.textContent = 'Je aanvraag voor “' + info.service.slice(0, 80) + '” staat genoteerd. Dit gebeurt er nu:';
      }
      store.del('cc-thanks');
    }
  }

  /* 11. Opened straight from disk (file://): folders don't auto-open index.html */
  if (location.protocol === 'file:') {
    var css = $('link[rel="stylesheet"][href$="style.css"]');
    if (css) {
      var embed = d.createElement('link');
      embed.rel = 'stylesheet';
      embed.href = css.getAttribute('href').replace('style.css', 'font-embed.css');
      d.head.appendChild(embed);
    }
    $$('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (/^[a-z]+:/i.test(href) || href.charAt(0) === '#') return;
      a.setAttribute('href', href.replace(/^([^?#]*\/)(?=[?#]|$)/, '$1index.html'));
    });
  }

  /* 12. Footer year -------------------------------------------------------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
