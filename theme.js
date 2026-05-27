/* theme.js — dark/light mode toggle.
 *
 * The default is the OS preference (handled in CSS via prefers-color-scheme).
 * This script adds a manual override on top: a floating button that flips the
 * theme, remembers the choice in localStorage, and writes it to
 * <html data-theme="…">. The matching anti-flash snippet in each page's <head>
 * applies a stored choice before first paint so there's no flicker.
 *
 * With no stored choice the button just mirrors (and lets you flip) the current
 * OS theme, and it keeps in sync if the OS theme changes. */
(function () {
  'use strict';

  var KEY = 'theme';
  var root = document.documentElement;
  var mql = window.matchMedia('(prefers-color-scheme: dark)');

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return v === 'dark' || v === 'light' ? v : null;
    } catch (e) {
      return null;
    }
  }

  function effective() {
    return stored() || (mql.matches ? 'dark' : 'light');
  }

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'theme-toggle';

  function reflect(theme) {
    var dark = theme === 'dark';
    var label = dark ? 'Switch to light mode' : 'Switch to dark mode';
    btn.textContent = dark ? '☀' : '☾'; // ☀ / ☾
    btn.setAttribute('aria-label', label);
    btn.title = label;
    btn.setAttribute('aria-pressed', String(dark));
  }

  function set(theme) {
    root.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(KEY, theme);
    } catch (e) {}
    reflect(theme);
  }

  btn.addEventListener('click', function () {
    set(effective() === 'dark' ? 'light' : 'dark');
  });

  // If the visitor hasn't pinned a choice, follow OS changes live.
  mql.addEventListener('change', function () {
    if (!stored()) reflect(effective());
  });

  function init() {
    document.body.appendChild(btn);
    reflect(effective());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
