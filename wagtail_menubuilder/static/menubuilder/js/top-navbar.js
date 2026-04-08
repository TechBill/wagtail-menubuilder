(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {

    // ── Mobile hamburger ───────────────────────────────────────────────────
    var hamburger = document.getElementById('wm-hamburger');
    var navMenu   = document.getElementById('wm-nav-menu');

    if (hamburger && navMenu) {
      hamburger.addEventListener('click', function () {
        var expanded = hamburger.getAttribute('aria-expanded') === 'true';
        hamburger.setAttribute('aria-expanded', String(!expanded));
        navMenu.classList.toggle('active', !expanded);
      });
    }

    // ── Dropdown toggles ───────────────────────────────────────────────────
    document.querySelectorAll('.nav-dropdown-toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var expanded = btn.getAttribute('aria-expanded') === 'true';

        // Close all other open dropdowns first
        document.querySelectorAll('.nav-dropdown-toggle[aria-expanded="true"]').forEach(function (other) {
          if (other !== btn) {
            other.setAttribute('aria-expanded', 'false');
            other.closest('.has-dropdown').classList.remove('open');
          }
        });

        btn.setAttribute('aria-expanded', String(!expanded));
        btn.closest('.has-dropdown').classList.toggle('open', !expanded);
      });
    });

    // ── Close dropdowns when clicking outside ──────────────────────────────
    document.addEventListener('click', function () {
      document.querySelectorAll('.nav-dropdown-toggle[aria-expanded="true"]').forEach(function (btn) {
        btn.setAttribute('aria-expanded', 'false');
        btn.closest('.has-dropdown').classList.remove('open');
      });
    });

    // ── Close on Escape ────────────────────────────────────────────────────
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        document.querySelectorAll('.nav-dropdown-toggle[aria-expanded="true"]').forEach(function (btn) {
          btn.setAttribute('aria-expanded', 'false');
          btn.closest('.has-dropdown').classList.remove('open');
          btn.focus();
        });
      }
    });

  });
})();
