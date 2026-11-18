// "Continue with Google" inside the Android app (see templates/partials/google_button.html).
// Google blocks its sign-in page inside apps, so the app signs in with Android's own account
// picker and posts Google's ID token to the server, which checks it. In browsers the button is a
// plain link to Google's sign-in page and this file does nothing. The button stays hidden in the
// iPhone app (Apple would then require Sign in with Apple too) and in Android builds from before
// the sign-in plugin was added.
(function () {
  const cap = window.Capacitor;
  if (!cap || typeof cap.isNativePlatform !== "function" || !cap.isNativePlatform()) return;
  if (cap.getPlatform() !== "android" || !cap.isPluginAvailable("FirebaseAuthentication")) return;
  const Auth = (cap.Plugins && cap.Plugins.FirebaseAuthentication) || cap.registerPlugin("FirebaseAuthentication");

  document.querySelectorAll("[data-google-signin]").forEach((box) => {
    const button = box.querySelector("[data-google-start]");
    const form = box.querySelector("[data-google-token-form]");
    const failed = box.querySelector("[data-google-error]");
    if (!button || !form) return;
    box.classList.add("is-native");
    button.addEventListener("click", async (event) => {
      event.preventDefault();
      if (failed) failed.hidden = true;
      try {
        const result = await Auth.signInWithGoogle();
        const token = result && result.credential && result.credential.idToken;
        if (!token) throw new Error("No ID token");
        form.elements.credential.value = token;
        form.submit();
      } catch (error) {
        // Closing the account picker is not a failure.
        if (/cancel/i.test(String((error && error.message) || error))) return;
        console.warn("Google sign-in failed", error);
        if (failed) failed.hidden = false;
      }
    });
  });
})();
