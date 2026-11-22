/* Alpine components for the games, the assign step and check-offs. */
(function () {
  "use strict";

  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  // With a mouse, a wish's details show on hover; on a touch screen, on tap.
  const HOVER = window.matchMedia("(hover: hover) and (pointer: fine)");
  const canHover = () => HOVER.matches;

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
      // A click on a pick card. With a mouse it chooses the card. On a touch screen only its circle does,
      // and tapping anywhere else shows the details (see "A wish's details" below).
      tap(el, event) {
        if (canHover() || event.target.closest("[data-pick]")) this.toggle(el);
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
      filters() {
        return { spice: this.spice.join(","), category: this.categories.join(",") };
      },
      // Start over with a single fresh draw, avoiding what's on screen when possible.
      randomize() {
        if (this.loading) return;
        const shown = this.ids(this.selected);
        this.selected = [];
        this.exhausted = false;
        this.load("#cards", "innerHTML", { avoid: shown, ...this.filters() });
      },
      addOne() {
        if (this.full || this.exhausted || this.loading) return;
        this.load("#cards", "beforeend", { exclude: this.ids(this.selected), ...this.filters() });
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

    // Truth or Dare: played live on one screen, taking turns.
    Alpine.data("truthOrDare", (configId) => {
      const cfg = JSON.parse(document.getElementById(configId).textContent);
      const nobody = { id: "", name: "", color: "", initial: "" };
      return {
        feedUrl: cfg.feedUrl,
        dareUrl: cfg.dareUrl,
        players: cfg.players,
        listDares: cfg.dareCount,
        wishes: cfg.wishCount,
        wishesWithDone: cfg.wishCountWithDone,
        // Whether wishes from The Kinky List join the dares, and whether ones already lived count.
        mix: false,
        withDone: false,
        chosen: cfg.players.map((p) => String(p.id)),
        spice: [],
        started: false,
        order: [],
        turn: 0,
        card: null,
        seen: { truth: [], dare: [] },
        session: "",
        status: "",
        loading: false,
        exhausted: false,

        get wishCount() {
          return this.withDone ? this.wishesWithDone : this.wishes;
        },
        get dareCount() {
          return this.listDares + (this.mix ? this.wishCount : 0);
        },
        get completed() {
          return this.mix && this.withDone ? "1" : "";
        },
        get player() {
          return this.order.length ? this.order[this.turn % this.order.length] : nobody;
        },
        start() {
          this.order = this.players.filter((p) => this.chosen.includes(String(p.id)));
          if (!this.order.length) return;
          // Whoever goes first is up to fate.
          this.turn = Math.floor(Math.random() * this.order.length);
          this.clear();
          this.started = true;
        },
        stop() {
          this.clear();
          this.started = false;
        },
        clear() {
          this.card = null;
          this.exhausted = false;
          this.status = "";
          document.getElementById("tod-stage").innerHTML = "";
        },
        nextTurn() {
          this.clear();
          this.turn++;
        },
        choose(kind) {
          if (this.loading) return;
          const current = this.card && this.card.kind === kind ? this.card.key : "";
          this.card = null;
          this.exhausted = false;
          this.status = "";
          this.loading = true;
          htmx
            .ajax("GET", this.feedUrl, {
              target: "#tod-stage",
              swap: "innerHTML",
              values: {
                kind,
                current,
                player: this.player.id,
                spice: this.spice.join(","),
                exclude: this.seen[kind].join(","),
                mix: this.mix ? "1" : "",
                completed: this.completed,
              },
            })
            .finally(() => {
              this.loading = false;
            });
        },
        // Called by each card as it lands on the stage.
        show(el) {
          const { kind, key, recycled } = el.dataset;
          // Everything has been seen once, so the server started over.
          if (recycled) this.seen[kind] = [];
          this.seen[kind].push(key);
          this.card = { kind, key };
        },
        async record(outcome) {
          if (!this.card || this.card.kind !== "dare" || this.loading) return;
          this.loading = true;
          const body = new URLSearchParams({
            item: this.card.key,
            player: this.player.id,
            outcome,
            session: this.session,
            completed: this.completed,
          });
          try {
            const response = await fetch(this.dareUrl, {
              method: "POST",
              body,
              headers: { "X-CSRFToken": csrfToken() },
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
              this.status = data.error || "Couldn't save that. Try again.";
              return;
            }
            this.session = data.session;
            if (outcome === "done") window.celebrate();
            this.nextTurn();
            this.status = data.message;
          } catch (error) {
            this.status = "Couldn't reach the site. Check your connection and try again.";
          } finally {
            this.loading = false;
          }
        },
      };
    });

    // Would you rather: one question at a time, answered out loud.
    Alpine.data("wouldYouRather", (configId) => {
      const cfg = JSON.parse(document.getElementById(configId).textContent);
      return {
        feedUrl: cfg.feedUrl,
        spice: [],
        seen: [],
        started: false,
        card: null,
        picked: 0,
        loading: false,
        exhausted: false,

        start() {
          this.started = true;
          this.next();
        },
        stop() {
          this.started = false;
          this.card = null;
          this.exhausted = false;
          document.getElementById("wyr-stage").innerHTML = "";
        },
        next() {
          if (this.loading) return;
          const current = this.card ? this.card.key : "";
          this.card = null;
          this.picked = 0;
          this.exhausted = false;
          this.loading = true;
          htmx
            .ajax("GET", this.feedUrl, {
              target: "#wyr-stage",
              swap: "innerHTML",
              values: { current, spice: this.spice.join(","), exclude: this.seen.join(",") },
            })
            .finally(() => {
              this.loading = false;
            });
        },
        // Called by each question card as it lands on the stage.
        show(el) {
          const { key, recycled } = el.dataset;
          // Every question has been asked once, so the server started over.
          if (recycled) this.seen = [];
          this.seen.push(key);
          this.card = { key };
        },
        pick(choice) {
          this.picked = this.picked === choice ? 0 : choice;
        },
      };
    });

    // Assign step shortcuts: tick one member (or everyone) on every item.
    Alpine.data("assigner", () => ({
      assignAll(memberId) {
        this.$root.querySelectorAll("input[data-member]").forEach((box) => {
          box.checked = !box.disabled && (memberId === "all" || box.dataset.member === String(memberId));
        });
      },
    }));

    // Check-off dialog on the assignments page.
    Alpine.data("checkoff", (cfg) => ({
      url: "",
      title: "",
      note: "",
      // The wish's levels, and the ids (as strings) of those ticked as reached this time.
      levels: [],
      reached: [],
      start(el) {
        this.url = el.dataset.url;
        this.title = el.dataset.title;
        this.note = "";
        try {
          this.levels = JSON.parse(el.dataset.levels || "[]");
        } catch (e) {
          this.levels = [];
        }
        // The next level is the one you most likely just reached.
        const next = this.levels.find((level) => !level.done);
        this.reached = next ? [String(next.id)] : [];
        this.$refs.dialog.showModal();
      },
      submit() {
        htmx.ajax("POST", this.url, {
          target: "#assignment-list",
          swap: "outerHTML",
          values: { note: this.note, levels: this.reached.join(","), tab: cfg.tab, who: cfg.who },
          headers: { "X-CSRFToken": csrfToken() },
        });
        this.$refs.dialog.close();
      },
    }));
  });

  // ---------- A wish's details ----------
  // Each game card for a wish carries them in a <template class="details-template">. With a mouse they
  // show in a panel beside the card on hover (or on keyboard focus); on a touch screen, tapping the card
  // opens them in a sheet. Both live in templates/games/_details_layer.html.

  function detailsOf(card) {
    const template = card.querySelector("template.details-template");
    return template ? template.content.cloneNode(true) : null;
  }

  let hoverCard = null;
  let pendingCard = null;
  let showTimer = 0;
  let hideTimer = 0;

  function placePop(pop, card) {
    const gap = 12;
    const margin = 16;
    const rect = card.getBoundingClientRect();
    const width = pop.offsetWidth;
    const height = pop.offsetHeight;
    const viewWidth = document.documentElement.clientWidth;
    const viewHeight = window.innerHeight;
    let left = null;
    let top;
    if (rect.right + gap + width <= viewWidth - margin) left = rect.right + gap;
    else if (rect.left - gap - width >= margin) left = rect.left - gap - width;
    if (left !== null) {
      // Beside the card, level with its top.
      top = Math.min(rect.top, viewHeight - height - margin);
    } else {
      // No room beside it: below the card, or above when it doesn't fit below.
      left = Math.min(Math.max(rect.left + (rect.width - width) / 2, margin), viewWidth - width - margin);
      top = rect.bottom + gap + height <= viewHeight - margin ? rect.bottom + gap : rect.top - gap - height;
    }
    pop.style.left = `${Math.round(left)}px`;
    pop.style.top = `${Math.round(Math.max(margin, top))}px`;
  }

  function showPop(card) {
    const pop = document.getElementById("details-pop");
    const content = pop && card.isConnected ? detailsOf(card) : null;
    pendingCard = null;
    if (!content) return;
    pop.replaceChildren(content);
    pop.style.visibility = "hidden";
    pop.hidden = false;
    placePop(pop, card);
    pop.style.visibility = "";
    hoverCard = card;
  }

  function hidePop() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    pendingCard = null;
    hoverCard = null;
    const pop = document.getElementById("details-pop");
    if (pop && !pop.hidden) {
      pop.hidden = true;
      pop.replaceChildren();
    }
  }

  document.addEventListener("mouseover", (event) => {
    if (!canHover()) return;
    const card = event.target.closest("[data-details]");
    if (card) {
      clearTimeout(hideTimer);
      if (card === hoverCard || card === pendingCard) return;
      clearTimeout(showTimer);
      pendingCard = card;
      // Moving from one card to the next swaps the panel almost at once.
      showTimer = setTimeout(() => showPop(card), hoverCard ? 80 : 350);
    } else if (event.target.closest("#details-pop")) {
      clearTimeout(hideTimer);
    } else {
      clearTimeout(showTimer);
      pendingCard = null;
      if (hoverCard) {
        clearTimeout(hideTimer);
        hideTimer = setTimeout(hidePop, 200);
      }
    }
  });

  document.documentElement.addEventListener("mouseleave", () => {
    if (hoverCard || pendingCard) hidePop();
  });

  // Keyboard: focusing a card shows its details too.
  document.addEventListener("focusin", (event) => {
    if (!canHover()) return;
    const card = event.target.closest && event.target.closest("[data-details]");
    if (card && event.target === card) {
      clearTimeout(showTimer);
      clearTimeout(hideTimer);
      showPop(card);
    } else if (hoverCard && card !== hoverCard) {
      hidePop();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && hoverCard) hidePop();
  });
  window.addEventListener("scroll", () => hoverCard && hidePop(), { passive: true });
  // Cards come and go (Randomize, Reshuffle, Skip): never leave a panel up for one that's gone.
  document.addEventListener("htmx:beforeSwap", hidePop);

  let sheetCard = null;

  function openSheet(card) {
    const sheet = document.getElementById("details-sheet");
    const content = sheet ? detailsOf(card) : null;
    if (!content) return;
    hidePop();
    const body = sheet.querySelector("[data-details-body]");
    body.replaceChildren(content);
    const title = body.querySelector(".details-title");
    if (title) title.id = "details-sheet-title";

    // Pick your favorite and Just ask! can choose the wish from here.
    const pick = sheet.querySelector("[data-details-pick]");
    const pickable = card.matches(".pickable");
    pick.hidden = !pickable;
    if (pickable) {
      const chosen = card.getAttribute("aria-pressed") === "true";
      const full = !chosen && card.classList.contains("is-dim");
      pick.disabled = full;
      pick.textContent = chosen ? "Remove from my picks" : full ? "You've chosen the most you can" : "Choose this one ♥";
    }
    sheetCard = card;
    sheet.showModal();
    body.scrollTop = 0;
  }

  document.addEventListener("click", (event) => {
    const sheet = event.target.closest("#details-sheet");
    if (sheet) {
      // The backdrop counts as the dialog itself.
      if (event.target === sheet || event.target.closest("[data-details-close]")) {
        sheet.close();
      } else if (event.target.closest("[data-details-pick]") && sheetCard) {
        sheetCard.dispatchEvent(new CustomEvent("details-pick"));
        sheet.close();
      }
      return;
    }
    setTimeout(() => {
      if (hoverCard && !hoverCard.isConnected) hidePop();
    });
    if (canHover()) return;
    const card = event.target.closest("[data-details]");
    // The card's own controls (Put back, the pick circle) do their own thing.
    if (!card || event.target.closest("button, a, input, label, [data-pick]")) return;
    openSheet(card);
  });

  document.addEventListener(
    "close",
    (event) => {
      if (event.target.id !== "details-sheet") return;
      sheetCard = null;
      event.target.querySelector("[data-details-body]").replaceChildren();
    },
    true
  );
})();
