import xml.etree.ElementTree as ET

from django.test import SimpleTestCase

from art import generator


class GeneratorTests(SimpleTestCase):
    def test_same_seed_gives_same_art(self):
        generator.render.cache_clear()
        first = generator.render("item-1", "rose", "hearts")
        generator.render.cache_clear()
        self.assertEqual(first, generator.render("item-1", "rose", "hearts"))

    def test_different_seeds_differ(self):
        self.assertNotEqual(generator.render("a", "rose", "hearts"), generator.render("b", "rose", "hearts"))

    def test_every_motif_renders_valid_svg(self):
        for motif in generator.MOTIFS:
            for palette in generator.PALETTES:
                root = ET.fromstring(generator.render(f"{palette}-{motif}", palette, motif))
                self.assertTrue(root.tag.endswith("svg"))

    def test_unknown_palette_and_motif_fall_back(self):
        ET.fromstring(generator.render("x", "nope", "nope"))

    def test_item_art_is_stable_per_item_and_category_drives_palette(self):
        self.assertEqual(generator.item_art(7, "Romance", 2), generator.item_art(7, "Romance", 2))
        self.assertEqual(generator.item_art(7, "romance ", 2), generator.item_art(7, "Romance", 2))
