import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .test_utils import make_user

HASHED = {
    **settings.STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}


class HashedStaticFilesTests(TestCase):
    def test_collectstatic_works_and_pages_use_hashed_names(self):
        # collectstatic fails on a CSS or JS file that points at a missing file, which would break
        # a deploy. Once it has run, pages must link to the hashed copies.
        with tempfile.TemporaryDirectory() as root, override_settings(STATIC_ROOT=root, STORAGES=HASHED):
            call_command("collectstatic", interactive=False, verbosity=0)
            page = self.client.get(reverse("login")).content.decode()
            worker = self.client.get(reverse("service_worker")).content.decode()
        self.assertRegex(page, r"/static/css/app\.[0-9a-f]{12}\.css")
        self.assertRegex(page, r"/static/js/confirm\.[0-9a-f]{12}\.js")
        # The service worker's offline copy follows the stylesheet's new name.
        self.assertRegex(worker, r"/static/css/app\.[0-9a-f]{12}\.css")


class AndroidAppDownloadTests(TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.apk = Path(folder.name) / "the-kinky-list.apk"
        override = override_settings(ANDROID_APK_FILE=self.apk)
        override.enable()
        self.addCleanup(override.disable)

    def test_hidden_until_the_apk_is_on_the_server(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Get the Android app")
        self.assertNotContains(response, "#get-app")
        self.assertEqual(self.client.get(reverse("android_apk")).status_code, 404)

    def test_top_bar_leads_to_the_card(self):
        # Signed out, the card is on the home page; signed in, on the profile page.
        self.apk.write_bytes(b"apk")
        self.assertContains(self.client.get(reverse("login")), f'href="{reverse("home")}#get-app"')
        self.client.force_login(make_user("sam"))
        self.assertContains(self.client.get(reverse("spaces:index")), f'href="{reverse("profile")}#get-app"')
        self.assertContains(self.client.get(reverse("profile")), 'id="get-app"')

    def test_landing_page_offers_the_download(self):
        self.apk.write_bytes(b"apk" * 1000)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Get the Android app")
        self.assertContains(response, f'href="{reverse("android_apk")}"')
        self.assertContains(response, "2.9\xa0KB")

    def test_profile_offers_the_download(self):
        # Signed-in people never see the landing page.
        self.apk.write_bytes(b"apk")
        self.client.force_login(make_user("sam"))
        self.assertContains(self.client.get(reverse("profile")), "Get the Android app")

    def test_download(self):
        self.apk.write_bytes(b"not really an apk")
        response = self.client.get(reverse("android_apk"))
        self.assertEqual(response["Content-Type"], "application/vnd.android.package-archive")
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="the-kinky-list.apk"')
        self.assertEqual(b"".join(response.streaming_content), b"not really an apk")
