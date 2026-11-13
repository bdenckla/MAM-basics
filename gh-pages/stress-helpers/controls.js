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
const menu = document.querySelector("#filter");
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
            || (menu.value && row.dataset.filter !== menu.value);
        if (!row.hidden) count++;
    }
    visible.textContent = count + (count === 1 ? " difference" : " differences");
}
input.addEventListener("input", filter);
menu.addEventListener("change", filter);
filter();
