from unittest import mock
from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from kinkylist.test_utils import make_user

from . import google
from .forms import GoogleSignupForm
from .models import profile_for

User = get_user_model()
GOOGLE_ON = override_settings(GOOGLE_CLIENT_ID="cid.apps.googleusercontent.com", GOOGLE_CLIENT_SECRET="shh")
GOOGLE_OFF = override_settings(GOOGLE_CLIENT_ID="", GOOGLE_CLIENT_SECRET="")
ALEX = google.Identity(sub="1234567890", name="Alex Example")


def link(user, sub=ALEX.sub):
    profile = profile_for(user)
    profile.google_id = sub
    profile.save()
    return user


def google_only_user(sub=ALEX.sub):
    form = GoogleSignupForm({"display_name": "Alex", "adult_confirmed": "on"})
    assert form.is_valid()
    return form.save(google_id=sub)


@GOOGLE_ON
class GoogleSignInTests(TestCase):
    def start(self, next_url=""):
        response = self.client.get(reverse("google_start"), {"next": next_url} if next_url else {})
        return parse_qs(urlparse(response["Location"]).query)

    def come_back(self, identity=ALEX, next_url="", **params):
        """Go to Google and come back with a code, as a browser would."""
        query = self.start(next_url)
        params = {"state": query["state"][0], "code": "one-time-code", **params}
        with mock.patch("accounts.google.exchange_code", return_value=identity) as exchange:
            response = self.client.get(reverse("google_callback"), params)
        return response, exchange

    def logged_in_id(self):
        return int(self.client.session.get("_auth_user_id", 0))

    def test_start_asks_google_for_a_name_but_never_an_email(self):
        query = self.start()
        self.assertEqual(query["scope"], ["openid profile"])
        self.assertEqual(query["client_id"], ["cid.apps.googleusercontent.com"])
        self.assertEqual(query["code_challenge_method"], ["S256"])
        self.assertTrue(query["redirect_uri"][0].endswith(reverse("google_callback")))

    def test_new_google_user_confirms_age_before_getting_an_account(self):
        response, exchange = self.come_back()
        self.assertRedirects(response, reverse("google_signup"), fetch_redirect_response=False)
        self.assertEqual(exchange.call_args.args[0], "one-time-code")
        self.assertContains(self.client.get(reverse("google_signup")), 'value="Alex Example"')

        self.client.post(reverse("google_signup"), {"display_name": "Alex"})
        self.assertFalse(User.objects.exists())

        response = self.client.post(reverse("google_signup"), {"display_name": "Alex", "adult_confirmed": "on"})
        self.assertRedirects(response, reverse("spaces:index"), fetch_redirect_response=False)
        user = User.objects.get()
        self.assertEqual((user.profile.google_id, user.profile.display_name), (ALEX.sub, "Alex"))
        self.assertTrue(user.profile.adult_confirmed)
        self.assertFalse(user.has_usable_password())
        self.assertEqual(self.logged_in_id(), user.pk)

    def test_returning_google_user_is_logged_in_and_sent_on(self):
        user = link(make_user("a"))
        response, _ = self.come_back(next_url="/privacy/")
        self.assertRedirects(response, "/privacy/", fetch_redirect_response=False)
        self.assertEqual(self.logged_in_id(), user.pk)

    def test_next_must_stay_on_this_site(self):
        link(make_user("a"))
        response, _ = self.come_back(next_url="https://evil.example/")
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)

    def test_forged_state_is_refused(self):
        link(make_user("a"))
        self.start()
        with mock.patch("accounts.google.exchange_code") as exchange:
            response = self.client.get(reverse("google_callback"), {"state": "forged", "code": "c"})
        exchange.assert_not_called()
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)
        self.assertEqual(self.logged_in_id(), 0)

    def test_cancelling_on_google_changes_nothing(self):
        response, exchange = self.come_back(code="", error="access_denied")
        exchange.assert_not_called()
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_failed_sign_in_shows_an_error(self):
        query = self.start()
        with mock.patch("accounts.google.exchange_code", side_effect=google.InvalidCredential("nope")):
            with self.assertLogs("accounts.views", "WARNING"):
                response = self.client.get(reverse("google_callback"), {"state": query["state"][0], "code": "c"}, follow=True)
        self.assertContains(response, "Google sign-in didn't work")
        self.assertEqual(self.logged_in_id(), 0)

    def test_android_app_posts_the_id_token(self):
        user = link(make_user("a"))
        with mock.patch("accounts.google.verify", return_value=ALEX) as verify:
            response = self.client.post(reverse("google_token"), {"credential": "id-token", "next": "/privacy/"})
        verify.assert_called_once_with("id-token")
        self.assertRedirects(response, "/privacy/", fetch_redirect_response=False)
        self.assertEqual(self.logged_in_id(), user.pk)

    def test_connect_google_from_the_profile(self):
        user = make_user("a")
        self.client.force_login(user)
        self.assertContains(self.client.get(reverse("profile")), "Connect Google")
        response, _ = self.come_back()
        self.assertRedirects(response, reverse("profile"), fetch_redirect_response=False)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.google_id, ALEX.sub)
        self.assertContains(self.client.get(reverse("profile")), "Google is connected")

    def test_cant_connect_a_google_account_someone_else_uses(self):
        link(make_user("b"))
        user = make_user("a")
        self.client.force_login(user)
        response, _ = self.come_back()
        user.profile.refresh_from_db()
        self.assertIsNone(user.profile.google_id)
        self.assertContains(self.client.get(response["Location"]), "already used by another")

    def test_disconnect_needs_a_password_to_fall_back_on(self):
        user = link(make_user("a"))
        self.client.force_login(user)
        self.client.post(reverse("google_disconnect"))
        user.profile.refresh_from_db()
        self.assertIsNone(user.profile.google_id)

        google_user = google_only_user(sub="999")
        self.client.force_login(google_user)
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "You log in with Google")
        self.assertContains(response, f'<strong class="select-all">{google_user.username}</strong>')
        self.assertContains(response, "made up for you, since you log in with Google")
        self.assertTrue(google_user.username.startswith("google-"))
        self.client.post(reverse("google_disconnect"))
        google_user.profile.refresh_from_db()
        self.assertEqual(google_user.profile.google_id, "999")

    def test_google_only_account_is_deleted_by_typing_delete(self):
        user = google_only_user()
        self.client.force_login(user)
        self.assertContains(self.client.get(reverse("delete_account")), "Type DELETE to confirm")
        self.client.post(reverse("delete_account"), {"confirm": "nope"})
        self.assertTrue(User.objects.filter(pk=user.pk).exists())
        self.client.post(reverse("delete_account"), {"confirm": "delete"})
        self.assertFalse(User.objects.filter(pk=user.pk).exists())

    def test_buttons_show_only_when_google_is_set_up(self):
        for name in ["login", "signup"]:
            self.assertContains(self.client.get(reverse(name)), reverse("google_start"))
        with GOOGLE_OFF:
            for name in ["login", "signup"]:
                self.assertNotContains(self.client.get(reverse(name)), "Continue with Google")
            self.assertEqual(self.client.get(reverse("google_start")).status_code, 404)
            self.assertEqual(self.client.post(reverse("google_token"), {"credential": "t"}).status_code, 404)


@GOOGLE_ON
class GoogleModuleTests(TestCase):
    def test_verify_checks_the_token_was_made_for_this_site(self):
        with mock.patch("google.oauth2.id_token.verify_oauth2_token", return_value={"sub": "42", "name": "Sam"}) as check:
            self.assertEqual(google.verify("tok"), google.Identity(sub="42", name="Sam"))
        self.assertEqual(check.call_args.kwargs["audience"], "cid.apps.googleusercontent.com")
        with mock.patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Token expired")):
            with self.assertRaises(google.InvalidCredential):
                google.verify("tok")
        with self.assertRaises(google.InvalidCredential):
            google.verify("")

    def test_exchange_code_proves_it_started_the_sign_in(self):
        ok = mock.Mock(ok=True, status_code=200)
        ok.json.return_value = {"id_token": "id-token"}
        with mock.patch("requests.post", return_value=ok) as post, mock.patch("accounts.google.verify") as verify:
            google.exchange_code("code", "https://site/google/callback/", "verifier")
        sent = post.call_args.kwargs["data"]
        self.assertEqual((sent["code_verifier"], sent["client_secret"]), ("verifier", "shh"))
        verify.assert_called_once_with("id-token")

        refused = mock.Mock(ok=False, status_code=400, text="invalid_grant")
        with mock.patch("requests.post", return_value=refused), self.assertLogs("accounts.google", "WARNING"):
            with self.assertRaises(google.InvalidCredential):
                google.exchange_code("code", "https://site/google/callback/", "verifier")
