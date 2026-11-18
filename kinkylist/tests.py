import tempfile

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

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
