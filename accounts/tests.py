from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from assignments.models import Assignment
from kinkylist.test_utils import make_items, make_space, make_user
from spaces.models import Membership, Space

PASSWORD = "pw-for-tests-123"  # what make_user sets


class DeleteAccountTests(TestCase):
    def setUp(self):
        self.a = make_user("a")
        self.client.force_login(self.a)

    def test_profile_links_to_delete_and_privacy(self):
        response = self.client.get(reverse("profile"))
        self.assertContains(response, reverse("delete_account"))
        self.assertContains(response, reverse("privacy"))

    def test_profile_shows_the_username(self):
        response = self.client.get(reverse("profile"))
        self.assertContains(response, '<strong class="select-all">a</strong>')
        self.assertContains(response, "you log in with it")

    def test_page_lists_spaces_that_will_be_deleted(self):
        make_space(self.a, name="Just me")
        make_space(self.a, make_user("b"), name="Shared")
        response = self.client.get(reverse("delete_account"))
        self.assertContains(response, "Just me")
        self.assertNotContains(response, "Shared")

    def test_wrong_password_keeps_account(self):
        response = self.client.post(reverse("delete_account"), {"password": "nope"})
        self.assertContains(response, "That password isn")
        self.assertTrue(get_user_model().objects.filter(pk=self.a.pk).exists())

    def test_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse("delete_account"), {"password": PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(pk=self.a.pk).exists())

    def test_delete_removes_user_and_solo_spaces_and_keeps_shared_ones(self):
        b = make_user("b")
        solo = make_space(self.a, name="Just me")
        shared = make_space(self.a, b, name="Shared")
        item = make_items(shared, "Candlelit bath")[0]
        item.created_by = self.a
        item.save()
        assignment = Assignment.objects.create(space=shared, item=item, assigned_by=self.a)
        assignment.assignees.set([self.a, b])

        response = self.client.post(reverse("delete_account"), {"password": PASSWORD})

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(get_user_model().objects.filter(username="a").exists())
        self.assertFalse(Space.objects.filter(pk=solo.pk).exists())
        # The partner keeps the shared space, now as its owner, with the wish but without a's name.
        membership = Membership.objects.get(space=shared)
        self.assertEqual((membership.user, membership.role), (b, Membership.OWNER))
        item.refresh_from_db()
        self.assertIsNone(item.created_by)
        self.assertEqual(list(assignment.assignees.all()), [b])
        # And the deleted user is logged out.
        self.assertEqual(self.client.get(reverse("profile")).status_code, 302)


class PrivacyTests(TestCase):
    def test_privacy_is_public(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "Privacy policy")

    @override_settings(CONTACT_EMAIL="hello@example.com")
    def test_contact_email_shown_when_set(self):
        self.assertContains(self.client.get(reverse("privacy")), "mailto:hello@example.com")

    @override_settings(CONTACT_EMAIL="")
    def test_contact_section_hidden_when_unset(self):
        self.assertNotContains(self.client.get(reverse("privacy")), "mailto:")


class InstallableAppTests(TestCase):
    def test_manifest(self):
        response = self.client.get(reverse("manifest"))
        self.assertEqual(response["Content-Type"], "application/manifest+json")
        data = response.json()
        self.assertEqual(data["display"], "standalone")
        self.assertEqual({icon["purpose"] for icon in data["icons"]}, {"any", "maskable"})

    def test_service_worker_served_from_root(self):
        response = self.client.get("/sw.js")
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertContains(response, '"/offline/"')

    def test_offline_page(self):
        self.assertContains(self.client.get(reverse("offline")), "You're offline")

    def test_pages_link_manifest(self):
        self.assertContains(self.client.get(reverse("home")), 'rel="manifest"')
