from django.test import TestCase
from django.urls import reverse

from kinkylist.test_utils import make_items, make_space, make_user

from .models import Assignment


class CheckOffTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Julie")
        self.space = make_space(self.a, self.b)
        (self.item,) = make_items(self.space, "Midnight swim")
        self.assignment = Assignment.objects.create(space=self.space, item=self.item, assigned_by=self.a)
        self.assignment.assignees.set([self.b])

    def url(self, name):
        return reverse(f"assignments:{name}", args=[self.space.id, self.assignment.id])

    def test_assignee_checks_off_with_note(self):
        self.client.force_login(self.b)
        response = self.client.post(self.url("complete"), {"note": "  Freezing, worth it  ", "tab": "active"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response["HX-Trigger"], "celebrate")
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, Assignment.COMPLETED)
        self.assertEqual(self.assignment.completed_by, self.b)
        self.assertEqual(self.assignment.note, "Freezing, worth it")

    def test_non_assignee_cannot_check_off(self):
        self.client.force_login(self.a)
        self.assertEqual(self.client.post(self.url("complete")).status_code, 403)
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, Assignment.ACTIVE)

    def test_assigner_can_put_it_back(self):
        self.client.force_login(self.a)
        self.client.post(self.url("release"))
        self.assertFalse(Assignment.objects.exists())

    def test_list_filters_mine_and_all(self):
        self.client.force_login(self.a)
        base = reverse("assignments:list", args=[self.space.id])
        self.assertNotContains(self.client.get(base), "Midnight swim")
        self.assertContains(self.client.get(base + "?who=all"), "Midnight swim")
        self.client.force_login(self.b)
        self.assertContains(self.client.get(base), "✓ Done")
