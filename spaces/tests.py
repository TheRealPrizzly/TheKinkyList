from django.test import TestCase
from django.urls import reverse

from kinkylist.test_utils import make_space, make_user

from .models import CODE_ALPHABET, Membership, Space


class SpaceTests(TestCase):
    def setUp(self):
        self.a = make_user("a")
        self.client.force_login(self.a)

    def test_create_space_makes_owner_and_code(self):
        response = self.client.post(reverse("spaces:create"), {"name": "Us"})
        space = Space.objects.get()
        self.assertRedirects(response, reverse("spaces:dashboard", args=[space.id]))
        self.assertEqual(space.memberships.get().role, Membership.OWNER)
        self.assertEqual(len(space.invite_code), 6)
        self.assertTrue(set(space.invite_code) <= set(CODE_ALPHABET))

    def test_join_with_code_is_case_and_space_insensitive(self):
        space = make_space(make_user("b"))
        self.client.post(reverse("spaces:join"), {"code": " " + space.invite_code.lower()[:3] + " " + space.invite_code.lower()[3:]})
        self.assertTrue(space.has_member(self.a))

    def test_join_with_bad_code(self):
        response = self.client.post(reverse("spaces:join"), {"code": "ZZZZZZ"}, follow=True)
        self.assertContains(response, "couldn&#x27;t find a space")

    def test_non_member_cannot_see_space(self):
        space = make_space(make_user("b"))
        for name in ["spaces:dashboard", "spaces:dashboard_live", "spaces:settings", "items:list", "games:index", "assignments:list"]:
            self.assertEqual(self.client.get(reverse(name, args=[space.id])).status_code, 404, name)

    def test_dashboard_renders_for_member(self):
        space = make_space(self.a, make_user("b"))
        response = self.client.get(reverse("spaces:dashboard", args=[space.id]))
        self.assertContains(response, "Our bucket list")
        self.assertRedirects(self.client.get(reverse("home")), reverse("spaces:dashboard", args=[space.id]))

    def test_owner_leaving_hands_over_ownership(self):
        b = make_user("b")
        space = make_space(self.a, b)
        self.client.post(reverse("spaces:leave", args=[space.id]))
        self.assertEqual(space.memberships.get().user, b)
        self.assertEqual(space.memberships.get().role, Membership.OWNER)

    def test_last_member_leaving_deletes_space(self):
        space = make_space(self.a)
        self.client.post(reverse("spaces:leave", args=[space.id]))
        self.assertFalse(Space.objects.exists())


class SignupTests(TestCase):
    def test_signup_requires_adult_confirmation(self):
        data = {"username": "new", "display_name": "Jo", "password1": "a-long-pass-phrase", "password2": "a-long-pass-phrase"}
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("signup"), {**data, "adult_confirmed": "on"})
        self.assertRedirects(response, reverse("spaces:index"))
        self.assertTrue(response.wsgi_request.user.profile.adult_confirmed)
