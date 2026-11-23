"""Write details for every built-in wish, and levels for the wishes that had none.

The new details and levels are in items/starter.py. Each entry is matched to the starter list by
its position, which never changes, so a wish renamed on the Built-in lists page still gets its
text. An entry only gets what staff never changed on that page: new details where its details are
still the ones 0011 started it with, and levels where it started with none and still has none.

Every copy in a space gets the change too, wherever the space never changed that field itself, as
saving on the Built-in lists page does. A wish a space already lived comes back in the games once
it has levels, until its last level is done.
"""

from django.db import migrations

# The details the starter list had before, by title in lowercase. The other wishes had none.
OLD_DETAILS = {
    "be groped in public.":
        "Have your partner grope you in a public setting.",
    "borrow your partner’s phone and take a dirty picture. they cannot look at it until one of you has left the "
    "house.":
        "Leave your partner something to remember for when you are away.",
    "do naked yoga.":
        "There is something hot about seeing your partner in certain poses that may or may not accentuate their "
        "curves and/or muscles. Let's explore that!",
    "for an entire session, one of you has to tell the other person what to do to them.":
        "Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.",
    "give a nuru massage.":
        "What is a nuru massage?\n\n"
        "It is a form of erotic full-body massage that originated in Japan. It is characterized by the use of a "
        "water-soluble, slippery gel that allows extensive skin-to-skin contact. The giver glides their naked body "
        "over the receiver's body to create a sensual experience.",
    "give him a blow job (or finger her and/or use toys) while he (or she) is driving. stay safe and park if needed.":
        "Important: Safety first! As you can imagine, this can be very distracting and driving requires your full "
        "attention. Maybe, pick a place where there is no traffic, no pedestrian. You don't want to turn this "
        "fantasy into a real nightmare. If driving is too distracting, park somewhere but the idea is that this "
        "happens in the vehicle.",
    "go skinny dipping at night.":
        "You can pick a pool, or a hot tub, or any place with water that you can swim... but you both have to go in "
        "naked!",
    "go to a sex party.":
        "If you are not familiar with sex parties, you will need to do some homework. Preparing for a sex party "
        "involves clarifying your boundaries, checking event rules and dress codes, packing safer-sex supplies, and "
        "getting ready physically and emotionally.",
    "go to a sex store together.":
        "Look around and talk! It's a great way to discover what your partner might be into. No purchase necessary.",
    "go to a swingers’ bar.":
        "Before going, make sure both of you are on the same page. Be clear on what you're both comfortable with, "
        "and what you aren't. Going to a swinger's bar does NOT mean you have to swing.",
    "have a threesome.":
        "Adding another person to a sex session is one of the most popular fantasies. However, this remains a "
        "fantasy for most because of concerns around jealousy and other considerations that could disrupt what the "
        "couple has built. See the levels below for options that could help with reaching a middle ground.",
    "have stoned sex (aka being high).":
        "Disclaimer: Only use legal substances.",
    "join the mile high club.":
        "Disclaimer: Likely illegal, and could lead to warnings, fines, banned travel, or law enforcement "
        "involvement. With that said...\n\n"
        "Some companies provide small blankets on longer flights, how convenient. Using a sweater, or other piece "
        "of clothing can work.",
    "next time your partner receives a telemarketer’s call, he/she cannot hang up!":
        "Give your partner oral sex while they are on the phone. Hang up when the deed is done.",
    "record yourself being naughty in a public setting and send it to your partner.":
        "Or record yourselves doing naughty things in public (changing room, elevator, etc.).",
}

# The wishes that already had levels: the ones reviewed in 0009. They keep them.
HAD_LEVELS = {
    "be groped in public.",
    "borrow your partner’s phone and take a dirty picture. they cannot look at it until one of you has left the "
    "house.",
    "do naked yoga.",
    "dress up and have a classy night out.",
    "for an entire session, one of you has to tell the other person what to do to them.",
    "give a nuru massage.",
    "give him a blow job (or finger her and/or use toys) while he (or she) is driving. stay safe and park if needed.",
    "go skinny dipping at night.",
    "go to a sex party.",
    "go to a sex store together.",
    "go to a swingers’ bar.",
    "have a threesome.",
    "have mind-blowing vacation sex.",
    "have phone sex.",
    "have sex in every non-bedroom room of your house in one night.",
    "have sex over video chat.",
    "have sex while other people are close by.",
    "have stoned sex (aka being high).",
    "join the mile high club.",
    "lunchtime sex at work.",
}


class Report:
    def __init__(self):
        self.details = 0
        self.levels = 0
        self.copies = 0
        # What staff changed on the Built-in lists page, which stays as it is.
        self.kept = []


def write(apps):
    """Write the new details and levels into the built-in wishes and their copies. Returns a Report."""
    from items.starter import STARTER_LEVELS, STARTER_WISHES

    BuiltIn = apps.get_model("items", "BuiltIn")
    Item = apps.get_model("items", "Item")
    Level = apps.get_model("items", "Level")
    report = Report()
    for entry in BuiltIn.objects.filter(kind="wish", position__lt=len(STARTER_WISHES)).order_by("position"):
        title, _, _, details = STARTER_WISHES[entry.position]
        key = title.lower()
        levels = STARTER_LEVELS.get(key, [])
        changes = {}
        if entry.details != details:
            if entry.details.strip() == OLD_DETAILS.get(key, "").strip():
                changes["details"] = details
            else:
                report.kept.append(f"“{entry.text}” (details)")
        if key not in HAD_LEVELS and levels and entry.levels != levels:
            if entry.levels:
                report.kept.append(f"“{entry.text}” (levels)")
            else:
                changes["levels"] = levels
        if not changes:
            continue
        old_details = entry.details
        for field, value in changes.items():
            setattr(entry, field, value)
        entry.save()
        report.details += "details" in changes
        report.levels += "levels" in changes
        for copy in Item.objects.filter(built_in=entry):
            updated = False
            if "details" in changes and copy.description.strip() == old_details.strip():
                copy.description = changes["details"]
                copy.save(update_fields=["description"])
                updated = True
            if "levels" in changes and not Level.objects.filter(item=copy).exists():
                Level.objects.bulk_create(
                    Level(item=copy, position=position, text=text) for position, text in enumerate(changes["levels"])
                )
                updated = True
            report.copies += updated
    return report


def forwards(apps, schema_editor):
    report = write(apps)
    if report.details or report.levels:
        print(
            f"\n  Wrote details for {report.details} built-in wishes and levels for {report.levels}, "
            f"and updated {report.copies} copies of them in spaces."
        )
    if report.kept:
        print("  Kept what was changed on the Built-in lists page: " + "; ".join(report.kept))


class Migration(migrations.Migration):
    dependencies = [("items", "0011_fill_builtins")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
