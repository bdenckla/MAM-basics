/* The view control of the side-by-side pages of the Introduction to MAM.
   Source of truth: py/mb_misc/he_en_view.js in MAM-basics; copied verbatim beside
   the pages by styles_authored.make_js_file_for_he_en_view(). Edit this source and
   regenerate; do not edit deployed copies.

   Each page loads this script right after its control, at the top of its body, so the
   view is chosen before the page's tables are parsed. The view is body's data-view:
   "he", "en" or "both", which style.css reads to show Hebrew, English or both. The
   address's ?view=he, ?view=en or ?view=both chooses it; any other address shows both,
   as the page does where this script never runs. A button changes the view, keeping in
   place the first row of the tables in sight, and names the view in the address with
   history.replaceState. Nothing is stored. */
(function () {
  "use strict";
  const VIEWS = ["he", "en", "both"];
  const control = document.getElementById("he-en-view");
  const buttons = control.querySelectorAll("button[data-view]");

  function show(view) {
    document.body.setAttribute("data-view", view);
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.view === view));
    }
  }

  // The first row of the tables that is in sight below the control, and its top's
  // offset in the window. A label row is passed over, since the Hebrew view hides it.
  function placeInSight() {
    const edge = control.getBoundingClientRect().bottom;
    const rows = document.querySelectorAll(
      "table.he-en > tbody > tr:not(.he-en-label)"
    );
    for (const row of rows) {
      const box = row.getBoundingClientRect();
      if (box.bottom > edge) {
        return box.top < window.innerHeight ? { row: row, top: box.top } : null;
      }
    }
    return null;
  }

  function choose(view) {
    const place = placeInSight();
    show(view);
    if (place) {
      window.scrollBy(0, place.row.getBoundingClientRect().top - place.top);
    }
    const address = new URL(window.location.href);
    address.searchParams.set("view", view);
    try {
      history.replaceState(history.state, "", address.href);
    } catch (error) {
      // A browser that will not rewrite this address keeps the old one; the view on
      // screen has already changed.
    }
  }

  control.addEventListener("click", function (event) {
    const button = event.target.closest("button[data-view]");
    if (button) {
      choose(button.dataset.view);
    }
  });
  const asked = new URLSearchParams(window.location.search).get("view");
  show(VIEWS.includes(asked) ? asked : "both");
  control.hidden = false;
})();
