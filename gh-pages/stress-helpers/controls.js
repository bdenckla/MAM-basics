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

const toggle = document.querySelector("#toggle-images");
const crops = document.querySelectorAll("#observations .scan");
toggle.addEventListener("click", () => {
    const show = toggle.getAttribute("aria-expanded") === "false";
    for (const cell of crops) cell.hidden = !show;
    toggle.textContent = show ? "Hide images" : "Show images";
    toggle.setAttribute("aria-expanded", show);
});

const input = document.querySelector("#find");
const edition = document.querySelector("#edition");
const outcome = document.querySelector("#outcome");
const visible = document.querySelector("#visible");
const rows = Array.from(document.querySelectorAll("#observations tbody tr"));
function searchKey(text) {
    return text.toLowerCase().replace(/[\u0591-\u05bd\u05bf-\u05c7]/g, "");
}
const searchable = rows.map(row => Array.from(row.cells, cell => searchKey(cell.textContent)));
function filter() {
    const query = searchKey(input.value.trim());
    let count = 0;
    for (const [index, row] of rows.entries()) {
        row.hidden = !searchable[index].some(cell => cell.includes(query))
            || (edition.value && row.dataset.edition !== edition.value)
            || (outcome.value && row.dataset.outcome !== outcome.value);
        if (!row.hidden) count++;
    }
    visible.textContent = count + (count === 1 ? " difference" : " differences");
}
input.addEventListener("input", filter);
edition.addEventListener("change", filter);
outcome.addEventListener("change", filter);
filter();
