const fs = require("fs");
const vm = require("vm");
const input = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const rows = Array.from({length: input.buttons}, () => {
  const blocks = [{hidden: false}, {hidden: true}];
  const button = {
    textContent: "click to show English translation",
    handlers: [],
    parentElement: {querySelectorAll(selector) {
      assert(selector === ":scope > div", "wrong direct-child scope");
      return blocks;
    }},
    addEventListener(type, handler) {
      assert(type === "click", "unexpected event");
      this.handlers.push(handler);
    }
  };
  return {blocks, button};
});
vm.runInNewContext(input.script, {document: {querySelectorAll(selector) {
  assert(selector === "button.translation-toggle", "wrong button selector");
  return rows.map(row => row.button);
}}});
let clicks = 0;
for (let index = 0; index < rows.length; index++) {
  const {blocks, button} = rows[index];
  assert(button.handlers.length === 1, "handler registration mismatch");
  for (let state = 0; state < 2; state++) {
    button.handlers[0](); clicks++;
    assert(blocks[0].hidden === (state === 0), "Hebrew state mismatch");
    assert(blocks[1].hidden === (state === 1), "English state mismatch");
    assert(button.textContent === (state === 0 ? "click to show original Hebrew" : "click to show English translation"), "label mismatch");
    rows.forEach((row, other) => {
      if (other !== index) assert(!row.blocks[0].hidden && row.blocks[1].hidden, "another row changed");
    });
  }
}
fs.writeFileSync(process.argv[3], JSON.stringify({buttons: rows.length, clicks, both_states_and_row_isolation: true, scope: "Pure JavaScript with fake DOM contracts; no browser/layout claim"}, null, 2) + "\n");
console.log(`${rows.length} buttons, ${clicks} clicks: states, labels and isolation pass.`);
