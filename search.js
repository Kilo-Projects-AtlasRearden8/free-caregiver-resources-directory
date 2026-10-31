/* Free Caregiver Resources Directory — client-side search
 * Filters the server-rendered cards by query text.
 * No network calls, no tracking, fully local.
 */
(function () {
  "use strict";

  var searchInput = document.getElementById("search");
  var countEl = document.getElementById("count");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));

  function showAll() {
    cards.forEach(function (card) { card.classList.remove("hidden"); });
  }

  function updateCount(visible) {
    if (!countEl) return;
    var total = cards.length;
    countEl.textContent = visible === total ? "" : visible + " of " + total + " shown";
  }

  function filter(query) {
    var q = (query || "").trim().toLowerCase();
    if (!q) {
      showAll();
      updateCount(cards.length);
      return;
    }
    var visible = 0;
    cards.forEach(function (card) {
      if (card.textContent.toLowerCase().indexOf(q) !== -1) {
        card.classList.remove("hidden");
        visible += 1;
      } else {
        card.classList.add("hidden");
      }
    });
    updateCount(visible);
  }

  if (!searchInput) return;
  searchInput.addEventListener("input", function () {
    filter(searchInput.value);
  });
  updateCount(cards.length);
})();