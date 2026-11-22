"""Levels: steps inside a wish, ticked in the Done dialog as you reach them."""

import json
from unittest import mock

from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment
from games import logic
from games.registry import GAMES
from kinkylist.test_utils import make_items, make_space, make_user

from . import starter
from .models import MAX_LEVELS, Item, Level
from .utils import split_levels


class SplitLevelsTests(SimpleTestCase):
    def test_one_per_line_without_numbering_blanks_or_repeats(self):
        text = """
        1. A finger,   with lots of lube
        - A small plug

        Level 3: The real thing
        level 4) Again, slower
        a small plug
        """
        self.assertEqual(
            split_levels(text),
            ["A finger, with lots of lube", "A small plug", "The real thing", "Again, slower"],
        )

    def test_leaves_numbers_that_belong_to_the_text(self):
        self.assertEqual(split_levels("69-ing\n3 minutes, eyes closed"), ["69-ing", "3 minutes, eyes closed"])


class LevelModelTests(TestCase):
    def setUp(self):
        self.space = make_space(make_user("a"))
        (self.item,) = make_items(self.space, "Try anal play")

    def texts(self):
        return list(self.item.levels.values_list("text", "position"))

    def test_progress_counts_done_levels_and_names_the_next(self):
        self.assertIsNone(self.item.level_progress)
        self.item.set_levels(["A finger", "A small plug", "The real thing"])
        self.item.levels.filter(text="A finger").update(done_at=timezone.now())
        progress = Item.objects.get(pk=self.item.pk).level_progress
        self.assertEqual((progress.done, progress.total, progress.finished), (1, 3, False))
        self.assertEqual((progress.next.text, progress.next_number), ("A small plug", 2))

    def test_unchanged_levels_keep_their_progress_when_moved(self):
        self.item.set_levels(["A finger", "A small plug"])
        self.item.levels.filter(text="A small plug").update(done_at=timezone.now())
        self.item.set_levels(["a small plug", "Something new", "A finger"])
        self.assertEqual(self.texts(), [("a small plug", 0), ("Something new", 1), ("A finger", 2)])
        self.assertTrue(self.item.levels.get(text="a small plug").done_at)
        self.assertFalse(self.item.levels.get(text="Something new").done_at)

    def test_removed_levels_go(self):
        self.item.set_levels(["A finger", "A small plug"])
        self.item.set_levels(["A small plug"])
        self.assertEqual(self.texts(), [("A small plug", 0)])
        self.item.set_levels([])
        self.assertIsNone(self.item.level_progress)

    def test_reset_marks_every_level_not_done(self):
        self.item.set_levels(["A finger", "A small plug"])
        self.item.levels.update(done_at=timezone.now())
        self.item.reset_levels()
        self.assertFalse(self.item.levels.filter(done_at__isnull=False).exists())


class LevelEditingTests(TestCase):
    def setUp(self):
        self.user = make_user("a")
        self.space = make_space(self.user)
        self.client.force_login(self.user)
        self.list_url = reverse("items:list", args=[self.space.id])

    def edit_url(self, item):
        return reverse("items:edit", args=[self.space.id, item.id])

    def wish(self, **fields):
        return {"title": "Try anal play", "categories": "", "spice": 2, **fields}

    def test_add_a_wish_with_levels(self):
        self.client.post(self.list_url, self.wish(levels="1. A finger\n2. A small plug\n3. The real thing"))
        item = self.space.items.get()
        self.assertEqual(list(item.levels.values_list("text", flat=True)), ["A finger", "A small plug", "The real thing"])
        self.assertContains(self.client.get(self.list_url), "Level 1 of 3")

    def test_edit_keeps_progress_and_can_start_over(self):
        (item,) = make_items(self.space, "Try anal play")
        item.set_levels(["A finger", "A small plug"])
        item.levels.filter(text="A finger").update(done_at=timezone.now())
        response = self.client.get(self.edit_url(item))
        self.assertContains(response, "A finger\nA small plug</textarea>")
        self.assertContains(response, "Start the levels over")

        self.client.post(self.edit_url(item), self.wish(levels="A finger\nA small plug\nThe real thing"))
        self.assertEqual(item.levels.filter(done_at__isnull=False).count(), 1)
        self.assertContains(self.client.get(self.list_url), "1 of 3 levels")

        self.client.post(self.edit_url(item), self.wish(levels="A finger\nA small plug", reset_levels="on"))
        self.assertFalse(item.levels.filter(done_at__isnull=False).exists())

    def test_too_many_or_too_long_levels_are_refused(self):
        (item,) = make_items(self.space, "Try anal play")
        many = "\n".join(f"Step {n}" for n in range(MAX_LEVELS + 1))
        response = self.client.post(self.edit_url(item), self.wish(levels=many))
        self.assertContains(response, f"up to {MAX_LEVELS} levels")
        response = self.client.post(self.edit_url(item), self.wish(levels="Fine\n" + "x" * 141))
        self.assertContains(response, "Level 2 has 141")
        self.assertFalse(item.levels.exists())


class CheckOffLevelTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Julie")
        self.space = make_space(self.a, self.b)
        (self.item,) = make_items(self.space, "Try anal play")
        self.item.set_levels(["A finger", "A small plug", "The real thing"])
        self.finger, self.plug, self.full = self.item.levels.all()
        self.assignment = Assignment.objects.create(space=self.space, item=self.item, assigned_by=self.a)
        self.assignment.assignees.set([self.b])
        self.complete_url = reverse("assignments:complete", args=[self.space.id, self.assignment.id])
        self.list_url = reverse("assignments:list", args=[self.space.id])

    def test_the_done_button_carries_the_levels(self):
        self.client.force_login(self.b)
        response = self.client.get(self.list_url)
        self.assertContains(response, "Level 1 of 3")
        (assignment,) = response.context["assignments"]
        self.assertEqual(
            json.loads(assignment.levels_json),
            [
                {"id": self.finger.id, "text": "A finger", "done": False},
                {"id": self.plug.id, "text": "A small plug", "done": False},
                {"id": self.full.id, "text": "The real thing", "done": False},
            ],
        )

    def test_check_off_marks_the_levels_reached(self):
        (elsewhere,) = make_items(self.space, "Other wish")
        elsewhere.set_levels(["Not this one"])
        self.client.force_login(self.b)
        levels = f"{self.finger.id},{self.plug.id},{elsewhere.levels.get().id},junk"
        self.client.post(self.complete_url, {"levels": levels, "tab": "active"}, HTTP_HX_REQUEST="true")
        self.finger.refresh_from_db()
        self.assertEqual((self.finger.done_by, self.finger.done_in), (self.b, self.assignment))
        self.assertTrue(self.item.levels.get(pk=self.plug.pk).done_at)
        self.assertFalse(self.item.levels.get(pk=self.full.pk).done_at)
        self.assertFalse(elsewhere.levels.get().done_at)

        response = self.client.get(self.list_url + "?tab=completed")
        self.assertContains(response, "✓ A finger")
        self.assertContains(response, "✓ A small plug")
        self.assertNotContains(response, "✓ The real thing")

    def test_levels_already_done_keep_their_first_check_off(self):
        earlier = Assignment.objects.create(space=self.space, item=self.item, status=Assignment.COMPLETED)
        self.item.levels.filter(pk=self.finger.pk).update(done_at=timezone.now(), done_in=earlier)
        self.client.force_login(self.b)
        self.client.post(self.complete_url, {"levels": f"{self.finger.id},{self.plug.id}"})
        self.assertEqual(self.item.levels.get(pk=self.finger.pk).done_in, earlier)
        self.assertEqual(self.item.levels.get(pk=self.plug.pk).done_in, self.assignment)

    def test_without_levels_ticked_nothing_moves(self):
        self.client.force_login(self.b)
        response = self.client.post(self.complete_url, follow=True)
        self.assertContains(response, "0 of 3 levels done")
        self.assertFalse(self.item.levels.filter(done_at__isnull=False).exists())


class LevelPoolTests(TestCase):
    def setUp(self):
        self.space = make_space(make_user("a"))
        self.started, self.finished, self.plain = make_items(self.space, "Started", "Finished", "Plain")
        for item in (self.started, self.finished, self.plain):
            Assignment.objects.create(space=self.space, item=item, status=Assignment.COMPLETED)
        self.started.set_levels(["One", "Two"])
        self.started.levels.filter(text="One").update(done_at=timezone.now())
        self.finished.set_levels(["One"])
        self.finished.levels.update(done_at=timezone.now())

    def titles(self, game, include_completed=False):
        return sorted(i.title for i in logic.eligible_items(self.space, GAMES[game], include_completed))

    def test_a_lived_wish_with_levels_left_keeps_coming_up(self):
        self.assertEqual(self.titles("randomize"), ["Started"])
        self.assertEqual(self.titles("randomize", include_completed=True), ["Finished", "Plain", "Started"])

    def test_try_new_things_still_only_offers_wishes_never_drawn(self):
        self.assertEqual(self.titles("new", include_completed=True), [])


class StarterLevelTests(TestCase):
    def test_starter_wishes_get_their_built_in_levels(self):
        space = make_space(make_user("a"))
        title = starter.STARTER_WISHES[0][0]
        with mock.patch.dict(starter.STARTER_LEVELS, {title.lower(): ["Gently", "All the way"]}):
            starter.add_starter_list(space)
        item = space.items.get(title=title)
        self.assertEqual(list(item.levels.values_list("text", flat=True)), ["Gently", "All the way"])
        self.assertEqual(Level.objects.filter(item__space=space).count(), 2)
