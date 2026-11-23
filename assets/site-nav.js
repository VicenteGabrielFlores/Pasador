(function () {
  var nav = document.getElementById('navbar');
  var btn = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (!nav || !links) return;

  function setOpen(open) {
    if (!btn) return;
    links.classList.toggle('open', open);
    btn.classList.toggle('active', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    var openLabel = btn.getAttribute('data-label-open') || 'Open menu';
    var closeLabel = btn.getAttribute('data-label-close') || 'Close menu';
    btn.setAttribute('aria-label', open ? closeLabel : openLabel);
  }

  function closeGroups(except) {
    nav.querySelectorAll('.nav-group.is-open').forEach(function (group) {
      if (group === except) return;
      group.classList.remove('is-open');
      var trigger = group.querySelector('.nav-group-btn');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    });
  }

  if (btn && !btn.dataset.navBound) {
    btn.dataset.navBound = '1';
    btn.addEventListener('click', function (event) {
      event.stopImmediatePropagation();
      setOpen(!links.classList.contains('open'));
    }, true);
  }

  nav.querySelectorAll('.nav-group-btn').forEach(function (trigger) {
    trigger.addEventListener('click', function (event) {
      event.stopImmediatePropagation();
      var group = trigger.parentElement;
      var willOpen = !group.classList.contains('is-open');
      closeGroups(willOpen ? group : null);
      group.classList.toggle('is-open', willOpen);
      trigger.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    closeGroups(null);
    if (links.classList.contains('open')) {
      setOpen(false);
      if (btn) btn.focus();
    }
  });

  document.addEventListener('click', function (event) {
    if (!nav.contains(event.target)) closeGroups(null);
  });

  links.querySelectorAll('a').forEach(function (anchor) {
    anchor.addEventListener('click', function () {
      closeGroups(null);
      setOpen(false);
    });
  });

  var path = location.pathname.replace(/\/index\.html$/, '/');
  if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
  nav.querySelectorAll('a[href]').forEach(function (anchor) {
    var href = anchor.getAttribute('href');
    if (!href || href.charAt(0) === '#') return;
    var target = href.split('#')[0];
    if (target === path) anchor.setAttribute('aria-current', 'page');
  });

  if (!document.documentElement.dataset.navScrollBound) {
    document.documentElement.dataset.navScrollBound = '1';
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }
})();
