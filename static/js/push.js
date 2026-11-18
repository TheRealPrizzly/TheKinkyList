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

  // Android files notifications by channel. This one pops up with sound; "private" lets the phone's
  // lock screen settings hide the text. Must match ANDROID_CHANNEL in push/fcm.py. Creating it
  // again on later visits is harmless.
  async function createChannel() {
    if (cap.getPlatform() !== "android") return;
    try {
      await Messaging.createChannel({
        id: "wishes",
        name: "Wishes and answers",
        description: "When someone requests something from you, answers your request, or checks one off",
        importance: 4,
        visibility: 0,
        vibration: true,
        lights: true,
        lightColor: "#E11D48",
      });
    } catch (error) {
      console.warn("Couldn't create the notification channel", error);
    }
  }

  async function register() {
    await createChannel();
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

  // Notifications only ever open pages on this site.
  function sitePath(notification) {
    const url = notification && notification.data && notification.data.url;
    return typeof url === "string" && url.startsWith("/") && !url.startsWith("//") ? url : "";
  }

  // While the app is open, Android hands the notification to the page instead of showing it,
  // so show it here as a banner. (iPhones show their own banner, see presentationOptions in
  // mobile/capacitor.config.ts.)
  let toastTimer;
  function showToast(notification) {
    if (cap.getPlatform() !== "android" || !notification || !(notification.title || notification.body)) return;
    document.querySelectorAll(".push-toast").forEach((old) => old.remove());
    const url = sitePath(notification);
    const toast = document.createElement("div");
    toast.className = "push-toast";
    toast.setAttribute("role", "status");
    const text = document.createElement(url ? "a" : "div");
    text.className = "push-toast-text";
    if (url) text.href = url;
    const title = document.createElement("strong");
    title.textContent = notification.title || "";
    const body = document.createElement("span");
    body.textContent = notification.body || "";
    text.append(title, body);
    const close = document.createElement("button");
    close.type = "button";
    close.className = "push-toast-close";
    close.setAttribute("aria-label", "Dismiss");
    close.textContent = "×";
    close.addEventListener("click", () => toast.remove());
    toast.append(text, close);
    document.body.append(toast);
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.remove(), 8000);
  }

  Messaging.addListener("notificationReceived", (event) => showToast(event && event.notification));
  // Tapping a notification opens the page it's about.
  Messaging.addListener("notificationActionPerformed", (event) => {
    const url = sitePath(event && event.notification);
    if (url) window.location.href = url;
  });
  Messaging.addListener("tokenReceived", (event) => sendToken(event.token));

  Messaging.checkPermissions()
    .then((result) => {
      if (result.receive === "granted") register();
      else if (result.receive === "prompt" || result.receive === "prompt-with-rationale") showPrompts();
    })
    .catch(() => {});
})();
