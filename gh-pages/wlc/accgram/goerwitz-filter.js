// Client-side filtering for the Goerwitz ungrammatical-verse report (goerwitz.html).
//
// Each verse is a <section class="goerwitz-verse"> tagged with data-category
// ("msp" = missing sof pasuq, "msl" = missing silluq, "zwhim" = zarqa whim,
// "other"), data-source ("wlc", "bhs" = BHS/BHQ, "lc", "tbd" = unclear/TBD),
// plus two boolean flags, data-uchange and data-wnote ("1"/"0"), for whether the
// verse has a UXLC change and a WLC bracket-note.
//
// The grammar-error checkboxes (.gf-category) and the source checkboxes
// (.gf-source) each select which of their values show; a verse must match a
// checked box in BOTH groups. Two tri-state radio groups (.gf-uchange,
// .gf-wnote) further constrain the list, ANDed with the checkboxes: each is
// "yes" (has), "no" (doesn't have), or "any" (don't care). .gf-count reports how
// many verses are currently visible.
//
// Every option label ends in a .gf-opt-count span (except each group's "don't
// care" radio). Each is recomputed live to the number of CURRENTLY-VISIBLE
// verses matching that option, so the counts always sum to what the page shows:
// an unchecked checkbox, or a radio option the active filters exclude, reads 0
// and renders empty (no "(0)"). The spans the Python writes are the no-JS
// fallback.
(function () {
  "use strict";

  function checkedValues(selector) {
    var values = new Set();
    document.querySelectorAll(selector).forEach(function (input) {
      if (input.checked) {
        values.add(input.value);
      }
    });
    return values;
  }

  function radioValue(name) {
    var checked = document.querySelector(
      'input[name="' + name + '"]:checked'
    );
    return checked ? checked.value : "any";
  }

  // want: "yes" | "no" | "any"; flag: the verse's "1"/"0" data attribute.
  function flagMatches(want, flag) {
    if (want === "yes") {
      return flag === "1";
    }
    if (want === "no") {
      return flag === "0";
    }
    return true;
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
  // equals each input's wanted value, and write it into that input's count span.
  // `valueFor` maps an input to the data-attribute value it represents (a radio
  // returning null carries no count and is skipped).
  function updateOptionCounts(selector, dataKey, visible, valueFor) {
    document.querySelectorAll(selector).forEach(function (input) {
      var wanted = valueFor(input);
      if (wanted === null) {
        return;
      }
      var count = 0;
      visible.forEach(function (verse) {
        if (verse.dataset[dataKey] === wanted) {
          count += 1;
        }
      });
      setOptCount(input, count);
    });
  }

  // The data-attribute value a tri-state radio represents: "1"/"0" for has/
  // doesn't-have, or null for "don't care" (which shows no count).
  function radioWanted(input) {
    if (input.value === "yes") {
      return "1";
    }
    if (input.value === "no") {
      return "0";
    }
    return null;
  }

  function applyFilters() {
    var categories = checkedValues("input.gf-category");
    var sources = checkedValues("input.gf-source");
    var wantUchange = radioValue("gf-uchange");
    var wantWnote = radioValue("gf-wnote");
    var verses = document.querySelectorAll("section.goerwitz-verse");

    function passesCategory(verse) {
      return categories.has(verse.dataset.category);
    }
    function passesSource(verse) {
      return sources.has(verse.dataset.source);
    }
    function passesUchange(verse) {
      return flagMatches(wantUchange, verse.dataset.uchange);
    }
    function passesWnote(verse) {
      return flagMatches(wantWnote, verse.dataset.wnote);
    }

    var visible = [];
    verses.forEach(function (verse) {
      var isVisible =
        passesCategory(verse) &&
        passesSource(verse) &&
        passesUchange(verse) &&
        passesWnote(verse);
      verse.style.display = isVisible ? "" : "none";
      if (isVisible) {
        visible.push(verse);
      }
    });

    // Every option's count is the number of currently-visible verses matching
    // it, so the counts always sum to what the page shows.
    updateOptionCounts("input.gf-category", "category", visible, function (i) {
      return i.value;
    });
    updateOptionCounts("input.gf-source", "source", visible, function (i) {
      return i.value;
    });
    updateOptionCounts("input.gf-uchange", "uchange", visible, radioWanted);
    updateOptionCounts("input.gf-wnote", "wnote", visible, radioWanted);

    var countEl = document.querySelector(".gf-count");
    if (countEl) {
      countEl.textContent =
        "Showing " + visible.length + " of " + verses.length + " verses";
    }
  }

  function init() {
    var inputs = document.querySelectorAll(
      "input.gf-category, input.gf-source, input.gf-uchange, input.gf-wnote"
    );
    inputs.forEach(function (input) {
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
