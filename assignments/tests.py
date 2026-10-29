from django.test import TestCase
from django.urls import reverse

from kinkylist.test_utils import make_items, make_space, make_user

from .models import Assignment, Reply


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


class ReplyTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Julie")
        self.c = make_user("c", "Sam")
        self.space = make_space(self.a, self.b, self.c)
        (self.item,) = make_items(self.space, "Midnight swim")
        self.assignment = Assignment.objects.create(space=self.space, item=self.item, assigned_by=self.a)
        self.assignment.assignees.set([self.b])
        self.list_url = reverse("assignments:list", args=[self.space.id])

    def answer(self, user, kind):
        self.client.force_login(user)
        return self.client.post(
            reverse("assignments:reply", args=[self.space.id, self.assignment.id]), {"kind": kind}, HTTP_HX_REQUEST="true"
        )

    def test_interested_keeps_it_and_tells_the_requester_once(self):
        self.answer(self.b, Reply.INTERESTED)
        self.answer(self.b, Reply.INTERESTED)
        self.assertEqual(Reply.objects.count(), 1)
        self.assertEqual(Assignment.objects.get().status, Assignment.ACTIVE)
        self.assertContains(self.client.get(self.list_url), "Julie is interested")
        self.client.force_login(self.a)
        self.assertContains(self.client.get(self.list_url), "is interested in “Midnight swim”")

    def test_maybe_eventually_puts_it_back_and_tells_the_requester(self):
        self.answer(self.b, Reply.LATER)
        self.assertFalse(Assignment.objects.exists())
        self.client.force_login(self.a)
        response = self.client.get(self.list_url)
        self.assertContains(response, "would like “Midnight swim” eventually")
        self.assertContains(response, "It's back on the list.")
        reply = Reply.objects.get()
        self.client.post(reverse("assignments:dismiss_reply", args=[self.space.id, reply.id]))
        self.assertNotContains(self.client.get(self.list_url), "Midnight swim")

    def test_not_for_me_takes_one_person_off_a_shared_item(self):
        self.assignment.assignees.add(self.c)
        self.answer(self.b, Reply.INTERESTED)
        self.answer(self.b, Reply.NOT_FOR_ME)
        self.assertEqual(list(Assignment.objects.get().assignees.all()), [self.c])
        self.assertEqual(Reply.objects.get().kind, Reply.NOT_FOR_ME)
        self.assertNotEqual(Assignment.objects.get().status, Assignment.COMPLETED)
        self.assertIn((self.item.id, self.b.id), Reply.blocked_until_by_person(self.space))

    def test_only_assignees_can_answer(self):
        self.assertEqual(self.answer(self.a, Reply.NOT_FOR_ME).status_code, 403)
        self.assertEqual(self.answer(self.b, "whatever").status_code, 400)
        self.assertFalse(Reply.objects.exists())

    def test_answers_to_your_own_draws_are_not_announced(self):
        self.assignment.assigned_by = self.b
        self.assignment.save()
        self.answer(self.b, Reply.LATER)
        self.assertTrue(Reply.objects.get().seen)

    def test_only_the_requester_can_dismiss(self):
        self.answer(self.b, Reply.LATER)
        reply = Reply.objects.get()
        self.client.force_login(self.c)
        self.assertEqual(self.client.post(reverse("assignments:dismiss_reply", args=[self.space.id, reply.id])).status_code, 404)
