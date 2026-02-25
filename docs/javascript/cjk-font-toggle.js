(function() {
  // Restore saved preference before first paint (runs as soon as script loads in head)
  try {
    if (localStorage.getItem('cjkFont') === 'tc') {
      document.documentElement.classList.add('font-chinese-tc');
    }
  } catch (e) {}

  var root = document.documentElement;

  function isTC() {
    return root.classList.contains('font-chinese-tc');
  }

  function setTC(tc) {
    if (tc) {
      root.classList.add('font-chinese-tc');
      try { localStorage.setItem('cjkFont', 'tc'); } catch (e) {}
    } else {
      root.classList.remove('font-chinese-tc');
      try { localStorage.setItem('cjkFont', 'sc'); } catch (e) {}
    }
    updateButtons();
  }

  function updateButtons() {
    // Button shows the *other* option: 繁 when simplified is active, 简 when traditional is active
    var label = isTC() ? '简' : '繁';
    var title = isTC() ? 'Switch to Simplified' : 'Switch to Traditional';
    ['cjk-font-toggle', 'cjk-font-toggle-mobile'].forEach(function(id) {
      var el = document.getElementById(id);
      if (el) {
        el.textContent = label;
        el.title = title;
        el.setAttribute('aria-label', title);
      }
    });
  }

  function init() {
    updateButtons();
    ['cjk-font-toggle', 'cjk-font-toggle-mobile'].forEach(function(id) {
      var el = document.getElementById(id);
      if (el) {
        el.addEventListener('click', function() {
          setTC(!isTC());
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
