from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from assignments.models import Assignment

from kinkylist.test_utils import make_items, make_space, make_user

from .models import Category, Item
from .starter import category_names
from .utils import parse_bulk, parse_questions, parse_truths_and_dares, split_categories


class ParseBulkTests(SimpleTestCase):
    def parsed(self, text):
        return [(e.title, e.categories, e.spice, e.bad_spice) for e in parse_bulk(text)]

    def test_action_categories_and_intensity(self):
        text = """
        Candlelit bath | Romance, Relaxing | Sweet
        - Skinny dip | Adventure | 3
        2. Stargazing picnic
        candlelit bath | Other
        Lap dance | | spicy
        Note: time: 9pm dinner | Romance
        """
        self.assertEqual(
            self.parsed(text),
            [
                ("Candlelit bath", ["Romance", "Relaxing"], 1, False),
                ("Skinny dip", ["Adventure"], 3, False),
                ("Stargazing picnic", [], 1, False),
                ("Lap dance", [], 2, False),
                ("Note: time: 9pm dinner", ["Romance"], 1, False),
            ],
        )

    def test_tabs_from_a_spreadsheet(self):
        self.assertEqual(self.parsed("Massage\tRomance, Touch\tSizzling"), [("Massage", ["Romance", "Touch"], 3, False)])

    def test_unreadable_intensity_falls_back_to_sweet(self):
        self.assertEqual(
            self.parsed("Massage | Romance | 7\nDance | | hot"),
            [("Massage", ["Romance"], 1, True), ("Dance", [], 1, True)],
        )

    def test_split_categories_trims_and_dedupes(self):
        self.assertEqual(split_categories(" Romance ,, romance, Big   adventure "), ["Romance", "Big adventure"])


class ItemViewTests(TestCase):
    def setUp(self):
        self.user = make_user("a")
        self.space = make_space(self.user)
        self.client.force_login(self.user)

    def test_bulk_add_skips_existing_titles(self):
        make_items(self.space, "Candlelit bath")
        url = reverse("items:bulk", args=[self.space.id])
        self.client.post(url, {"lines": "candlelit bath | Romance\nDance in the rain | Romance"})
        self.assertEqual(sorted(self.space.items.values_list("title", flat=True)), ["Candlelit bath", "Dance in the rain"])

    def test_bulk_add_sets_categories_and_intensity_and_reuses_categories(self):
        make_items(self.space, "Existing", categories=["Romance"])
        url = reverse("items:bulk", args=[self.space.id])
        response = self.client.post(
            url, {"lines": "Dance in the rain | romance, Outdoors | Spicy\nSkinny dip | | 9"}, follow=True
        )
        dance = self.space.items.get(title="Dance in the rain")
        self.assertEqual(dance.category_names, ["Outdoors", "Romance"])
        self.assertEqual(dance.spice, 2)
        self.assertEqual(self.space.items.get(title="Skinny dip").spice, 1)
        self.assertEqual(sorted(self.space.categories.values_list("name", flat=True)), ["Outdoors", "Romance"])
        self.assertContains(response, "1 line had an intensity we didn")

    def test_add_and_edit_with_several_categories(self):
        list_url = reverse("items:list", args=[self.space.id])
        self.client.post(list_url, {"title": "Massage", "categories": "Touch, Romance", "spice": 3})
        item = self.space.items.get()
        self.assertEqual((item.category_names, item.spice), (["Romance", "Touch"], 3))
        edit_url = reverse("items:edit", args=[self.space.id, item.id])
        self.assertContains(self.client.get(edit_url), 'value="Romance, Touch"')
        self.client.post(edit_url, {"title": "Massage", "categories": "touch", "spice": 1})
        self.assertEqual(item.category_names, ["Touch"])

    def test_list_filters_by_any_category_and_hides_unused_ones(self):
        make_items(self.space, "Beach", categories=["Outdoors", "Romance"])
        make_items(self.space, "Bath", categories=["Romance"])
        Category.objects.create(space=self.space, name="Unused")
        url = reverse("items:list", args=[self.space.id])
        response = self.client.get(url, {"category": "outdoors"})
        self.assertEqual([i.title for i in response.context["items"]], ["Beach"])
        self.assertEqual(response.context["categories"], ["Outdoors", "Romance"])

    def test_other_space_items_are_not_editable(self):
        other = make_space(make_user("b"), name="Them")
        (item,) = make_items(other, "Secret")
        response = self.client.get(reverse("items:edit", args=[self.space.id, item.id]))
        self.assertEqual(response.status_code, 404)

    def test_clear_deletes_only_this_spaces_items_and_assignments(self):
        mine = make_items(self.space, "One", "Two")
        Assignment.objects.create(space=self.space, item=mine[0])
        other = make_space(make_user("b"), name="Them")
        make_items(other, "Theirs")
        response = self.client.post(reverse("items:clear", args=[self.space.id, "kinky-list"]))
        self.assertRedirects(response, reverse("items:list", args=[self.space.id]))
        self.assertFalse(self.space.items.exists())
        self.assertFalse(Assignment.objects.filter(space=self.space).exists())
        self.assertEqual(other.items.count(), 1)

    def test_clear_requires_post_and_membership(self):
        url = reverse("items:clear", args=[self.space.id, "kinky-list"])
        make_items(self.space, "Keep me")
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.force_login(make_user("stranger"))
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertEqual(self.space.items.count(), 1)


class StarterListTests(TestCase):
    def setUp(self):
        from items.starter import STARTER_WISHES

        self.wishes = STARTER_WISHES
        self.user = make_user("a")
        self.client.force_login(self.user)

    def test_starter_wishes_have_one_category_or_a_tuple_of_them(self):
        for _, category, _, _ in self.wishes:
            self.assertTrue(category_names(category))

    def test_starter_wishes_fit_and_are_unique(self):
        titles = [title.lower() for title, *_ in self.wishes]
        self.assertEqual(len(titles), 134)
        self.assertEqual(len(set(titles)), len(titles))
        self.assertLessEqual(max(len(title) for title, *_ in self.wishes), Item._meta.get_field("title").max_length)
        self.assertEqual({spice for _, _, spice, _ in self.wishes}, {1, 2, 3})

    def test_starter_levels_belong_to_starter_wishes_and_fit(self):
        from items.models import MAX_LEVELS, Level
        from items.starter import STARTER_LEVELS

        titles = {title.lower() for title, *_ in self.wishes}
        self.assertEqual(set(STARTER_LEVELS) - titles, set())
        limit = Level._meta.get_field("text").max_length
        for levels in STARTER_LEVELS.values():
            self.assertLessEqual(len(levels), MAX_LEVELS)
            self.assertEqual(len({level.lower() for level in levels}), len(levels))
            self.assertLessEqual(max(len(level) for level in levels), limit)

    def test_new_spaces_start_with_all_three_lists(self):
        from games.dares import BUILT_IN_DARES
        from games.truths import BUILT_IN_TRUTHS
        from games.would_you_rather import BUILT_IN_QUESTIONS

        self.client.post(reverse("spaces:create"), {"name": "Us"})
        space = self.user.memberships.get().space
        self.assertEqual(space.items.count(), 134)
        item = space.items.get(title__startswith="Next time your partner receives")
        self.assertEqual((item.spice, item.category_names), (1, ["Challenge"]))
        self.assertIn("Hang up when the deed is done.", item.description)
        groped = space.items.get(title="Be groped in public.")
        self.assertEqual(groped.category_names, ["Public", "Teasing", "Voyeurism"])
        self.assertEqual(groped.levels.count(), 3)
        names = {name for _, category, _, _ in self.wishes for name in category_names(category)}
        self.assertEqual(space.categories.count(), len(names))
        self.assertEqual(space.truths.count(), len(BUILT_IN_TRUTHS))
        self.assertEqual(space.dares.count(), len(BUILT_IN_DARES))
        self.assertEqual(space.questions.count(), len(BUILT_IN_QUESTIONS))

    def test_generate_adds_only_whats_missing(self):
        space = make_space(self.user)
        url = reverse("items:list", kwargs={"space_id": space.id})
        generate_url = reverse("items:generate", kwargs={"space_id": space.id, "list_slug": "kinky-list"})
        self.assertContains(self.client.get(url), "Fills it with our 134 wishes.")
        make_items(space, "GO SKINNY DIPPING AT NIGHT.")
        self.assertContains(self.client.get(url), "Adds back the 133 of our 134 that aren’t on it.")
        response = self.client.post(generate_url, follow=True)
        self.assertContains(response, "Added 133 wishes to The Kinky List.")
        self.assertEqual(space.items.count(), 134)
        self.assertContains(response, "All 134 of ours are on it.")
        response = self.client.post(generate_url, follow=True)
        self.assertContains(response, "Everything we have for The Kinky List is already on your list.")


class ParseGameListTests(SimpleTestCase):
    def test_truths_and_dares_take_a_default_kind_or_a_kind_column(self):
        entries = parse_truths_and_dares(
            "Best kiss? | Spicy\n- Dare | Kiss my neck | 3\n2. best KISS?\nTruth\tWorst date\thot\n\nDare", "truth"
        )
        self.assertEqual(
            [(e.kind, e.text, e.spice, e.bad_spice) for e in entries],
            [
                ("truth", "Best kiss?", 2, False),
                ("dare", "Kiss my neck", 3, False),
                ("truth", "Worst date", 1, True),
                # A lone "Dare" is a dare-less line, so it's read as the text itself.
                ("truth", "Dare", 1, False),
            ],
        )
        self.assertEqual([e.kind for e in parse_truths_and_dares("Kiss me", "dare")], ["dare"])

    def test_questions_as_columns_or_written_out(self):
        entries, unreadable = parse_questions(
            "be tied up | do the tying | Spicy\n"
            "Would you rather kiss or cuddle? | 3\n"
            "WOULD YOU RATHER: sleep naked OR in my shirt?\n"
            "Would you rather kiss or cuddle\n"
            "this or that or the other\n"
            "nothing to choose\n"
            "would you rather | x"
        )
        self.assertEqual(
            [(e.first, e.second, e.spice) for e in entries],
            [("be tied up", "do the tying", 2), ("kiss", "cuddle", 3), ("sleep naked", "in my shirt", 1)],
        )
        self.assertEqual(unreadable, ["this or that or the other", "nothing to choose", "would you rather | x"])


class GameListViewTests(TestCase):
    def setUp(self):
        self.user = make_user("a")
        self.space = make_space(self.user)
        self.client.force_login(self.user)
        self.tod_url = reverse("items:truth_or_dare", args=[self.space.id])
        self.wyr_url = reverse("items:would_you_rather", args=[self.space.id])

    def url(self, name, *args):
        return reverse(f"items:{name}", args=[self.space.id, *args])

    def test_every_tab_renders_with_the_counts_of_every_list(self):
        make_items(self.space, "Dance")
        self.space.truths.create(text="Best kiss?")
        for url in (self.url("list"), self.tod_url, self.wyr_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual([tab["count"] for tab in response.context["tabs"]], [1, 1, 0])
        self.assertContains(self.client.get(self.wyr_url), "Fills it with our 100 questions.")
        self.assertContains(self.client.get(self.tod_url), "1 truth or dare")

    def test_generate_fills_a_game_list_and_restores_what_was_removed(self):
        self.client.post(self.url("generate", "truth-or-dare"))
        self.client.post(self.url("generate", "would-you-rather"))
        self.assertEqual((self.space.truths.count(), self.space.dares.count(), self.space.questions.count()), (105, 105, 100))
        self.assertFalse(self.space.items.exists())
        truth, dare, question = self.space.truths.first(), self.space.dares.first(), self.space.questions.first()
        self.client.post(self.url("delete_truth", truth.id))
        self.client.post(self.url("delete_dare", dare.id))
        self.client.post(self.url("delete_question", question.id))
        self.assertEqual((self.space.truths.count(), self.space.dares.count(), self.space.questions.count()), (104, 104, 99))
        response = self.client.post(self.url("generate", "truth-or-dare"), follow=True)
        self.assertContains(response, "Added 2 truths and dares to Truth or Dare.")
        response = self.client.post(self.url("generate", "would-you-rather"), follow=True)
        self.assertContains(response, "Added 1 question to Would you rather.")
        self.assertEqual(self.space.questions.filter(first=question.first).count(), 1)

    def test_clear_empties_only_that_list_of_only_this_space(self):
        from items.starter import fill_new_space

        fill_new_space(self.space)
        other = make_space(make_user("b"), name="Them")
        fill_new_space(other)
        response = self.client.post(self.url("clear", "truth-or-dare"))
        self.assertRedirects(response, self.tod_url)
        self.assertEqual((self.space.truths.count(), self.space.dares.count()), (0, 0))
        self.assertEqual((self.space.questions.count(), self.space.items.count()), (100, 134))
        self.client.post(self.url("clear", "would-you-rather"))
        self.assertFalse(self.space.questions.exists())
        self.assertEqual((other.truths.count(), other.dares.count(), other.questions.count()), (105, 105, 100))
        self.assertEqual(self.client.post(self.url("clear", "nope")).status_code, 404)
        self.client.force_login(make_user("stranger"))
        self.assertEqual(self.client.post(self.url("generate", "would-you-rather")).status_code, 404)
        self.assertFalse(self.space.questions.exists())

    def test_add_a_truth_or_a_dare_once(self):
        self.client.post(self.tod_url, {"kind": "truth", "text": "Best kiss ever?", "spice": 1})
        response = self.client.post(self.tod_url, {"kind": "truth", "text": "best kiss  EVER?", "spice": 2}, follow=True)
        self.assertContains(response, "That truth is already on the list.")
        self.client.post(self.tod_url, {"kind": "dare", "text": "Best kiss ever?", "spice": 3})
        self.assertEqual(self.space.truths.get().text, "Best kiss ever?")
        self.assertEqual(self.space.dares.get().spice, 3)
        response = self.client.post(self.tod_url, {"kind": "dare", "text": "x" * 141, "spice": 1})
        self.assertContains(response, "Keep a dare to 140 characters.")
        self.assertEqual(self.space.dares.count(), 1)

    def test_import_truths_and_dares_skips_whats_there(self):
        self.space.dares.create(text="Kiss my neck")
        response = self.client.post(
            self.url("import_truth_or_dare"),
            {"kind": "truth", "lines": "Best kiss? | Spicy\nDare | kiss my NECK\nDare | Tie me up | 9"},
            follow=True,
        )
        self.assertContains(response, "Added 1 truth and 1 dare (skipped 1 already on the list).")
        self.assertContains(response, "1 line had an intensity we didn")
        self.assertEqual(self.space.truths.get().spice, 2)
        self.assertEqual(sorted(self.space.dares.values_list("text", flat=True)), ["Kiss my neck", "Tie me up"])

    def test_add_and_import_questions(self):
        self.client.post(self.wyr_url, {"first": " kiss ", "second": "cuddle", "spice": 2})
        response = self.client.post(self.wyr_url, {"first": "Kiss", "second": "CUDDLE", "spice": 1}, follow=True)
        self.assertContains(response, "That question is already on the list.")
        response = self.client.post(
            self.url("import_questions"),
            {"lines": "Would you rather kiss or cuddle?\nbe tied up | do the tying | 3\nhmm"},
            follow=True,
        )
        self.assertContains(response, "Added 1 question (skipped 1 already on the list).")
        self.assertContains(response, "read 1 line, starting with “hmm”.")
        self.assertEqual(
            sorted(q.text for q in self.space.questions.all()),
            ["Would you rather be tied up or do the tying?", "Would you rather kiss or cuddle?"],
        )

    def test_removing_needs_the_entry_to_be_in_this_space(self):
        other = make_space(make_user("b"), name="Them")
        truth = other.truths.create(text="Theirs?")
        dare = other.dares.create(text="Theirs")
        question = other.questions.create(first="this", second="that")
        (item,) = make_items(other, "Theirs")
        for name, entry in (("delete_truth", truth), ("delete_dare", dare), ("delete_question", question), ("delete", item)):
            self.assertEqual(self.client.post(self.url(name, entry.id)).status_code, 404)
        self.assertEqual((other.truths.count(), other.dares.count(), other.questions.count(), other.items.count()), (1, 1, 1, 1))

    def test_removing_a_wish_takes_its_to_dos_and_empty_sessions(self):
        from assignments.models import GameSession

        keep, remove = make_items(self.space, "Keep", "Remove")
        shared = GameSession.objects.create(space=self.space, game_type="randomize")
        alone = GameSession.objects.create(space=self.space, game_type="randomize")
        Assignment.objects.create(space=self.space, item=keep, session=shared)
        Assignment.objects.create(space=self.space, item=remove, session=shared)
        Assignment.objects.create(space=self.space, item=remove, session=alone)
        response = self.client.post(self.url("delete", remove.id), follow=True)
        self.assertContains(response, "Removed “Remove”.")
        self.assertEqual(list(self.space.items.all()), [keep])
        self.assertEqual(list(GameSession.objects.all()), [shared])


class FillGameListsMigrationTests(TestCase):
    def test_gives_existing_spaces_the_built_ins_without_doubling_their_own_truths(self):
        import importlib

        from django.apps import apps

        from games.truths import BUILT_IN_TRUTHS

        migration = importlib.import_module("items.migrations.0007_fill_game_lists")
        space = make_space(make_user("a"))
        space.truths.create(text=BUILT_IN_TRUTHS[0][1].upper())
        space.truths.create(text="Our own question?")
        migration.fill_lists(apps, None)
        self.assertEqual(space.truths.count(), len(BUILT_IN_TRUTHS) + 1)
        self.assertEqual((space.dares.count(), space.questions.count()), (105, 100))


class FixStarterWishesMigrationTests(TestCase):
    def test_renames_in_place_including_case_only_fixes_and_never_clashes(self):
        import importlib

        from django.apps import apps

        migration = importlib.import_module("items.migrations.0005_fix_starter_wishes")
        space = make_space(make_user("a"))
        cut_off = (
            "Next time your partner receives a telemarketers’ call, he/she cannot hang up! "
            "Give your partner oral sex while they are on the phone. Hang u"
        )
        typo, case_only, truncated, clash = make_items(
            space, "Dress up", "Join the mile high club.", cut_off, "Have rough sex"
        )
        make_items(space, "Have rough sex.")
        Assignment.objects.create(space=space, item=typo, status=Assignment.COMPLETED)

        migration.fix_titles(apps, None)

        for item in (typo, case_only, truncated, clash):
            item.refresh_from_db()
        self.assertEqual(typo.title, "Dress up.")
        self.assertEqual(typo.assignments.count(), 1)
        self.assertEqual(case_only.title, "Join the Mile High Club.")
        self.assertEqual(truncated.title, "Next time your partner receives a telemarketer’s call, he/she cannot hang up!")
        self.assertIn("Hang up when the deed is done.", truncated.description)
        self.assertEqual(clash.title, "Have rough sex")


class ReviewedStarterWishesMigrationTests(TestCase):
    """0009 brings existing spaces in line with the reviewed starter wishes, keeping their own changes."""

    def setUp(self):
        import importlib

        self.migration = importlib.import_module("items.migrations.0009_reviewed_starter_wishes")
        self.space = make_space(make_user("a"))

    def wish(self, title, category, spice, details="", space=None):
        item = Item.objects.create(space=space or self.space, title=title, spice=spice, description=details)
        item.set_categories([category] if isinstance(category, str) else category)
        return item

    def migrate(self):
        from django.apps import apps

        self.migration.forwards(apps, None)

    def levels(self, item):
        return list(item.levels.values_list("text", flat=True))

    def test_untouched_wishes_get_the_review(self):
        yoga = self.wish("Do naked yoga.", "Activity", 3)
        dress = self.wish("Dress up.", "Clothing", 1)
        groped = self.wish("Be groped in public.", "Public", 2)
        Assignment.objects.create(space=self.space, item=dress, status=Assignment.COMPLETED)
        self.migrate()

        yoga.refresh_from_db()
        self.assertEqual(yoga.spice, 2)
        self.assertTrue(yoga.description.startswith("There is something hot about seeing your partner"))
        self.assertEqual(self.levels(yoga)[1], "Yoga in your underwear is fine... real fine.")
        dress.refresh_from_db()
        self.assertEqual(dress.title, "Dress up and have a classy night out.")
        self.assertEqual(dress.description, "")
        self.assertEqual(len(self.levels(dress)), 3)
        self.assertEqual(dress.assignments.count(), 1)
        self.assertEqual(groped.category_names, ["Public", "Teasing", "Voyeurism"])
        self.assertEqual(self.space.categories.filter(name="Voyeurism").count(), 1)

    def test_what_a_space_changed_stays_as_it_is(self):
        phone = self.wish("Have phone sex.", "Activity", 3, "Our own notes")
        groped = self.wish("Be groped in public.", ["Public", "Fun"], 2)
        yoga = self.wish("Do naked yoga.", "Activity", 3)
        yoga.levels.create(text="Our own first step")
        renamed = self.wish("Have stoned sex.", "Sensory", 1)
        self.wish("dress up and have a classy night out.", "Clothing", 1)
        dress = self.wish("Dress up.", "Clothing", 1)
        self.migrate()

        phone.refresh_from_db()
        self.assertEqual((phone.spice, phone.description), (3, "Our own notes"))
        self.assertEqual(self.levels(phone)[0], "Flirt, talk dirty to each other.")
        self.assertEqual(sorted(groped.category_names), ["Fun", "Public"])
        self.assertEqual(self.levels(yoga), ["Our own first step"])
        self.assertEqual(self.levels(renamed), [])
        dress.refresh_from_db()
        self.assertEqual(dress.title, "Dress up.")

    def test_removed_wishes_go_only_where_untouched_and_never_used(self):
        unused = self.wish("Listen to audio porn.", "Activity", 1)
        lived = self.wish("Have super-hot quickie sex.", "Challenge", 1)
        Assignment.objects.create(space=self.space, item=lived, status=Assignment.COMPLETED)
        other = make_space(make_user("b"), name="Them")
        edited = self.wish("Listen to audio porn.", "Activity", 2, space=other)
        with_details = self.wish("Have super-hot quickie sex.", "Challenge", 1, "Before the movie", space=other)
        self.migrate()

        self.assertFalse(Item.objects.filter(pk=unused.pk).exists())
        self.assertEqual(
            set(Item.objects.values_list("pk", flat=True)), {lived.pk, edited.pk, with_details.pk}
        )
