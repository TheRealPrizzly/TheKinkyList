from django.test import SimpleTestCase, TestCase
from django.urls import reverse

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
