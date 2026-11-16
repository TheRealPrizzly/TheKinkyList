"""Give every existing space its own Truth or Dare and "Would you rather" lists.

Until now those games always drew the built-in questions and dares, so each space gets
all of them on its lists. Truths the space wrote itself stay, and a built-in truth
they already wrote (ignoring case) isn't added twice.
"""

from django.db import migrations


def fill_lists(apps, schema_editor):
    from games.dares import BUILT_IN_DARES
    from games.truths import BUILT_IN_TRUTHS
    from games.would_you_rather import BUILT_IN_QUESTIONS

    Space = apps.get_model("spaces", "Space")
    Truth = apps.get_model("items", "Truth")
    Dare = apps.get_model("items", "Dare")
    Question = apps.get_model("items", "Question")
    for space in Space.objects.all():
        own = {text.lower() for text in Truth.objects.filter(space=space).values_list("text", flat=True)}
        Truth.objects.bulk_create(
            Truth(space=space, text=text, spice=spice) for spice, text in BUILT_IN_TRUTHS if text.lower() not in own
        )
        if not Dare.objects.filter(space=space).exists():
            Dare.objects.bulk_create(Dare(space=space, text=text, spice=spice) for spice, text in BUILT_IN_DARES)
        if not Question.objects.filter(space=space).exists():
            Question.objects.bulk_create(
                Question(space=space, first=first, second=second, spice=spice)
                for spice, first, second in BUILT_IN_QUESTIONS
            )


class Migration(migrations.Migration):
    dependencies = [("items", "0006_game_lists"), ("spaces", "0001_initial")]

    operations = [migrations.RunPython(fill_lists, migrations.RunPython.noop)]
