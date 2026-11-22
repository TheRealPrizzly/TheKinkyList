"""The built-in lists: kept in the database, copied into spaces, and edited for everyone by staff."""

import importlib

from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment
from kinkylist.test_utils import make_space, make_user

from . import builtins
from .lists import KINKY_LIST, TRUTH_OR_DARE
from .models import BuiltIn, Item, Question, Truth

HTMX = {"HTTP_HX_REQUEST": "true"}


def wish(text):
    return BuiltIn.objects.get(kind=BuiltIn.WISH, text=text)


class SeedTests(TestCase):
    def test_the_lists_start_from_the_code_with_the_review_marked(self):
        counts = {kind: BuiltIn.objects.filter(kind=kind).count() for kind, _ in BuiltIn.KIND_CHOICES}
        self.assertEqual(counts, {"wish": 134, "truth": 105, "dare": 105, "question": 100})
        self.assertEqual(BuiltIn.objects.filter(reviewed_at__isnull=False).count(), 20)
        groped = wish("Be groped in public.")
        self.assertEqual(groped.categories, ["Public", "Teasing", "Voyeurism"])
        self.assertEqual(len(groped.levels), 3)
        self.assertEqual(list(builtins.entries(BuiltIn.WISH))[0], groped)

    def test_existing_copies_are_linked_ignoring_case(self):
        space = make_space(make_user("a"))
        item = Item.objects.create(space=space, title="BE GROPED IN PUBLIC.")
        own = Item.objects.create(space=space, title="Our own wish")
        question = Question.objects.create(space=space, first="Kiss", second="Cuddle")
        entry = BuiltIn.objects.filter(kind=BuiltIn.QUESTION).first()
        other = Question.objects.create(space=space, first=entry.text.upper(), second=entry.second)
        importlib.import_module("items.migrations.0011_fill_builtins").link_copies(apps, None)
        for row in (item, own, question, other):
            row.refresh_from_db()
        self.assertEqual(item.built_in, wish("Be groped in public."))
        self.assertIsNone(own.built_in)
        self.assertIsNone(question.built_in)
        self.assertEqual(other.built_in, entry)


class CopyTests(TestCase):
    def test_new_spaces_get_linked_copies_of_everything(self):
        space = make_space(make_user("a"))
        builtins.fill_new_space(space)
        self.assertEqual(space.items.filter(built_in__isnull=False).count(), 134)
        self.assertEqual(space.truths.filter(built_in__isnull=False).count(), 105)
        self.assertEqual(space.questions.filter(built_in__isnull=False).count(), 100)
        groped = space.items.get(title="Be groped in public.")
        self.assertEqual(groped.category_names, ["Public", "Teasing", "Voyeurism"])
        self.assertEqual(groped.levels.count(), 3)

    def test_a_renamed_copy_still_counts_and_a_deleted_one_comes_back(self):
        space = make_space(make_user("a"))
        builtins.fill_new_space(space)
        space.items.filter(title="Do naked yoga.").update(title="Yoga, our way")
        space.items.filter(title="Go to a sex party.").delete()
        self.assertEqual(KINKY_LIST.missing(space), 1)
        self.assertEqual(KINKY_LIST.generate(space), 1)
        self.assertTrue(space.items.filter(title="Go to a sex party.", built_in__isnull=False).exists())
        self.assertEqual((KINKY_LIST.missing(space), TRUTH_OR_DARE.missing(space)), (0, 0))


class PageAccessTests(TestCase):
    def test_only_staff_can_open_it(self):
        url = reverse("builtins:page", args=["wishes"])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(make_user("member"))
        self.assertEqual(self.client.get(url).status_code, 404)
        entry = wish("Do naked yoga.")
        self.assertEqual(self.client.post(reverse("builtins:spice", args=[entry.id]), {"spice": 1}).status_code, 404)
        entry.refresh_from_db()
        self.assertEqual(entry.spice, 2)


class EditTests(TestCase):
    def setUp(self):
        self.staff = make_user("staff")
        self.staff.is_staff = True
        self.staff.save()
        self.client.force_login(self.staff)
        self.untouched = make_space(make_user("a"), name="Untouched")
        self.changed = make_space(make_user("b"), name="Changed")
        builtins.fill_new_space(self.untouched)
        builtins.fill_new_space(self.changed)

    def post(self, name, entry, data=None, **extra):
        return self.client.post(reverse(f"builtins:{name}", args=[entry.id]), data or {}, **HTMX, **extra)

    def wish_form(self, entry, **changes):
        data = {
            "text": entry.text,
            "details": entry.details,
            "categories": ", ".join(entry.categories),
            "levels": "\n".join(entry.levels),
            "spice": entry.spice,
        }
        data.update(changes)
        return data

    def test_the_page_lists_and_filters_entries(self):
        url = reverse("builtins:page", args=["wishes"])
        response = self.client.get(url)
        self.assertContains(response, "20 of 134 reviewed")
        self.assertContains(response, "Do naked yoga.")
        self.assertContains(response, "Public, Teasing, Voyeurism · 3 levels")
        response = self.client.get(url, {"show": "todo", "q": "SKINNY"})
        self.assertNotContains(response, "Go skinny dipping at night.")
        response = self.client.get(url, {"q": "voyeurism"})
        self.assertContains(response, "Be groped in public.")
        self.assertContains(response, "showing 1")
        self.assertContains(self.client.get(reverse("builtins:page", args=["questions"])), "Would you rather")
        self.assertEqual(self.client.get(reverse("builtins:page", args=["nope"])).status_code, 404)

    def test_saving_a_wish_updates_every_field_a_space_never_changed(self):
        entry = wish("Do naked yoga.")
        mine = self.changed.items.get(built_in=entry)
        mine.title = "Naked yoga, our way"
        mine.spice = 3
        mine.save()
        response = self.post(
            "edit",
            entry,
            self.wish_form(
                entry,
                text="Do naked yoga together.",
                details="Line one\r\n\r\nLine two",
                categories="Activity, Fitness",
                levels="Warm up\nThe full flow",
                spice=1,
            ),
        )
        self.assertContains(response, "Saved. Updated in 2 spaces. 1 space had changed it and kept its own version.")
        entry.refresh_from_db()
        self.assertEqual((entry.text, entry.spice, entry.details), ("Do naked yoga together.", 1, "Line one\n\nLine two"))
        self.assertIsNotNone(entry.reviewed_at)

        theirs = self.untouched.items.get(built_in=entry)
        self.assertEqual((theirs.title, theirs.spice, theirs.description), ("Do naked yoga together.", 1, "Line one\n\nLine two"))
        self.assertEqual(theirs.category_names, ["Activity", "Fitness"])
        self.assertEqual(list(theirs.levels.values_list("text", flat=True)), ["Warm up", "The full flow"])
        mine.refresh_from_db()
        self.assertEqual((mine.title, mine.spice, mine.description), ("Naked yoga, our way", 3, "Line one\n\nLine two"))
        self.assertEqual(mine.levels.count(), 2)

        newcomer = make_space(make_user("c"), name="New")
        builtins.fill_new_space(newcomer)
        self.assertEqual(newcomer.items.get(built_in=entry).title, "Do naked yoga together.")

    def test_level_progress_survives_a_change_to_another_level(self):
        entry = wish("Be groped in public.")
        copy = self.untouched.items.get(built_in=entry)
        first = copy.levels.first()
        first.done_at = timezone.now()
        first.save()
        levels = entry.levels[:2] + ["A brand new last level"]
        self.post("edit", entry, self.wish_form(entry, levels="\n".join(levels)))
        texts = list(copy.levels.values_list("text", "done_at"))
        self.assertEqual([text for text, _ in texts], levels)
        self.assertIsNotNone(texts[0][1])

    def test_a_rename_never_duplicates_a_wish_a_space_already_has(self):
        entry = wish("Do naked yoga.")
        self.changed.items.create(title="Naked yoga at dawn")
        self.post("edit", entry, self.wish_form(entry, text="Naked yoga at dawn", spice=3))
        self.assertEqual(self.untouched.items.get(built_in=entry).title, "Naked yoga at dawn")
        copy = self.changed.items.get(built_in=entry)
        self.assertEqual((copy.title, copy.spice), ("Do naked yoga.", 3))

    def test_a_bad_form_saves_nothing(self):
        entry = wish("Make a sex tape.")
        response = self.post("edit", entry, self.wish_form(entry, levels="\n".join("x" * 140 + str(n) for n in range(3))))
        self.assertContains(response, "Keep each level to 140 characters. Level 1 has 141.")
        self.assertContains(response, "is-editing")
        entry.refresh_from_db()
        self.assertEqual(entry.levels, [])
        self.assertIsNone(entry.reviewed_at)

    def test_the_wish_editor_offers_every_category_and_a_new_one(self):
        entry = wish("Be groped in public.")
        response = self.client.get(reverse("builtins:edit", args=[entry.id]), **HTMX)
        self.assertContains(response, 'name="new_category"')
        # Without its script, the hidden field still holds the wish's categories, so saving keeps them.
        self.assertContains(response, 'name="categories" value="Public, Teasing, Voyeurism"')
        self.assertContains(response, "chosen: [&quot;Public&quot;, &quot;Teasing&quot;, &quot;Voyeurism&quot;]")
        self.assertContains(response, "every: [&quot;Activity&quot;, &quot;Amateur&quot;, &quot;BDSM&quot;")

    def test_saving_can_create_categories_and_keeps_existing_spellings(self):
        entry = wish("Make a sex tape.")
        form = self.wish_form(entry, categories="amateur, toys", new_category="  Home   video ")
        self.assertContains(self.post("edit", entry, form), "Amateur, Toys, Home video")
        entry.refresh_from_db()
        self.assertEqual(entry.categories, ["Amateur", "Toys", "Home video"])
        copy = self.untouched.items.get(built_in=entry)
        self.assertEqual(copy.category_names, ["Amateur", "Home video", "Toys"])
        other = self.client.get(reverse("builtins:edit", args=[wish("Do naked yoga.").id]), **HTMX)
        self.assertContains(other, "&quot;Home video&quot;")

    def test_a_bad_form_keeps_a_new_category_chosen(self):
        entry = wish("Make a sex tape.")
        response = self.post("edit", entry, self.wish_form(entry, new_category="Outdoors", levels="x" * 141))
        self.assertContains(response, "chosen: [&quot;Amateur&quot;, &quot;Outdoors&quot;]")
        entry.refresh_from_db()
        self.assertEqual(entry.categories, ["Amateur"])

    def test_without_htmx_saving_goes_back_to_the_page(self):
        entry = wish("Do naked yoga.")
        url = reverse("builtins:edit", args=[entry.id])
        self.assertContains(self.client.get(url), "Edit a built-in wish")
        response = self.client.post(url, self.wish_form(entry, spice=1), follow=True)
        self.assertRedirects(response, reverse("builtins:page", args=["wishes"]) + f"#entry-{entry.id}")
        self.assertContains(response, "Saved. Updated in 2 spaces.")

    def test_tapping_an_intensity_sets_it_and_marks_it_reviewed(self):
        entry = wish("Go to a sex party.")
        response = self.post("spice", entry, {"spice": 2})
        self.assertContains(response, "Saved. Updated in 2 spaces.")
        self.assertContains(response, "✓ Reviewed")
        entry.refresh_from_db()
        self.assertEqual(entry.spice, 2)
        self.assertEqual(self.untouched.items.get(built_in=entry).spice, 2)
        self.assertContains(self.post("spice", entry, {"spice": 2}), "Saved.")
        self.assertContains(self.post("spice", entry, {"spice": 9}), "Go to a sex party.")
        entry.refresh_from_db()
        self.assertEqual(entry.spice, 2)

    def test_marking_as_reviewed_toggles(self):
        entry = wish("Make a sex tape.")
        self.assertContains(self.post("reviewed", entry), "Marked as reviewed.")
        entry.refresh_from_db()
        self.assertIsNotNone(entry.reviewed_at)
        self.assertContains(self.post("reviewed", entry), "Marked as not reviewed.")
        entry.refresh_from_db()
        self.assertIsNone(entry.reviewed_at)

    def test_truths_and_questions_update_their_copies(self):
        truth = BuiltIn.objects.filter(kind=BuiltIn.TRUTH).first()
        self.changed.truths.create(text="What do you love about mornings?")
        self.post("edit", truth, {"text": "What do you love about mornings?", "spice": 3})
        self.assertEqual(self.untouched.truths.get(built_in=truth).text, "What do you love about mornings?")
        self.assertEqual(self.changed.truths.get(built_in=truth).spice, 3)
        question = BuiltIn.objects.filter(kind=BuiltIn.QUESTION).first()
        self.post("edit", question, {"text": "kiss  slowly", "second": "kiss fast", "spice": question.spice})
        copy = self.untouched.questions.get(built_in=question)
        self.assertEqual((copy.first, copy.second), ("kiss slowly", "kiss fast"))

    def test_removing_keeps_copies_that_were_changed_or_used(self):
        entry = wish("Go to a sex party.")
        lived = self.changed.items.get(built_in=entry)
        Assignment.objects.create(space=self.changed, item=lived, status=Assignment.COMPLETED)
        third = make_space(make_user("c"), name="Third")
        builtins.fill_new_space(third)
        third.items.filter(built_in=entry).update(description="Our notes")
        response = self.post("remove", entry)
        self.assertContains(response, "Removed “Go to a sex party.” Deleted from 1 space. 2 spaces keep their copy")
        self.assertFalse(BuiltIn.objects.filter(pk=entry.pk).exists())
        self.assertFalse(self.untouched.items.filter(title="Go to a sex party.").exists())
        lived.refresh_from_db()
        self.assertIsNone(lived.built_in)
        self.assertTrue(third.items.filter(title="Go to a sex party.").exists())
        self.assertEqual(KINKY_LIST.ours(), 133)
        self.assertEqual(KINKY_LIST.missing(self.untouched), 0)

    def test_removing_a_truth_takes_it_off_every_space(self):
        truth = BuiltIn.objects.filter(kind=BuiltIn.TRUTH).first()
        self.post("remove", truth)
        self.assertFalse(Truth.objects.filter(text=truth.text).exists())
        self.assertEqual(TRUTH_OR_DARE.ours(), 209)

    def test_staff_find_the_page_from_their_lists_and_profile(self):
        space = make_space(self.staff, name="Ours")
        self.assertContains(self.client.get(reverse("items:list", args=[space.id])), "Edit ours")
        self.assertContains(self.client.get(reverse("profile")), "Built-in lists")
        member = make_user("member")
        self.client.force_login(member)
        theirs = make_space(member, name="Theirs")
        self.assertNotContains(self.client.get(reverse("items:list", args=[theirs.id])), "Edit ours")
        self.assertNotContains(self.client.get(reverse("profile")), "Built-in lists")
