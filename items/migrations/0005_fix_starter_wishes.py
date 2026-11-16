"""Bring wishes imported from the original Kinky Bucket List in line with the corrected starter list.

Renames in place, so a wish keeps its assignments, memories and replies. Only exact
matches of the old titles change, in every space, and never when the space already
has a wish with the new title. Details are filled in only where they are empty.
"""

from django.db import migrations

# (old title, corrected title, details)
RENAMES = [
    ('Borrow your partner’s phone and take a dirty picture. They cannot look at it until you have left the home.', 'Borrow your partner’s phone and take a dirty picture. They cannot look at it until you have left the house.', ''),
    ('Dress up', 'Dress up.', ''),
    ('For an entire session, one of you has to tell the other person what to do to them. Communication (and dirty talk?) is key! It’s okay to be s', 'For an entire session, one of you has to tell the other person what to do to them.', 'Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.'),
    ('Give him a BJ while he’s driving or finger her (and/or use toys) while she’s driving.', 'Give him a blow job while he’s driving, or finger her (and/or use toys) while she’s driving.', ''),
    ('Go to a swinger bar.', 'Go to a swingers’ bar.', ''),
    ('Join the mile high club.', 'Join the Mile High Club.', ''),
    ('Lunchtime sex when working.', 'Lunchtime sex at work.', ''),
    ('Next time your partner receives a telemarketers’ call, he/she cannot hang up! Give your partner oral sex while they are on the phone. Hang u', 'Next time your partner receives a telemarketer’s call, he/she cannot hang up!', 'Give your partner oral sex while they are on the phone. Hang up when the deed is done.'),
    ('Record yourself being naughty in a public setting and send it to your partner OR record yourselves doing naughty things in public (change ro', 'Record yourself being naughty in a public setting and send it to your partner.', 'Or record yourselves doing naughty things in public (changing room, elevator, etc.).'),
    ('Recreate a porno video (Pick at random, or already have one in mind?).', 'Recreate a porno video (pick at random, or already have one in mind?).', ''),
    ('Roleplay (Play out a Fantasy, or explore a theme with it).', 'Roleplay (play out a fantasy, or explore a theme with it).', ''),
    ('Use your mouth to put a condom on your man.', 'Use your mouth to put a condom on him.', ''),
    ('Be a dominant mistress/master of your partner for a night', 'Be a dominant mistress/master of your partner for a night.', ''),
    ('Bound and blindfolded', 'Bound and blindfolded.', ''),
    ('Breath play - safely.', 'Breath play — safely.', ''),
    ('Chair ties', 'Chair ties.', ''),
    ('Dom/Sub switch it up!', 'Dom/sub switch it up!', ''),
    ('Handcuffs', 'Handcuffs.', ''),
    ('Light hair pulling & biting.', 'Light hair pulling and biting.', ''),
    ('Massage (everything but between the legs… make them wait, then finish them off with a glorious happy ending.', 'Massage (everything but between the legs… make them wait, then finish them off with a glorious happy ending).', ''),
    ('Sensual restraint with scarves/silky necktie', 'Sensual restraint with scarves or a silky necktie.', ''),
    ('Shibari rope harness', 'Shibari rope harness.', ''),
    ('Tell your partner, “Do whatever you want to me.” Just remember to use a safe word!', 'Tell your partner, “Do whatever you want to me.” Just remember to use a safeword!', ''),
    ('Have sex in public-sort of.', 'Have sex in public — sort of.', ''),
    ('Chair sex', 'Chair sex.', ''),
    ('Have a reeeealy deep penetrative sex.', 'Have a really deep penetrative sex session.', ''),
    ('Try “Airlock” (DP + BJ)', 'Try “Airlock” (DP + BJ).', ''),
    ('Try a finger up the butt.', 'Try a finger in the butt.', ''),
    ('Try consensual “non consensual”.', 'Try consensual “non-consensual” play.', ''),
    ('Try deep throating.', 'Try deep-throating.', ''),
    ('Do it in the amazon sex position.', 'Do it in the Amazon sex position.', ''),
    ('Explore the joys of a good ol’ fashioned missionary position.', 'Explore the joys of a good old-fashioned missionary position.', ''),
    ('Have sex in doggy style.', 'Have sex doggy style.', ''),
    ('Try 69-ing', 'Try 69-ing.', ''),
    ('Try a new position that neither of you tried.', 'Try a new position that neither of you has tried before.', ''),
    ('Try the yab-yum position.', 'Try the Yab-Yum position.', ''),
    ('Positions:Try all the Kama Sutra sex positions.', 'Try all the Kama Sutra sex positions.', ''),
    ('Use a remote-controlled sex toy with a partner. (in public?)', 'Use a remote-controlled sex toy with a partner (in public?).', ''),
    ('Give her a creampie, she decides where she wants it.', 'Give her a creampie; she decides where she wants it.', ''),
    ('Give her a cumshot, she decides where she wants it.', 'Give her a cumshot; she decides where she wants it.', ''),
    ('Have rough sex', 'Have rough sex.', ''),
    ("Look at each other's eyes when cumming. Bonus: cum at the same time.", 'Look into each other’s eyes when cumming. Bonus: cum at the same time.', ''),
    ('No kissing sesh', 'No-kissing session.', ''),
    ('Surprise each other with a new piece of lingerie or sex toys.', 'Surprise each other with a new piece of lingerie or a new sex toy.', ''),
    ('Wear sexy costumes', 'Wear sexy costumes.', ''),
]


def fix_titles(apps, schema_editor):
    Item = apps.get_model("items", "Item")
    for old, new, details in RENAMES:
        for item in Item.objects.filter(title=old):
            # Fixes that only change capitalization would otherwise find the wish itself.
            if Item.objects.filter(space_id=item.space_id, title__iexact=new).exclude(pk=item.pk).exists():
                continue
            item.title = new
            if details and not item.description:
                item.description = details
            item.save(update_fields=["title", "description"])


class Migration(migrations.Migration):
    dependencies = [("items", "0004_truth_or_dare")]

    operations = [migrations.RunPython(fix_titles, migrations.RunPython.noop)]
