"""A wish's details in the games: shown on hover with a mouse, or on tap on a touch screen."""

from datetime import timedelta

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment
from kinkylist.test_utils import make_items, make_space, make_user

from . import logic


class AttachHistoryTests(TestCase):
    def setUp(self):
        self.space = make_space(make_user("a"))
        self.lived, self.fresh = make_items(self.space, "Lived", "Fresh")

    def complete(self, days_ago, note=""):
        Assignment.objects.create(
            space=self.space,
            item=self.lived,
            status=Assignment.COMPLETED,
            completed_at=timezone.now() - timedelta(days=days_ago),
            note=note,
        )

    def test_counts_and_finds_the_latest_date_and_memory(self):
        self.complete(30, "The first time")
        self.complete(10, "Even better")
        self.complete(2)
        logic.attach_history([self.lived, self.fresh, logic.dare_card(self.space.dares.create(text="Dare"))])
        self.assertEqual(self.lived.history.count, 3)
        self.assertEqual(self.lived.history.last_lived.date(), (timezone.now() - timedelta(days=2)).date())
        self.assertEqual(self.lived.history.last_memory, "Even better")
        self.assertEqual((self.fresh.history.count, self.fresh.history.last_memory), (0, ""))


class GameDetailsTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.space = make_space(self.a)
        self.client.force_login(self.a)
        (self.wish,) = make_items(self.space, "Try anal play", categories=["Toys"])
        self.wish.description = "Go slow.\nLots of lube."
        self.wish.spice = 3
        self.wish.save()
        self.wish.set_levels(["A finger", "A small plug", "The real thing"])
        self.wish.levels.filter(text="A finger").update(done_at=timezone.now())
        Assignment.objects.create(
            space=self.space, item=self.wish, status=Assignment.COMPLETED, completed_at=timezone.now(), note="Worth it"
        )

    def feed(self, slug, **params):
        return self.client.get(reverse("games:feed", args=[self.space.id, slug]), {"completed": "1", **params})

    def test_pick_cards_carry_every_detail(self):
        response = self.feed("favorite")
        html = response.content.decode()
        self.assertIn("data-details", html)
        self.assertIn('<template class="details-template">', html)
        for text in ("<p>Go slow.<br>Lots of lube.</p>", "Sizzling", "Toys", "1 of 3 done", "Up next", "Once, last on",
                     "Last memory", "“Worth it”"):
            self.assertIn(text, html)
        self.assertNotIn("<dt>Added</dt>", html)

    def test_randomize_and_try_new_cards_have_details_too(self):
        self.assertContains(self.feed("randomize"), "details-template")
        (fresh,) = make_items(self.space, "Never drawn")
        self.assertEqual(self.feed("new").context["item"], fresh)
        self.assertContains(self.feed("new"), "details-template")

    def test_truth_or_dare_shows_details_only_for_wishes(self):
        url = reverse("games:feed", args=[self.space.id, "truth-or-dare"])
        params = {"player": self.a.id, "kind": "dare", "completed": "1"}
        self.space.dares.create(text="Kiss my neck")
        self.assertNotContains(self.client.get(url, params), "details-template")
        self.space.dares.all().delete()
        response = self.client.get(url, {**params, "mix": "1"})
        self.assertEqual(response.context["item"], self.wish)
        self.assertContains(response, "details-template")
        self.assertContains(response, "Tap for the details")

    def test_play_page_explains_hover_and_tap(self):
        response = self.client.get(reverse("games:play", args=[self.space.id, "favorite"]) + "?completed=1")
        self.assertContains(response, "Hover over a wish to see everything about it.")
        self.assertContains(response, "or tap its circle to choose it")
        self.assertContains(response, 'id="details-sheet"')

    def test_more_cards_cost_no_more_queries(self):
        def queries():
            with CaptureQueriesContext(connection) as captured:
                self.feed("search")
            return len(captured)

        self.feed("search")  # The first visit also remembers this space on the profile.
        few = queries()
        for n in range(6):
            (item,) = make_items(self.space, f"Wish {n}", categories=["Toys"])
            item.set_levels(["One", "Two"])
            Assignment.objects.create(space=self.space, item=item, status=Assignment.COMPLETED, note="Nice")
        self.assertEqual(queries(), few)
