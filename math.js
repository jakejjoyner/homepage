/* math.js: render LaTeX on any page of the site, as native MathML (no stylesheet).
 *
 * Every page loads it with  <script defer src="/math.js"></script>  in its <head>; new blog posts copy that line from
 * an existing post. (jakejoyner.com is served straight from the repository files, so nothing can be added at deploy time.)
 * It downloads the Temml library (temml.min.js, MIT, github.com/ronkok/Temml) only when a page contains math.
 *
 * Delimiters:  $...$  and  \(...\)  inline;   $$...$$  and  \[...\]  on their own line (display).
 * A single $ only counts when it hugs the formula, so "$5 and $10" is left alone. Write \$ for a literal dollar sign.
 * Text inside <code>, <pre>, <script>, <style>, <textarea> and existing <math> is never touched.
 */
(function () {
  'use strict';
  var SRC = new URL('temml.min.js', document.currentScript.src).href;
  var MATH = /\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?![\d$])/;
  var SKIP = 'script,style,code,pre,textarea,math';
  var loading = null;

  // plain text between formulas: escape for HTML, and turn \$ into a literal dollar sign
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\\\$/g, '$'); }

  function typeset(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), nodes = [], n;
    while ((n = walker.nextNode())) {
      if ((MATH.test(n.nodeValue) || n.nodeValue.indexOf('\\$') >= 0) && !n.parentElement.closest(SKIP)) nodes.push(n);
    }
    nodes.forEach(function (node) {
      var re = new RegExp(MATH.source, 'g'), s = node.nodeValue, html = '', last = 0, m;
      while ((m = re.exec(s))) {
        var display = m[1] !== undefined || m[2] !== undefined;
        var tex = m[1] || m[2] || m[3] || m[4];
        html += esc(s.slice(last, m.index));
        try {
          html += window.temml.renderToString(tex, { displayMode: display, throwOnError: false });
        } catch (e) {
          html += esc(m[0]);                    // leave the source visible if it cannot be parsed
        }
        last = m.index + m[0].length;
      }
      html += esc(s.slice(last));
      var t = document.createElement('template');
      t.innerHTML = html;
      node.replaceWith(t.content);
    });
  }

  function go(root) {
    if (!root || !(MATH.test(root.textContent) || root.textContent.indexOf('\\$') >= 0)) return;
    if (window.temml) return typeset(root);
    loading = loading || new Promise(function (ok, fail) {
      var s = document.createElement('script');
      s.src = SRC; s.onload = ok; s.onerror = fail;
      document.head.appendChild(s);
    });
    loading.then(function () { typeset(root); }, function () {});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { go(document.body); });
  else go(document.body);
  document.addEventListener('md:rendered', function (e) { go(e.target); });   // blog posts, after md.js fills them in
})();
