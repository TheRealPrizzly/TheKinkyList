import random
from collections import Counter
from types import SimpleNamespace

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from assignments.models import Assignment
from kinkylist.test_utils import make_items, make_space, make_user

from . import logic
from .registry import GAMES


def fake(id, title="", category="", description=""):
    return SimpleNamespace(id=id, title=title or f"Item {id}", category=category, description=description)


class SelectionLogicTests(SimpleTestCase):
    def test_draw_random_never_repeats_excluded_items(self):
        pool = [fake(i) for i in range(1, 6)]
        rng = random.Random(1)
        drawn = set()
        for _ in range(5):
            item = logic.draw_random(pool, drawn, rng)
            self.assertNotIn(item.id, drawn)
            drawn.add(item.id)
        self.assertIsNone(logic.draw_random(pool, drawn, rng))

    def test_sample_options_keeps_selected_first_and_caps_count(self):
        pool = [fake(i) for i in range(1, 30)]
        options = logic.sample_options(pool, 10, random.Random(2), keep_ids={3, 7})
        self.assertEqual(len(options), 10)
        self.assertEqual({o.id for o in options[:2]}, {3, 7})
        self.assertEqual(len({o.id for o in options}), 10)

    def test_sample_options_with_small_pool(self):
        pool = [fake(i) for i in range(1, 4)]
        self.assertEqual(len(logic.sample_options(pool, 10, random.Random(3))), 3)

    def test_search_requires_every_word_and_ranks_title_hits_first(self):
        pool = [
            fake(1, "Beach picnic", "Outdoors"),
            fake(2, "Sunset kiss", "Romance", "on the beach at dusk"),
            fake(3, "Massage night", "Romance"),
        ]
        self.assertEqual([i.id for i in logic.search_items(pool, "beach")], [1, 2])
        self.assertEqual([i.id for i in logic.search_items(pool, "beach dusk")], [2])
        self.assertEqual([i.id for i in logic.search_items(pool, "", "romance")], [3, 2])
        self.assertEqual(len(logic.search_items(pool)), 3)

    def test_draw_new_favours_less_explored_categories(self):
        pool = [fake(i, category="Romance") for i in range(1, 11)] + [fake(i, category="Adventure") for i in range(11, 21)]
        completed = Counter({"romance": 9})  # weight 0.1 vs 1.0
        rng = random.Random(4)
        picks = Counter(logic.draw_new(pool, completed, set(), rng).category for _ in range(2000))
        self.assertGreater(picks["Adventure"], picks["Romance"] * 5)

    def test_draw_new_respects_exclusions(self):
        pool = [fake(1, category="A"), fake(2, category="B")]
        self.assertEqual(logic.draw_new(pool, Counter(), {1}, random.Random(5)).id, 2)
        self.assertIsNone(logic.draw_new(pool, Counter(), {1, 2}, random.Random(5)))

    def test_parse_ids(self):
        self.assertEqual(logic.parse_ids("3, 1,x,3,,2"), [3, 1, 2])
        self.assertEqual(logic.parse_ids(["5", "-1", "5", "6"]), [5, 6])


class PoolTests(TestCase):
    def setUp(self):
        self.user = make_user("a")
        self.space = make_space(self.user)
        self.fresh, self.active, self.done, self.archived = make_items(self.space, "Fresh", "Active", "Done", "Archived")
        self.archived.archived = True
        self.archived.save()
        Assignment.objects.create(space=self.space, item=self.active)
        Assignment.objects.create(space=self.space, item=self.done, status=Assignment.COMPLETED)

    def titles(self, game, include_completed=False):
        return sorted(i.title for i in logic.eligible_items(self.space, GAMES[game], include_completed))

    def test_default_pool_excludes_archived_active_and_completed(self):
        self.assertEqual(self.titles("randomize"), ["Fresh"])

    def test_include_completed(self):
        self.assertEqual(self.titles("favorite", include_completed=True), ["Done", "Fresh"])

    def test_try_new_only_uses_never_assigned_items(self):
        self.assertEqual(self.titles("new", include_completed=True), ["Fresh"])


class GameViewTests(TestCase):
    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Julie")
        self.space = make_space(self.a, self.b)
        self.items = make_items(self.space, *[f"Wish {n}" for n in range(1, 13)], category="Romance")
        self.client.force_login(self.a)

    def url(self, name, slug="favorite", **kwargs):
        return reverse(f"games:{name}", kwargs={"space_id": self.space.id, "slug": slug, **kwargs})

    def test_every_game_page_renders(self):
        for slug in GAMES:
            response = self.client.get(self.url("play", slug))
            self.assertContains(response, GAMES[slug].name)

    def test_non_member_gets_404(self):
        self.client.force_login(make_user("stranger"))
        self.assertEqual(self.client.get(self.url("play")).status_code, 404)

    def test_feeds(self):
        response = self.client.get(self.url("feed", "randomize"), {"exclude": ",".join(str(i.id) for i in self.items[:-1])})
        self.assertContains(response, "Wish 12")
        response = self.client.get(self.url("feed", "search"), {"q": "wish 1"})
        self.assertContains(response, "Wish 10")
        self.assertNotContains(response, "Wish 2<")
        response = self.client.get(self.url("feed", "new"), {"exclude": ",".join(str(i.id) for i in self.items)})
        self.assertContains(response, "exhausted = true")

    def test_assign_rejects_too_many_picks(self):
        response = self.client.post(self.url("assign"), {"item": [i.id for i in self.items[:4]]})
        self.assertRedirects(response, self.url("play"))
        self.assertFalse(Assignment.objects.exists())

    def test_assign_rejects_items_from_another_space(self):
        (foreign,) = make_items(make_space(make_user("c"), name="Other"), "Not yours")
        response = self.client.post(self.url("assign"), {"item": [foreign.id]})
        self.assertRedirects(response, self.url("play"))

    def test_assign_requires_someone_per_item_and_ignores_non_members(self):
        stranger = make_user("stranger")
        item = self.items[0]
        response = self.client.post(
            self.url("assign"), {"item": [item.id], "confirm": "1", f"assign-{item.id}": [stranger.id]}
        )
        self.assertContains(response, "Choose at least one person.")
        self.assertFalse(Assignment.objects.exists())

    def test_full_flow_creates_session_and_assignments(self):
        first, second = self.items[:2]
        response = self.client.post(
            self.url("assign"),
            {
                "item": [first.id, second.id],
                "confirm": "1",
                f"assign-{first.id}": [self.a.id, self.b.id],
                f"assign-{second.id}": [self.b.id],
            },
        )
        assignment = Assignment.objects.get(item=first)
        done_url = reverse("games:done", kwargs={"space_id": self.space.id, "session_id": assignment.session_id})
        self.assertRedirects(response, done_url)
        self.assertEqual(set(assignment.assignees.all()), {self.a, self.b})
        self.assertEqual(list(Assignment.objects.get(item=second).assignees.all()), [self.b])
        self.assertEqual(assignment.session.game_type, "favorite")
        self.assertContains(self.client.get(response.url), "It's a date.")
        # Assigned items leave the pool.
        self.assertNotIn(first, logic.eligible_items(self.space, GAMES["favorite"]))
