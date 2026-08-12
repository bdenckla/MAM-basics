// Client-side column sorting for the supplied-marks punctuation table
// (supplied-marks.html). The table is <table class="goerwitz-obs-tree-table">;
// its first row holds the headers, four of which (Verse, Strand, Mark, Change)
// carry class "goerwitz-tms-sortable". Clicking such a header sorts the data
// rows by that column, toggling ascending/descending and recording the state in
// the header's aria-sort attribute (the stylesheet draws the ▲/▼ from it).
//
// The sort key is the cell's data-sort attribute when present (the Verse column
// supplies a canonical "rank-chapter-verse" key so G < E < D sorts by passage,
// not alphabetically), else its text. The sort is stable and the table ships in
// canonical order, so ties keep their verse order. With no JS the table is just
// the static, canonically-ordered table.
(function () {
  "use strict";

  // Header rows hold <th> only; data rows hold <td>.
  function dataRows(table) {
    var rows = Array.prototype.slice.call(table.rows);
    return rows.filter(function (row) {
      return row.querySelector("td");
    });
  }

  function sortKey(row, colIndex) {
    var cell = row.cells[colIndex];
    if (!cell) {
      return "";
    }
    var key = cell.dataset.sort;
    return (key !== undefined ? key : cell.textContent).trim();
  }

  function sortByColumn(table, header) {
    var colIndex = header.cellIndex;
    var ascending = header.getAttribute("aria-sort") !== "ascending";

    table.querySelectorAll("th.goerwitz-tms-sortable").forEach(function (th) {
      th.removeAttribute("aria-sort");
    });
    header.setAttribute("aria-sort", ascending ? "ascending" : "descending");

    var rows = dataRows(table);
    rows.sort(function (a, b) {
      var cmp = sortKey(a, colIndex).localeCompare(sortKey(b, colIndex), undefined, {
        numeric: true,
        sensitivity: "base",
      });
      return ascending ? cmp : -cmp;
    });
    rows.forEach(function (row) {
      row.parentNode.appendChild(row);
    });
  }

  function init() {
    var table = document.querySelector("table.goerwitz-obs-tree-table");
    if (!table) {
      return;
    }
    table.querySelectorAll("th.goerwitz-tms-sortable").forEach(function (header) {
      header.addEventListener("click", function () {
        sortByColumn(table, header);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
