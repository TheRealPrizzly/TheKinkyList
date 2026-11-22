import random
from collections import Counter
from types import SimpleNamespace

from datetime import timedelta

from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment, Reply
from kinkylist.test_utils import make_items, make_space, make_user

from . import logic
from .registry import GAMES


def fake(id, title="", categories=(), description=""):
    return SimpleNamespace(id=id, title=title or f"Item {id}", category_names=list(categories), description=description)


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
            fake(1, "Beach picnic", ["Outdoors"]),
            fake(2, "Sunset kiss", ["Romance", "Outdoors"], "on the beach at dusk"),
            fake(3, "Massage night", ["Romance"]),
        ]
        self.assertEqual([i.id for i in logic.search_items(pool, "beach")], [1, 2])
        self.assertEqual([i.id for i in logic.search_items(pool, "beach dusk")], [2])
        self.assertEqual([i.id for i in logic.search_items(pool, "", "romance")], [3, 2])
        self.assertEqual(len(logic.search_items(pool)), 3)
        self.assertEqual([i.id for i in logic.search_items(pool, "", "outdoors")], [1, 2])
        self.assertEqual([i.id for i in logic.search_items(pool, "outdoors")], [1, 2])

    def test_draw_new_favours_less_explored_categories(self):
        pool = [fake(i, categories=["Romance"]) for i in range(1, 11)] + [
            fake(i, categories=["Adventure"]) for i in range(11, 21)
        ]
        completed = Counter({"romance": 9})  # weight 0.1 vs 1.0
        rng = random.Random(4)
        picks = Counter(logic.draw_new(pool, completed, set(), rng).category_names[0] for _ in range(2000))
        self.assertGreater(picks["Adventure"], picks["Romance"] * 5)

    def test_draw_new_reaches_an_item_through_any_of_its_categories(self):
        pool = [fake(1, categories=["Romance"]), fake(2, categories=["Romance", "Adventure"]), fake(3)]
        completed = Counter({"romance": 1000, "": 1000})
        picks = Counter(logic.draw_new(pool, completed, set(), random.Random(6)).id for _ in range(500))
        self.assertGreater(picks[2], 450)

    def test_draw_new_respects_exclusions(self):
        pool = [fake(1, categories=["A"]), fake(2, categories=["B"])]
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
        self.items = make_items(self.space, *[f"Wish {n}" for n in range(1, 13)], categories=["Romance"])
        self.client.force_login(self.a)

    def url(self, name, slug="favorite", **kwargs):
        return reverse(f"games:{name}", kwargs={"space_id": self.space.id, "slug": slug, **kwargs})

    def test_every_game_page_renders(self):
        for slug in GAMES:
            response = self.client.get(self.url("play", slug))
            self.assertContains(response, GAMES[slug].name)

    def test_play_page_offers_the_kinky_list_game_instead_of_its_modes(self):
        response = self.client.get(reverse("games:index", args=[self.space.id]))
        self.assertEqual(
            [game.slug for game in response.context["games"]], ["kinky-list", "truth-or-dare", "would-you-rather"]
        )
        self.assertContains(response, self.url("play", "kinky-list"))
        self.assertNotContains(response, self.url("play", "randomize"))
        dashboard = self.client.get(reverse("spaces:dashboard", args=[self.space.id]))
        self.assertEqual([game.slug for game in dashboard.context["games"]], ["kinky-list", "truth-or-dare", "would-you-rather"])

    def test_kinky_list_game_offers_every_mode(self):
        response = self.client.get(self.url("play", "kinky-list"))
        self.assertContains(response, "Choose a mode")
        self.assertContains(response, "12 wishes ready")
        for slug in ("randomize", "favorite", "search", "new"):
            self.assertContains(response, f'href="{self.url("play", slug)}"')
            self.assertContains(response, GAMES[slug].name)
        # It has nothing to draw or assign itself.
        self.assertEqual(self.client.get(self.url("feed", "kinky-list")).status_code, 404)
        self.assertEqual(self.client.post(self.url("assign", "kinky-list"), {"item": [self.items[0].id]}).status_code, 404)

    def test_each_mode_links_back_and_to_the_other_modes(self):
        response = self.client.get(self.url("play", "search"))
        self.assertContains(response, f'<a href="{self.url("play", "kinky-list")}">Kinky List</a>')
        self.assertEqual([mode.slug for mode in response.context["modes"]], ["randomize", "favorite", "search", "new"])
        self.assertContains(response, 'aria-current="page">Just ask!</a>')
        self.assertNotIn("modes", self.client.get(self.url("play", "would-you-rather")).context)

    def test_favorite_offers_eight_options(self):
        self.assertEqual(len(self.client.get(self.url("play")).context["options"]), 8)
        self.assertEqual(len(self.client.get(self.url("feed")).context["options"]), 8)

    def test_randomize_waits_for_the_button(self):
        response = self.client.get(self.url("play", "randomize"))
        self.assertContains(response, "Randomize</span>")
        self.assertNotContains(response, "data-id=")
        self.assertEqual([c.name for c in response.context["filter_categories"]], ["Romance"])
        self.assertFalse(response.context["has_uncategorized"])

    def test_randomize_draws_only_the_chosen_intensity_and_categories(self):
        Item = type(self.items[0])
        spicy, sizzling, bare = (
            Item.objects.create(space=self.space, title=title, spice=spice)
            for title, spice in [("Spicy one", 2), ("Sizzling one", 3), ("Bare spicy", 2)]
        )
        spicy.set_categories(["Outdoors"])
        sizzling.set_categories(["Outdoors"])
        outdoors = spicy.categories.get()
        romance = self.items[0].categories.get()

        def drawn(**params):
            titles = set()
            for _ in range(40):
                response = self.client.get(self.url("feed", "randomize"), params)
                if response.context and "item" in response.context:
                    titles.add(response.context["item"].title)
            return titles

        self.assertEqual(drawn(spice="2"), {"Spicy one", "Bare spicy"})
        self.assertEqual(drawn(spice="2", category=str(outdoors.id)), {"Spicy one"})
        self.assertEqual(drawn(spice="2,3", category=f"{outdoors.id},none"), {"Spicy one", "Sizzling one", "Bare spicy"})
        self.assertEqual(drawn(category="none"), {"Bare spicy"})
        self.assertTrue(drawn(category=str(romance.id)) <= {f"Wish {n}" for n in range(1, 13)})
        response = self.client.get(self.url("feed", "randomize"), {"spice": "3", "category": str(romance.id)})
        self.assertContains(response, "exhausted = true")

    def test_randomize_again_avoids_what_was_shown_unless_nothing_else_is_left(self):
        shown = ",".join(str(item.id) for item in self.items[:11])
        for _ in range(10):
            response = self.client.get(self.url("feed", "randomize"), {"avoid": shown})
            self.assertEqual(response.context["item"], self.items[11])
        every_id = ",".join(str(item.id) for item in self.items)
        response = self.client.get(self.url("feed", "randomize"), {"avoid": every_id})
        self.assertIn(response.context["item"], self.items)

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

    def decline(self, item, user, days_ago=0):
        reply = Reply.objects.create(space=self.space, item=item, user=user, kind=Reply.NOT_FOR_ME)
        Reply.objects.filter(pk=reply.pk).update(created_at=timezone.now() - timedelta(days=days_ago))

    def test_assign_refuses_someone_who_said_not_for_me(self):
        item = self.items[0]
        self.decline(item, self.b)
        response = self.client.post(self.url("assign"), {"item": [item.id]})
        self.assertContains(response, "not for now")
        response = self.client.post(
            self.url("assign"), {"item": [item.id], "confirm": "1", f"assign-{item.id}": [self.b.id]}
        )
        self.assertContains(response, "Julie said this isn&#x27;t for them.")
        self.assertFalse(Assignment.objects.exists())
        self.client.post(self.url("assign"), {"item": [item.id], "confirm": "1", f"assign-{item.id}": [self.a.id]})
        self.assertEqual(list(Assignment.objects.get().assignees.all()), [self.a])

    def test_not_for_me_wears_off_after_six_months(self):
        item = self.items[0]
        self.decline(item, self.b, days_ago=183)
        self.client.post(self.url("assign"), {"item": [item.id], "confirm": "1", f"assign-{item.id}": [self.b.id]})
        self.assertEqual(list(Assignment.objects.get().assignees.all()), [self.b])

    def test_items_everyone_declined_leave_the_pool(self):
        item = self.items[0]
        self.decline(item, self.b)
        self.assertIn(item, logic.eligible_items(self.space, GAMES["favorite"]))
        self.decline(item, self.a)
        self.assertNotIn(item, logic.eligible_items(self.space, GAMES["favorite"]))

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


class TruthOrDareLogicTests(SimpleTestCase):
    def test_draw_fresh_avoids_seen_cards_then_starts_over_without_repeating_the_current_one(self):
        pool = [fake(i) for i in range(1, 4)]
        rng = random.Random(7)
        self.assertEqual(logic.draw_fresh(pool, {1, 2}, rng), (pool[2], False))
        for _ in range(20):
            card, recycled = logic.draw_fresh(pool, {1, 2, 3}, rng, current=3)
            self.assertTrue(recycled)
            self.assertNotEqual(card.id, 3)
        self.assertEqual(logic.draw_fresh([pool[0]], {1}, rng, current=1), (None, False))

    def test_dares_for_drops_what_the_player_declined(self):
        pool = [fake(1), fake(2)]
        self.assertEqual([i.id for i in logic.dares_for(pool, 5, {(1, 5): None, (2, 6): None})], [2])

    def test_parse_keys(self):
        self.assertEqual(logic.parse_keys("b1, t4,,b1"), ["b1", "t4"])

    def test_built_in_truths_and_dares_have_plenty_at_every_intensity(self):
        from .dares import BUILT_IN_DARES
        from .truths import BUILT_IN_TRUTHS

        for built_ins in (BUILT_IN_TRUTHS, BUILT_IN_DARES):
            self.assertGreaterEqual(len(built_ins), 100)
            self.assertEqual(len({text.lower() for _, text in built_ins}), len(built_ins))
            counts = Counter(spice for spice, _ in built_ins)
            self.assertEqual(set(counts), {1, 2, 3})
            self.assertGreaterEqual(min(counts.values()), 30)
        # Saved-for-later dares become list items, whose titles are capped at 140 characters.
        self.assertLessEqual(max(len(text) for _, text in BUILT_IN_DARES), 140)


class TruthOrDareViewTests(TestCase):
    """Each space plays from its own Truth or Dare list; wishes from The Kinky List join the dares only with mix=1."""

    def setUp(self):
        self.a = make_user("a", "Alex")
        self.b = make_user("b", "Julie")
        self.space = make_space(self.a, self.b)
        self.sweet, self.sizzling = make_items(self.space, "Slow dance", "Blindfold")
        self.sizzling.spice = 3
        self.sizzling.save()
        self.client.force_login(self.a)
        self.feed_url = reverse("games:feed", kwargs={"space_id": self.space.id, "slug": "truth-or-dare"})
        self.dare_url = reverse("games:dare", kwargs={"space_id": self.space.id})
        self.play_url = reverse("games:play", kwargs={"space_id": self.space.id, "slug": "truth-or-dare"})

    def feed(self, **params):
        return self.client.get(self.feed_url, {"player": self.b.id, **params})

    def test_page_lists_players_and_has_no_assign_step(self):
        self.space.truths.create(text="Best kiss?")
        self.space.dares.create(text="Kiss my neck")
        response = self.client.get(self.play_url)
        self.assertContains(response, "Who's playing?")
        self.assertContains(response, "Julie")
        self.assertContains(response, "1 truth and")
        self.assertEqual(response.context["config"]["dareCount"], 1)
        self.assertEqual(response.context["config"]["wishCount"], 2)
        self.assertNotContains(response, "Include things we've already done")
        response = self.client.post(
            reverse("games:assign", kwargs={"space_id": self.space.id, "slug": "truth-or-dare"}),
            {"item": [self.sweet.id]},
        )
        self.assertEqual(response.status_code, 404)

    def test_an_empty_list_says_how_to_fill_it(self):
        self.assertContains(self.client.get(self.play_url), "Your Truth or Dare list is empty")
        self.assertContains(self.feed(kind="truth"), "exhausted = true")

    def test_truths_come_from_this_spaces_list_and_respect_intensity(self):
        spicy = self.space.truths.create(text="  What's   our secret? ", spice=2)
        self.space.truths.create(text="Best kiss?", spice=1)
        make_space(make_user("c"), name="Other").truths.create(text="Not yours", spice=2)
        self.assertEqual(spicy.text, "What's our secret?")
        for _ in range(10):
            truth = self.feed(kind="truth", spice="2").context["truth"]
            self.assertEqual((truth.key, truth.spice), (f"t{spicy.id}", 2))

    def test_truths_start_over_once_all_are_seen(self):
        keys = [f"t{self.space.truths.create(text=text).id}" for text in ("One?", "Two?")]
        response = self.feed(kind="truth", exclude=",".join(keys), current=keys[0])
        self.assertTrue(response.context["recycled"])
        self.assertEqual(response.context["truth"].key, keys[1])
        self.assertContains(response, 'data-recycled="1"')

    def test_wishes_are_dares_only_when_mixed_in(self):
        self.assertContains(self.feed(kind="dare"), "exhausted = true")
        self.assertEqual(self.feed(kind="dare", spice="3", mix="1").context["item"], self.sizzling)

    def test_mixed_in_dares_respect_the_players_not_for_me(self):
        Reply.objects.create(space=self.space, item=self.sizzling, user=self.b, kind=Reply.NOT_FOR_ME)
        self.assertContains(self.feed(kind="dare", spice="3", mix="1"), "exhausted = true")
        # Alex never declined it.
        response = self.client.get(self.feed_url, {"player": self.a.id, "kind": "dare", "spice": "3", "mix": "1"})
        self.assertEqual(response.context["item"], self.sizzling)

    def test_feed_needs_a_player_from_this_space(self):
        self.assertEqual(self.client.get(self.feed_url, {"kind": "truth"}).status_code, 404)
        stranger = make_user("stranger")
        self.assertEqual(self.client.get(self.feed_url, {"kind": "truth", "player": stranger.id}).status_code, 404)

    def test_done_wish_is_lived_and_later_goes_to_the_players_to_do(self):
        response = self.client.post(self.dare_url, {"item": self.sweet.id, "player": self.b.id, "outcome": "done"})
        self.assertEqual(response.json()["message"], "Julie did it! It's on your list as lived.")
        done = Assignment.objects.get(item=self.sweet)
        self.assertEqual((done.status, done.completed_by, list(done.assignees.all())), ("completed", self.b, [self.b]))
        self.assertEqual(done.session.game_type, "truth-or-dare")

        session = response.json()["session"]
        response = self.client.post(
            self.dare_url, {"item": self.sizzling.id, "player": self.b.id, "outcome": "later", "session": session}
        )
        self.assertEqual(response.json(), {"session": session, "message": "Saved to Julie's To-do."})
        later = Assignment.objects.get(item=self.sizzling)
        self.assertEqual((later.status, later.assigned_by, later.session_id), ("active", self.a, session))
        # Both are out of the dare pool now.
        self.assertContains(self.feed(kind="dare", mix="1"), "exhausted = true")

    def test_dare_rejects_unavailable_declined_and_foreign_items(self):
        Assignment.objects.create(space=self.space, item=self.sweet)
        response = self.client.post(self.dare_url, {"item": self.sweet.id, "player": self.b.id, "outcome": "done"})
        self.assertEqual(response.status_code, 409)
        Reply.objects.create(space=self.space, item=self.sizzling, user=self.b, kind=Reply.NOT_FOR_ME)
        response = self.client.post(self.dare_url, {"item": self.sizzling.id, "player": self.b.id, "outcome": "done"})
        self.assertEqual(response.json()["error"], "Julie said this isn't for them.")
        other = make_space(make_user("c"), name="Other")
        (foreign,) = make_items(other, "Not yours")
        foreign_dare = other.dares.create(text="Not yours either")
        for key in (foreign.id, f"d{foreign_dare.id}"):
            response = self.client.post(self.dare_url, {"item": key, "player": self.a.id, "outcome": "later"})
            self.assertEqual(response.status_code, 409)
        response = self.client.post(self.dare_url, {"item": self.sizzling.id, "player": self.a.id, "outcome": "maybe"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_list_dares_are_drawn_unless_already_on_the_kinky_list(self):
        tie = self.space.dares.create(text="Tie me up", spice=3)
        self.space.dares.create(text="Blindfold", spice=3)
        self.space.dares.create(text="Kiss my neck", spice=1)
        ids = {str(self.feed(kind="dare", spice="3").context["item"].id) for _ in range(30)}
        # "Blindfold" is already on The Kinky List, so it's left out.
        self.assertEqual(ids, {f"d{tie.id}"})
        response = self.feed(kind="dare", spice="3", mix="1", exclude=f"{self.sizzling.id}")
        self.assertContains(response, f'data-key="d{tie.id}"')
        self.assertContains(response, "Tie me up")

    def test_list_dare_done_records_nothing_and_later_saves_it_to_the_kinky_list(self):
        key = f"d{self.space.dares.create(text='Tie me up', spice=2).id}"
        response = self.client.post(self.dare_url, {"item": key, "player": self.b.id, "outcome": "done"})
        self.assertEqual(response.json()["message"], "Julie did it!")
        self.assertFalse(Assignment.objects.exists())

        response = self.client.post(self.dare_url, {"item": key, "player": self.b.id, "outcome": "later"})
        self.assertEqual(response.json()["message"], "Saved to Julie's To-do.")
        item = self.space.items.get(title="Tie me up")
        self.assertEqual((item.spice, item.category_names), (2, ["Truth or Dare"]))
        self.assertEqual(list(Assignment.objects.get(item=item).assignees.all()), [self.b])
        # It's in progress now, so it leaves the draw and can't be saved twice.
        self.assertEqual(logic.dare_pool(self.space), [])
        response = self.client.post(self.dare_url, {"item": key, "player": self.a.id, "outcome": "later"})
        self.assertEqual(response.status_code, 409)
        response = self.client.post(self.dare_url, {"item": "d999", "player": self.a.id, "outcome": "later"})
        self.assertEqual(response.status_code, 409)


class BuiltInQuestionTests(SimpleTestCase):
    """What "Generate a list" fills the "Would you rather" list with."""

    def test_built_in_questions_are_plenty_unique_and_spread_across_intensities(self):
        from .would_you_rather import BUILT_IN_QUESTIONS

        self.assertGreaterEqual(len(BUILT_IN_QUESTIONS), 100)
        pairs = {(first.lower(), second.lower()) for _, first, second in BUILT_IN_QUESTIONS}
        self.assertEqual(len(pairs), len(BUILT_IN_QUESTIONS))
        # They have to fit Question.first and Question.second.
        self.assertLessEqual(max(max(len(first), len(second)) for _, first, second in BUILT_IN_QUESTIONS), 120)
        counts = Counter(spice for spice, *_ in BUILT_IN_QUESTIONS)
        self.assertEqual(set(counts), {1, 2, 3})
        self.assertGreaterEqual(min(counts.values()), 30)


class WouldYouRatherTests(TestCase):
    def setUp(self):
        from items.lists import WOULD_YOU_RATHER

        self.a = make_user("a", "Alex")
        self.space = make_space(self.a)
        WOULD_YOU_RATHER.generate(self.space)
        self.client.force_login(self.a)
        self.feed_url = reverse("games:feed", kwargs={"space_id": self.space.id, "slug": "would-you-rather"})
        self.play_url = reverse("games:play", kwargs={"space_id": self.space.id, "slug": "would-you-rather"})

    def test_page_renders_without_an_assign_step(self):
        self.assertContains(self.client.get(self.play_url), "100 questions are ready")
        response = self.client.post(
            reverse("games:assign", kwargs={"space_id": self.space.id, "slug": "would-you-rather"}), {"item": [1]}
        )
        self.assertEqual(response.status_code, 404)

    def test_plays_from_this_spaces_list(self):
        self.space.questions.all().delete()
        self.assertContains(self.client.get(self.play_url), "Your Would you rather list is empty")
        question = self.space.questions.create(first="kiss", second="cuddle", spice=2)
        response = self.client.get(self.feed_url)
        self.assertEqual(response.context["question"].key, f"q{question.id}")
        self.assertContains(response, "Would you rather kiss or cuddle?")

    def test_questions_respect_intensity_and_start_over_once_all_are_seen(self):
        for _ in range(15):
            self.assertEqual(self.client.get(self.feed_url, {"spice": "3"}).context["question"].spice, 3)
        sizzling = [card.key for card in logic.question_pool(self.space, [3])]
        response = self.client.get(self.feed_url, {"spice": "3", "exclude": ",".join(sizzling[1:])})
        self.assertEqual(response.context["question"].key, sizzling[0])
        self.assertFalse(response.context["recycled"])
        response = self.client.get(self.feed_url, {"spice": "3", "exclude": ",".join(sizzling), "current": sizzling[0]})
        self.assertTrue(response.context["recycled"])
        self.assertNotEqual(response.context["question"].key, sizzling[0])
        self.assertContains(response, 'data-recycled="1"')
