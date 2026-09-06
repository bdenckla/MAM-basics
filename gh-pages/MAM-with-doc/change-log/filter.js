(function() {
  var activeFilters = new Set();
  var cards = document.querySelectorAll('.diff-card');
  var buttons = document.querySelectorAll('.filter-btn');
  var summaryRows = document.querySelectorAll('table.summary tr[data-cat]');
  var bookHeaders = document.querySelectorAll('.book-header');
  var catLabels = {};
  summaryRows.forEach(function(r) {
    var cat = r.getAttribute('data-cat');
    var td = r.querySelectorAll('td')[1];
    if (cat && td) catLabels[cat] = td.textContent;
  });
  function filterSuffix() {
    if (activeFilters.size === 0) return '';
    if (activeFilters.size === 1) {
      var cat = activeFilters.values().next().value;
      var label = catLabels[cat] || cat;
      return ' diffs are of type “' + label + '”';
    }
    return ' diffs are of the selected categories';
  }
  function update() {
    var suffix = filterSuffix();
    cards.forEach(function(card) {
      var cat = card.getAttribute('data-categories');
      card.classList.toggle('hidden',
        activeFilters.size > 0 && !activeFilters.has(cat));
    });
    bookHeaders.forEach(function(hdr) {
      var next = hdr.nextElementSibling;
      var visCount = 0;
      while (next && !next.classList.contains('book-header')) {
        if (next.classList.contains('diff-card') && !next.classList.contains('hidden')) {
          visCount++;
        }
        next = next.nextElementSibling;
      }
      hdr.classList.toggle('hidden', visCount === 0);
      var span = hdr.querySelector('.book-count');
      if (span) {
        var total = parseInt(hdr.getAttribute('data-total'), 10);
        if (activeFilters.size === 0) {
          span.textContent = total + (total === 1 ? ' diff' : ' diffs');
        } else {
          span.textContent = visCount + ' of ' + total + suffix;
        }
      }
    });
  }
  function toggleFilter(cat) {
    if (activeFilters.has(cat)) activeFilters.delete(cat);
    else activeFilters.add(cat);
    buttons.forEach(function(b) {
      b.classList.toggle('active', activeFilters.has(b.getAttribute('data-cat')));
    });
    summaryRows.forEach(function(r) {
      r.classList.toggle('active', activeFilters.has(r.getAttribute('data-cat')));
    });
    update();
  }
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var cat = btn.getAttribute('data-cat');
      if (cat) toggleFilter(cat);
    });
  });
  summaryRows.forEach(function(row) {
    row.addEventListener('click', function() {
      var cat = row.getAttribute('data-cat');
      if (cat) toggleFilter(cat);
    });
  });
  var showAll = document.getElementById('show-all-btn');
  if (showAll) {
    showAll.addEventListener('click', function() {
      activeFilters.clear();
      buttons.forEach(function(b) { b.classList.remove('active'); });
      summaryRows.forEach(function(r) { r.classList.remove('active'); });
      update();
    });
  }
})();