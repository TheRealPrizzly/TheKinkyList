from django import template
from django.utils.safestring import mark_safe

from art import generator

register = template.Library()


@register.simple_tag
def abstract_art(seed, palette="rose", motif="hearts", intensity=1.0):
    return mark_safe(generator.render(str(seed), palette, motif, float(intensity)))


@register.simple_tag
def item_art(item):
    names = item.category_names
    return mark_safe(generator.item_art(item.pk, names[0] if names else "", item.spice))


@register.simple_tag
def game_art(game):
    return mark_safe(generator.render(f"game-{game.slug}", game.palette, game.motif, 1.2))
