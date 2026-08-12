// Client-side filtering for the poetic ungrammatical-verse report (poetic.html).
//
// Each verse is a <section class="goerwitz-verse"> tagged with data-kind
// ("missing_silluq" | "no_parse"), data-book ("ps" | "pr" | "jb"), and
// data-agree ("agree" | "differ" | "na"), the last comparing the WLC and
// MAM-simple disjunctive skeletons ("na" = the verse is not in MAM-simple).
//
// Each facet is a group of checkboxes (.pf-kind, .pf-book, .pf-agree) selecting
// which of its values show; a verse must match a checked box in EVERY group.
// .pf-count reports how many verses are currently visible. Every option label
// ends in a .gf-opt-count span recomputed live to the number of
// currently-visible verses matching that option (a zero renders empty); the
// spans the Python writes are the no-JS fallback. This mirrors
// goerwitz-filter.js, restricted to the all-checkbox case.
(function () {
  "use strict";

  // Each filter group: the checkbox class and the data-* attribute it gates.
  var GROUPS = [
    { selector: "input.pf-kind", dataKey: "kind" },
    { selector: "input.pf-book", dataKey: "book" },
    { selector: "input.pf-agree", dataKey: "agree" },
  ];

  function checkedValues(selector) {
    var values = new Set();
    document.querySelectorAll(selector).forEach(function (input) {
      if (input.checked) {
        values.add(input.value);
      }
    });
    return values;
  }

  // The "(N)" a count span shows; zero renders empty (no "(0)").
  function countText(count) {
    return count ? " (" + count + ")" : "";
  }

  // Write `count` into the .gf-opt-count span inside an input's <label>.
  function setOptCount(input, count) {
    var label = input.closest("label");
    var span = label && label.querySelector(".gf-opt-count");
    if (span) {
      span.textContent = countText(count);
    }
  }

  // Count, among the currently-visible verses, those whose dataKey attribute
  // equals each input's value, and write it into that input's count span.
  function updateOptionCounts(selector, dataKey, visible) {
    document.querySelectorAll(selector).forEach(function (input) {
      var count = 0;
      visible.forEach(function (verse) {
        if (verse.dataset[dataKey] === input.value) {
          count += 1;
        }
      });
      setOptCount(input, count);
    });
  }

  function applyFilters() {
    var wanted = GROUPS.map(function (group) {
      return { dataKey: group.dataKey, values: checkedValues(group.selector) };
    });
    var verses = document.querySelectorAll("section.goerwitz-verse");

    var visible = [];
    verses.forEach(function (verse) {
      var isVisible = wanted.every(function (group) {
        return group.values.has(verse.dataset[group.dataKey]);
      });
      verse.style.display = isVisible ? "" : "none";
      if (isVisible) {
        visible.push(verse);
      }
    });

    GROUPS.forEach(function (group) {
      updateOptionCounts(group.selector, group.dataKey, visible);
    });

    var countEl = document.querySelector(".pf-count");
    if (countEl) {
      countEl.textContent =
        "Showing " + visible.length + " of " + verses.length + " verses";
    }
  }

  function init() {
    var selectors = GROUPS.map(function (group) {
      return group.selector;
    }).join(", ");
    document.querySelectorAll(selectors).forEach(function (input) {
      input.addEventListener("change", applyFilters);
    });
    applyFilters();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
