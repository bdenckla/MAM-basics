const slider = document.querySelector("#hebrew-size");
const sizeValue = document.querySelector("#size-value");
function applySize() {
    document.documentElement.style.setProperty("--hebrew-size", slider.value + "px");
    sizeValue.textContent = slider.value + " px";
}
slider.addEventListener("input", applySize);
document.querySelector("#size-reset").addEventListener("click", () => {
    slider.value = slider.defaultValue;
    applySize();
});
applySize();

// A page rendered without crops has no button.
const toggle = document.querySelector("#toggle-images");
if (toggle) {
    const crops = document.querySelectorAll("#observations .scan");
    toggle.addEventListener("click", () => {
        const show = toggle.getAttribute("aria-expanded") === "false";
        for (const cell of crops) cell.hidden = !show;
        toggle.textContent = show ? "Hide images" : "Show images";
        toggle.setAttribute("aria-expanded", show);
    });
}

const input = document.querySelector("#find");
const menu = document.querySelector("#filter");
const batchMenu = document.querySelector("#batch");
const visible = document.querySelector("#visible");
const rows = Array.from(document.querySelectorAll("#observations tbody tr"));
function searchKey(text) {
    return text.toLowerCase().replace(/[\u0591-\u05bd\u05bf-\u05c7]/g, "");
}
const searchable = rows.map(row => Array.from(row.cells, cell => searchKey(cell.textContent)));
// Each menu counts the rows that the other menu's choice leaves, and greys out a choice
// that would leave none.  The search box affects only the table and the readout.
function recount(target, key, other, otherKey) {
    const pool = rows.filter(row => !other.value || row.dataset[otherKey] === other.value);
    for (const option of target.options) {
        const count = option.value
            ? pool.filter(row => row.dataset[key] === option.value).length
            : pool.length;
        option.textContent = `${option.dataset.label} (${count})`;
        option.disabled = option.value !== "" && count === 0;
    }
}
function filter() {
    const query = searchKey(input.value.trim());
    let count = 0;
    for (const [index, row] of rows.entries()) {
        row.hidden = !searchable[index].some(cell => cell.includes(query))
            || (menu.value && row.dataset.filter !== menu.value)
            || (batchMenu.value && row.dataset.batch !== batchMenu.value);
        if (!row.hidden) count++;
    }
    visible.textContent = count + (count === 1 ? " difference" : " differences");
}
// A menu's choice changes the other menu's counts as well as the table.
function choose() {
    recount(menu, "filter", batchMenu, "batch");
    recount(batchMenu, "batch", menu, "filter");
    filter();
}
input.addEventListener("input", filter);
menu.addEventListener("change", choose);
batchMenu.addEventListener("change", choose);
choose();
