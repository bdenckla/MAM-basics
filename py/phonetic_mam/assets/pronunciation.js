"use strict";

(() => {
    const choices = Array.from(document.querySelectorAll('input[name="pronunciation"]'));
    const links = Array.from(document.querySelectorAll("a[data-pronunciation-link]"));
    const allowed = new Set(["sephardic", "ashkenazic"]);

    function select(pronunciation, replaceURL) {
        for (const choice of choices) {
            choice.checked = choice.value === pronunciation;
        }
        // style.css's fallback for a browser without :has().
        document.body.classList.toggle("ashkenazic-selected", pronunciation === "ashkenazic");
        if (replaceURL) {
            const current = new URL(window.location.href);
            current.searchParams.set("pronunciation", pronunciation);
            window.history.replaceState(window.history.state, "", current.href);
        }
        for (const link of links) {
            const target = new URL(link.getAttribute("href"), document.baseURI);
            target.searchParams.set("pronunciation", pronunciation);
            link.setAttribute("href", target.href);
        }
    }

    function readURL() {
        const values = new URL(window.location.href).searchParams.getAll("pronunciation");
        const valid = values.length === 1 && allowed.has(values[0]);
        select(valid ? values[0] : "sephardic", !valid);
    }

    for (const choice of choices) {
        choice.addEventListener("change", () => {
            if (choice.checked && allowed.has(choice.value)) {
                select(choice.value, true);
            }
        });
    }
    window.addEventListener("popstate", readURL);
    readURL();
})();
