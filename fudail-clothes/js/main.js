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
})();
