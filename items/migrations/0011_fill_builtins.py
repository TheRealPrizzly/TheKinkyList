"""Move our built-in lists into the database, and link every space's copies to them.

The lists come from items/starter.py and games/ as they are now, in the same order. The wishes
reviewed in 0009 start out marked as reviewed. A space's wish, truth, dare or question counts as a
copy when its text matches an entry, ignoring case, so later edits can update it.
"""

import importlib

from django.db import migrations
from django.utils import timezone


def fill(apps, schema_editor):
    from games.dares import BUILT_IN_DARES
    from games.truths import BUILT_IN_TRUTHS
    from games.would_you_rather import BUILT_IN_QUESTIONS
    from items.starter import STARTER_LEVELS, STARTER_WISHES, category_names

    BuiltIn = apps.get_model("items", "BuiltIn")
    review = importlib.import_module("items.migrations.0009_reviewed_starter_wishes")
    reviewed = {wish.title.lower() for wish in review.REVIEWED}
    now = timezone.now()
    entries = [
        BuiltIn(
            kind="wish",
            position=position,
            text=title,
            details=details,
            categories=category_names(category),
            levels=STARTER_LEVELS.get(title.lower(), []),
            spice=spice,
            reviewed_at=now if title.lower() in reviewed else None,
        )
        for position, (title, category, spice, details) in enumerate(STARTER_WISHES)
    ]
    entries += [
        BuiltIn(kind="truth", position=position, text=text, spice=spice)
        for position, (spice, text) in enumerate(BUILT_IN_TRUTHS)
    ]
    entries += [
        BuiltIn(kind="dare", position=position, text=text, spice=spice)
        for position, (spice, text) in enumerate(BUILT_IN_DARES)
    ]
    entries += [
        BuiltIn(kind="question", position=position, text=first, second=second, spice=spice)
        for position, (spice, first, second) in enumerate(BUILT_IN_QUESTIONS)
    ]
    BuiltIn.objects.bulk_create(entries)
    link_copies(apps, schema_editor)


def link_copies(apps, schema_editor):
    BuiltIn = apps.get_model("items", "BuiltIn")
    Item = apps.get_model("items", "Item")
    Truth = apps.get_model("items", "Truth")
    Dare = apps.get_model("items", "Dare")
    Question = apps.get_model("items", "Question")
    for entry in BuiltIn.objects.all():
        if entry.kind == "wish":
            copies = Item.objects.filter(title__iexact=entry.text)
        elif entry.kind == "truth":
            copies = Truth.objects.filter(text__iexact=entry.text)
        elif entry.kind == "dare":
            copies = Dare.objects.filter(text__iexact=entry.text)
        else:
            copies = Question.objects.filter(first__iexact=entry.text, second__iexact=entry.second)
        copies.filter(built_in__isnull=True).update(built_in=entry)


def empty(apps, schema_editor):
    apps.get_model("items", "BuiltIn").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("items", "0010_builtin")]

    operations = [migrations.RunPython(fill, empty)]
