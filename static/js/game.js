/* Alpine components for the games, the assign step and check-offs. */
(function () {
  "use strict";

  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  const COLORS = ["#e11d48", "#fb7185", "#fbcfe8", "#fdba8c", "#f5d7a1", "#c084fc"];

  window.celebrate = function () {
    if (!window.confetti || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const heart = confetti.shapeFromPath
      ? confetti.shapeFromPath({ path: "M14 22C8 17 0 12 4 5C7 0 13 2 14 7C15 2 21 0 24 5C28 12 20 17 14 22Z" })
      : "circle";
    const burst = (x) =>
      confetti({ particleCount: 60, spread: 70, startVelocity: 38, origin: { x, y: 0.75 }, colors: COLORS, shapes: [heart, "circle"], scalar: 1.2 });
    burst(0.3);
    setTimeout(() => burst(0.7), 180);
  };

  document.addEventListener("celebrate", window.celebrate);

  document.addEventListener("alpine:init", () => {
    // Shared by all four games: tracks picks and fetches more cards from the feed endpoint.
    Alpine.data("picker", (cfg) => ({
      max: cfg.max,
      feedUrl: cfg.feedUrl,
      completed: cfg.completed ? "1" : "",
      selected: [],
      seen: [],
      skipsLeft: cfg.skips || 0,
      exhausted: false,
      current: null,
      loading: false,
      spice: [],
      categories: [],

      get full() {
        return this.selected.length >= this.max;
      },
      has(id) {
        return this.selected.some((s) => s.id === Number(id));
      },
      entry(el) {
        const card = el.closest("[data-id]");
        return { id: Number(card.dataset.id), title: card.dataset.title };
      },
      ids(list) {
        return list.map((s) => (typeof s === "object" ? s.id : s)).join(",");
      },
      add(el) {
        const entry = this.entry(el);
        if (!this.has(entry.id) && !this.full) this.selected.push(entry);
      },
      toggle(el) {
        const entry = this.entry(el);
        if (this.has(entry.id)) {
          this.selected = this.selected.filter((s) => s.id !== entry.id);
        } else if (!this.full) {
          this.selected.push(entry);
        }
      },
      load(target, swap, extra) {
        this.loading = true;
        return htmx
          .ajax("GET", this.feedUrl, { target, swap, values: { completed: this.completed, ...extra } })
          .finally(() => {
            this.loading = false;
          });
      },

      // Game 1: Randomize, drawing only from the chosen intensities and categories
      get filtered() {
        return this.spice.length > 0 || this.categories.length > 0;
      },
      randomize() {
        if (this.full || this.exhausted || this.loading) return;
        this.load("#cards", "beforeend", {
          exclude: this.ids(this.selected),
          spice: this.spice.join(","),
          category: this.categories.join(","),
        });
      },
      discard(el) {
        const card = el.closest("[data-id]");
        this.selected = this.selected.filter((s) => s.id !== Number(card.dataset.id));
        card.remove();
        this.exhausted = false;
      },

      // Game 2: Pick your favorite (keeps current picks, refreshes the rest)
      reshuffle() {
        if (this.loading) return;
        this.load("#grid", "innerHTML", { exclude: this.ids(this.selected) });
      },

      // Game 4: Try new things!
      show(el) {
        this.current = this.entry(el);
        this.seen.push(this.current.id);
      },
      accept() {
        if (!this.current || this.full) return;
        this.selected.push(this.current);
        this.next();
      },
      skip() {
        if (!this.current || this.skipsLeft <= 0) return;
        this.skipsLeft--;
        this.next();
      },
      next() {
        this.current = null;
        if (this.full) return;
        this.load("#stage", "innerHTML", { exclude: this.seen.join(",") });
      },
    }));

    // Assign step shortcuts: tick one member (or everyone) on every item.
    Alpine.data("assigner", () => ({
      assignAll(memberId) {
        this.$root.querySelectorAll("input[data-member]").forEach((box) => {
          box.checked = memberId === "all" || box.dataset.member === String(memberId);
        });
      },
    }));

    // Check-off dialog on the assignments page.
    Alpine.data("checkoff", (cfg) => ({
      url: "",
      title: "",
      note: "",
      start(el) {
        this.url = el.dataset.url;
        this.title = el.dataset.title;
        this.note = "";
        this.$refs.dialog.showModal();
      },
      submit() {
        htmx.ajax("POST", this.url, {
          target: "#assignment-list",
          swap: "outerHTML",
          values: { note: this.note, tab: cfg.tab, who: cfg.who },
          headers: { "X-CSRFToken": csrfToken() },
        });
        this.$refs.dialog.close();
      },
    }));
  });
})();
