(() => {
  const activeFilterIds = new Set();
  const cards = Array.from(document.querySelectorAll('.record-card'));
  const sourceEmails = Array.from(document.querySelectorAll('.source-email'));
  const summaryRows = Array.from(document.querySelectorAll('.summary tr[data-filter-id]'));
  const visibleFilteredCountEl = document.getElementById('visible-filtered-count');

  function filterIdsOf(element) {
    return (element.dataset.filterIds || '').split(/\s+/).filter(Boolean);
  }

  function isVisible(element) {
    if (activeFilterIds.size === 0) return true;
    return filterIdsOf(element).some((id) => activeFilterIds.has(id));
  }

  function updateVisibility() {
    let visibleCount = 0;
    for (const card of cards) {
      const visible = isVisible(card);
      card.classList.toggle('hidden', !visible);
      if (visible) visibleCount += 1;
    }

    // The source-email blocks answer "which message did this come from", so a
    // filter that hides every case from a message hides the message too. A
    // message that survives still lists every case it raised, so the links to
    // the ones now hidden are struck through and made inert rather than
    // removed: the list states what the message contained.
    for (const sourceEmail of sourceEmails) {
      sourceEmail.classList.toggle('hidden', !isVisible(sourceEmail));
      for (const link of sourceEmail.querySelectorAll('a.case-link')) {
        const target = document.getElementById(link.getAttribute('href').slice(1));
        link.classList.toggle('unreachable', !target || target.classList.contains('hidden'));
      }
    }

    if (visibleFilteredCountEl) {
      visibleFilteredCountEl.textContent = `${visibleCount}/${cards.length - visibleCount}`;
    }

    for (const row of summaryRows) {
      row.classList.toggle('active', activeFilterIds.has(row.dataset.filterId));
    }
  }

  function toggleFilter(filterId) {
    if (activeFilterIds.has(filterId)) {
      activeFilterIds.delete(filterId);
    } else {
      activeFilterIds.add(filterId);
    }
    updateVisibility();
  }

  for (const row of summaryRows) {
    row.addEventListener('click', () => toggleFilter(row.dataset.filterId));
  }

  updateVisibility();
})();
