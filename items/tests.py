from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from assignments.models import Assignment

from kinkylist.test_utils import make_items, make_space, make_user

from .utils import parse_bulk


class ParseBulkTests(SimpleTestCase):
    def test_categories_bullets_numbers_and_duplicates(self):
        text = """
        Romance: Candlelit bath
        - Stargazing picnic
        2. Adventure: Skinny dip
        candlelit bath
        Note: time: 9pm dinner
        """
        self.assertEqual(
            parse_bulk(text),
            [
                ("Romance", "Candlelit bath"),
                ("", "Stargazing picnic"),
                ("Adventure", "Skinny dip"),
                ("Note", "time: 9pm dinner"),
            ],
        )

    def test_long_prefix_is_not_a_category(self):
        line = "This is a very long sentence that happens to have a colon: really"
        self.assertEqual(parse_bulk(line), [("", line)])


class ItemViewTests(TestCase):
    def setUp(self):
        self.user = make_user("a")
        self.space = make_space(self.user)
        self.client.force_login(self.user)

    def test_bulk_add_skips_existing_titles(self):
        make_items(self.space, "Candlelit bath")
        url = reverse("items:bulk", args=[self.space.id])
        self.client.post(url, {"lines": "Romance: candlelit bath\nRomance: Dance in the rain"})
        self.assertEqual(sorted(self.space.items.values_list("title", flat=True)), ["Candlelit bath", "Dance in the rain"])

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
        response = self.client.post(reverse("items:clear", args=[self.space.id]))
        self.assertRedirects(response, reverse("items:list", args=[self.space.id]))
        self.assertFalse(self.space.items.exists())
        self.assertFalse(Assignment.objects.filter(space=self.space).exists())
        self.assertEqual(other.items.count(), 1)

    def test_clear_requires_post_and_membership(self):
        url = reverse("items:clear", args=[self.space.id])
        make_items(self.space, "Keep me")
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.force_login(make_user("stranger"))
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertEqual(self.space.items.count(), 1)
