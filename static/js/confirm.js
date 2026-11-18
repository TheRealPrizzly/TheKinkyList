// "Are you sure?" questions, asked in the app's own dialog (#confirm-dialog in base.html) instead of
// the browser's confirm box, which looks like a system message and, in the iPhone and Android apps,
// shows the server's address.
//   htmx buttons:    hx-confirm="Put this back on the list?"
//   ordinary forms:  data-confirm="Leave this space?"
// The confirm button is labelled with the text of the button that was pressed.
(function () {
  function ask(question, label) {
    const dialog = document.getElementById("confirm-dialog");
    if (!dialog || typeof dialog.showModal !== "function") return Promise.resolve(window.confirm(question));
    dialog.querySelector("[data-confirm-text]").textContent = question;
    dialog.querySelector("[data-confirm-ok]").textContent = label || "OK";
    dialog.returnValue = "";
    dialog.showModal();
    return new Promise((resolve) => {
      dialog.addEventListener("close", () => resolve(dialog.returnValue === "ok"), { once: true });
    });
  }

  function buttonText(element) {
    return element && element.matches("button") ? element.textContent.trim() : "";
  }

  document.addEventListener("htmx:confirm", (event) => {
    const question = event.detail.question;
    if (!question) return;
    event.preventDefault();
    ask(question, buttonText(event.detail.elt)).then((ok) => {
      if (ok) event.detail.issueRequest(true);
    });
  });

  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!form.dataset.confirm) return;
    if (form.dataset.confirmed) {
      delete form.dataset.confirmed;
      return;
    }
    event.preventDefault();
    const submitter = event.submitter;
    ask(form.dataset.confirm, buttonText(submitter)).then((ok) => {
      if (!ok) return;
      form.dataset.confirmed = "1";
      form.requestSubmit(submitter);
    });
  });
})();
