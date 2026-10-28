from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from assignments.models import Assignment

from kinkylist.test_utils import make_items, make_space, make_user

from .models import Category
from .utils import parse_bulk, split_categories


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
        self.assertContains(response, "1 item had an intensity we didn")

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
