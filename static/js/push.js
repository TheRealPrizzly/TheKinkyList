// Push notifications inside the iPhone and Android apps (Capacitor + Firebase Cloud Messaging).
// The apps load this site, and Capacitor gives its pages a bridge to the native plugins.
// In an ordinary browser there is no bridge, so this file does nothing.
(function () {
  const script = document.currentScript;
  const cap = window.Capacitor;
  if (!script || !cap || typeof cap.isNativePlatform !== "function" || !cap.isNativePlatform()) return;

  const Messaging = (cap.Plugins && cap.Plugins.FirebaseMessaging) || cap.registerPlugin("FirebaseMessaging");
  const registerUrl = script.dataset.registerUrl;
  const knownToken = script.dataset.knownToken || "";
  const DISMISSED = "kl-push-prompt-dismissed";

  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  // The server remembers which token this login session registered, so only send a new one.
  function sendToken(token) {
    if (!token || token === knownToken) return;
    fetch(registerUrl, {
      method: "POST",
      body: new URLSearchParams({ token: token, platform: cap.getPlatform() }),
      headers: { "X-CSRFToken": csrfToken() },
      credentials: "same-origin",
    }).catch(() => {});
  }

  async function register() {
    try {
      const result = await Messaging.getToken();
      sendToken(result.token);
    } catch (error) {
      console.warn("Push registration failed", error);
    }
  }

  function wasDismissed() {
    try {
      return localStorage.getItem(DISMISSED) === "1";
    } catch (error) {
      return false;
    }
  }

  // Ask only when someone taps "Turn on notifications", never on first launch.
  function showPrompts() {
    if (wasDismissed()) return;
    document.querySelectorAll("[data-push-prompt]").forEach((prompt) => {
      prompt.hidden = false;
      const enable = prompt.querySelector("[data-push-enable]");
      const dismiss = prompt.querySelector("[data-push-dismiss]");
      if (enable) {
        enable.addEventListener("click", async () => {
          prompt.hidden = true;
          const result = await Messaging.requestPermissions();
          if (result.receive === "granted") register();
        });
      }
      if (dismiss) {
        dismiss.addEventListener("click", () => {
          prompt.hidden = true;
          try {
            localStorage.setItem(DISMISSED, "1");
          } catch (error) {
            // Private mode or blocked storage: the prompt simply shows again next time.
          }
        });
      }
    });
  }

  // Tapping a notification opens the page it's about (only paths on this site).
  Messaging.addListener("notificationActionPerformed", (event) => {
    const data = event && event.notification && event.notification.data;
    const url = data && data.url;
    if (typeof url === "string" && url.startsWith("/") && !url.startsWith("//")) {
      window.location.href = url;
    }
  });
  Messaging.addListener("tokenReceived", (event) => sendToken(event.token));

  Messaging.checkPermissions()
    .then((result) => {
      if (result.receive === "granted") register();
      else if (result.receive === "prompt" || result.receive === "prompt-with-rationale") showPrompts();
    })
    .catch(() => {});
})();
