"""Apply the intensity review of the first 22 starter wishes to every existing space.

The starter list in items/starter.py has the reviewed wishes for new spaces. This brings existing
spaces in line, one field at a time, and only where the space never changed that field:

- the title, intensity and details change where they still are what the starter list had;
- the categories change where the wish is still in just its starter category;
- the levels are added where the wish has no levels yet.

The two wishes taken off the starter list are deleted only where they are exactly as the starter
list had them and were never used: never given in a game, no replies, no levels. A wish that was
used keeps its history and stays.
"""

from collections import namedtuple

from django.db import migrations

Reviewed = namedtuple(
    "Reviewed", "old_title old_categories old_spice old_details title categories spice details levels"
)

REVIEWED = [
    Reviewed(
        old_title='Be groped in public.',
        old_categories=['Public'],
        old_spice=2,
        old_details='',
        title='Be groped in public.',
        categories=['Public', 'Teasing', 'Voyeurism'],
        spice=2,
        details='Have your partner grope you in a public setting.',
        levels=[
            'Sneaky and no one needs to notice.',
            'Have someone (or a group) watch.',
            'Groped by someone other than your partner (if you are both into that).',
        ],
    ),
    Reviewed(
        old_title='Borrow your partner’s phone and take a dirty picture. They cannot look at it until you have left the house.',
        old_categories=['Teasing'],
        old_spice=3,
        old_details='',
        title='Borrow your partner’s phone and take a dirty picture. They cannot look at it until one of you has left the house.',
        categories=['Teasing'],
        spice=2,
        details='Leave your partner something to remember for when you are away.',
        levels=[
            'Clothes stay on but show your best "features".',
            "Underwear is showing... maybe a glimpse of skin that doesn't usually get much sun?",
            'You are now showing some skin, and private parts. Be provocative, have fun with this one!',
        ],
    ),
    Reviewed(
        old_title='Do naked yoga.',
        old_categories=['Activity'],
        old_spice=3,
        old_details='',
        title='Do naked yoga.',
        categories=['Activity'],
        spice=2,
        details="There is something hot about seeing your partner in certain poses that may or may not accentuate their curves and/or muscles. Let's explore that!",
        levels=[
            "Keep your yoga-wear, it's likely that curves are already showing.",
            'Yoga in your underwear is fine... real fine.',
            'Nothing but skin, and poses, and maybe you use yoga poses to try a new position or two?',
        ],
    ),
    Reviewed(
        old_title='Dress up.',
        old_categories=['Clothing'],
        old_spice=1,
        old_details='',
        title='Dress up and have a classy night out.',
        categories=['Clothing'],
        spice=1,
        details='',
        levels=[
            'Enjoy your night out, but take a good look at your partner, stunning!',
            'Compliment your partner, flirt, tease, be "touchy".',
            'Dressing up is how it started, undressing each other is how it ends. Bonus if this happened before you made it back home.',
        ],
    ),
    Reviewed(
        old_title='For an entire session, one of you has to tell the other person what to do to them.',
        old_categories=['Challenge'],
        old_spice=2,
        old_details='Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.',
        title='For an entire session, one of you has to tell the other person what to do to them.',
        categories=['Challenge'],
        spice=2,
        details='Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.',
        levels=[
            'You lead the session. You decide what your partner does to you, the positions, and how you finish.',
            'You need to have requested your partner to perform some form of dirty talk, some form of foreplay, and a mix of at least 2 sex positions.',
            'With proper guidance, your partner makes you orgasm multiple times.',
        ],
    ),
    Reviewed(
        old_title='Give a nuru massage.',
        old_categories=['Challenge'],
        old_spice=1,
        old_details='',
        title='Give a nuru massage.',
        categories=['Challenge'],
        spice=1,
        details="What is a nuru massage?\n\nIt is a form of erotic full-body massage that originated in Japan. It is characterized by the use of a water-soluble, slippery gel that allows extensive skin-to-skin contact. The giver glides their naked body over the receiver's body to create a sensual experience.",
        levels=[
            'Both of you are naked, simply be generous with the massage oil/gel and use your body (and body parts) to rub your partner.',
            'Massages (at least the Nuru kind) have to have a happy ending.',
            'Either one or both of you finish, BUT no penetration allowed. Be creative and good use of your body (parts).',
        ],
    ),
    Reviewed(
        old_title='Give him a blow job while he’s driving, or finger her (and/or use toys) while she’s driving.',
        old_categories=['Challenge'],
        old_spice=1,
        old_details='',
        title='Give him a blow job (or finger her and/or use toys) while he (or she) is driving. Stay safe and park if needed.',
        categories=['Challenge'],
        spice=2,
        details="Important: Safety first! As you can imagine, this can be very distracting and driving requires your full attention. Maybe, pick a place where there is no traffic, no pedestrian. You don't want to turn this fantasy into a real nightmare. If driving is too distracting, park somewhere but the idea is that this happens in the vehicle.",
        levels=[
            'Do it, if only for a brief moment just to check it off the kinky (bucket) list.',
            'The person in the driver seat needs to finish.',
            'Once the first driver finishes, you swap seats and return the favor.',
        ],
    ),
    Reviewed(
        old_title='Go skinny dipping at night.',
        old_categories=['Activity'],
        old_spice=1,
        old_details='',
        title='Go skinny dipping at night.',
        categories=['Activity'],
        spice=1,
        details='You can pick a pool, or a hot tub, or any place with water that you can swim... but you both have to go in naked!',
        levels=[
            "What's the point if you aren't sharing at least a kiss.",
            'Maybe that kiss leads to some foreplay.',
            'Both of you manage to finish while still in the water.',
        ],
    ),
    Reviewed(
        old_title='Go to a sex party.',
        old_categories=['Activity'],
        old_spice=3,
        old_details='',
        title='Go to a sex party.',
        categories=['Activity'],
        spice=3,
        details='If you are not familiar with sex parties, you will need to do some homework. Preparing for a sex party involves clarifying your boundaries, checking event rules and dress codes, packing safer-sex supplies, and getting ready physically and emotionally.',
        levels=[
            'You showed up and that already took a lot of courage. Congrats, you made it!',
            "Maybe you're not interested in sharing, but your curious side leads you to watch others do their thing.",
            'Explore, maybe including someone else in your activities, or both going your separate ways to discover something else, if only for a moment.',
        ],
    ),
    Reviewed(
        old_title='Go to a sex store together.',
        old_categories=['Activity'],
        old_spice=2,
        old_details='',
        title='Go to a sex store together.',
        categories=['Activity'],
        spice=2,
        details="Look around and talk! It's a great way to discover what your partner might be into. No purchase necessary.",
        levels=[
            'You made it, congrats! Look around and both of you should share your observations. Your likes and dislikes.',
            "Buy something! Maybe it's lingerie, or edible massage oil, or a toy, or whatever else that seemed interesting to both of you.",
            "Whatever you bought gets used that same day. Don't wait, have fun!",
        ],
    ),
    Reviewed(
        old_title='Go to a swingers’ bar.',
        old_categories=['Activity'],
        old_spice=3,
        old_details='',
        title='Go to a swingers’ bar.',
        categories=['Activity'],
        spice=3,
        details="Before going, make sure both of you are on the same page. Be clear on what you're both comfortable with, and what you aren't. Going to a swinger's bar does NOT mean you have to swing.",
        levels=[
            'You made it! Look around and share with your partner the things that make you uncomfortable, and the things that make you curious.',
            'Engage with others, and find out what they are into. Who knows, maybe you\'ll find "interesting" people.',
            'Embrace your options. Take the opportunity to invite others into your partnership or be invited to meet other people in an intimate way.',
        ],
    ),
    Reviewed(
        old_title='Have a threesome.',
        old_categories=['Activity'],
        old_spice=3,
        old_details='',
        title='Have a threesome.',
        categories=['Activity'],
        spice=3,
        details='Adding another person to a sex session is one of the most popular fantasies. However, this remains a fantasy for most because of concerns around jealousy and other considerations that could disrupt what the couple has built. See the levels below for options that could help with reaching a middle ground.',
        levels=[
            "Invite someone into your partnership with limits. Kiss & touch your partner while the 3rd person is watching, but maybe that's all, for now.",
            'You and your partner have sex. The 3rd person can only watch and tell the couple what to do to each other, but remains an observer.',
            'Include the 3rd person, they also get to have fun. Bonus: all 3 were able to finish.',
        ],
    ),
    Reviewed(
        old_title='Have mind-blowing vacation sex.',
        old_categories=['Activity'],
        old_spice=1,
        old_details='',
        title='Have mind-blowing vacation sex.',
        categories=['Activity'],
        spice=1,
        details='',
        levels=[
            'You have sex while you are on vacation, home is fine.',
            'You have sex during a vacation somewhere else. Frankly, anywhere else but home.',
            'You have sex somewhere far away. Maybe you had to take a plane to get there. Maybe at a resort, a cruise. Bonus: in a different country.',
        ],
    ),
    Reviewed(
        old_title='Have phone sex.',
        old_categories=['Activity'],
        old_spice=1,
        old_details='',
        title='Have phone sex.',
        categories=['Activity'],
        spice=2,
        details='',
        levels=[
            'Flirt, talk dirty to each other.',
            'Do level 1 but add masturbation.',
            'One of you was able to finish (Bonus: both finished)',
        ],
    ),
    Reviewed(
        old_title='Have sex in every non-bedroom room of your house in one night.',
        old_categories=['Challenge'],
        old_spice=1,
        old_details='',
        title='Have sex in every non-bedroom room of your house in one night.',
        categories=['Challenge'],
        spice=1,
        details='',
        levels=[
            'Any kind of touching is fine, as long as you have done so in every room.',
            'Every room means trying a different position.',
            'Each room requires an orgasm before moving on to the next. Godspeed!',
        ],
    ),
    Reviewed(
        old_title='Have sex over video chat.',
        old_categories=['Activity'],
        old_spice=1,
        old_details='',
        title='Have sex over video chat.',
        categories=['Activity'],
        spice=2,
        details='',
        levels=[
            "Flirt, talk dirty and have fun. No need to show what's going on down there.",
            'Undress each other (by asking the other which piece of clothing to remove).',
            'This video chat has naturally progressed to one (or both) of you to masturbate and finish. Bonus if both were able to finish.',
        ],
    ),
    Reviewed(
        old_title='Have sex while other people are close by.',
        old_categories=['Challenge'],
        old_spice=2,
        old_details='',
        title='Have sex while other people are close by.',
        categories=['Challenge'],
        spice=2,
        details='',
        levels=[
            'Some touching, maybe some foreplay if you dare!',
            'You have sex where at least one of you finished.',
            'Level 2 but by "other people", we really mean "a lot of people".',
        ],
    ),
    Reviewed(
        old_title='Have stoned sex (aka being high).',
        old_categories=['Sensory'],
        old_spice=1,
        old_details='',
        title='Have stoned sex (aka being high).',
        categories=['Sensory'],
        spice=1,
        details='Disclaimer: Only use legal substances.',
        levels=[
            'Drunk sex is fine at this level.',
            'Have sex under a very light influence of substances.',
            'Have sex under a stronger influence of substances (responsibly, of course).',
        ],
    ),
    Reviewed(
        old_title='Join the Mile High Club.',
        old_categories=['Challenge'],
        old_spice=2,
        old_details='',
        title='Join the Mile High Club.',
        categories=['Challenge'],
        spice=2,
        details='Disclaimer: Likely illegal, and could lead to warnings, fines, banned travel, or law enforcement involvement. With that said...\n\nSome companies provide small blankets on longer flights, how convenient. Using a sweater, or other piece of clothing can work.',
        levels=[
            "Use your hands to pleasure your partner while they're at their seat. Bonus: Orgasm",
            'Figure out a way to perform oral sex discreetly. Bonus: Orgasm',
            'Figure out a way to perform penetrative sex. Bonus: Orgasm',
        ],
    ),
    Reviewed(
        old_title='Lunchtime sex at work.',
        old_categories=['Activity'],
        old_spice=1,
        old_details='',
        title='Lunchtime sex at work.',
        categories=['Activity'],
        spice=3,
        details='',
        levels=[
            'Maybe some kissing, maybe some inappropriate touching.',
            "Any kind of sex, even if it's just to check it off the kinky (bucket) list.",
            'One (or both) of you were able to finish.',
        ],
    ),
]

# (title, categories, intensity, details) as the starter list had them
REMOVED = [
    ('Have super-hot quickie sex.', ['Challenge'], 1, ''),
    ('Listen to audio porn.', ['Activity'], 1, ''),
]


def same_names(categories, names):
    return sorted(category.name.lower() for category in categories) == sorted(name.lower() for name in names)


def resolve_categories(Category, space_id, names):
    """The space's categories for these names, created as needed and matched ignoring case."""
    categories = []
    for name in names:
        category = Category.objects.filter(space_id=space_id, name__iexact=name).first()
        categories.append(category or Category.objects.create(space_id=space_id, name=name))
    return categories


def apply_review(apps, schema_editor):
    Item = apps.get_model("items", "Item")
    Category = apps.get_model("items", "Category")
    Level = apps.get_model("items", "Level")
    for wish in REVIEWED:
        for item in Item.objects.filter(title=wish.old_title).prefetch_related("categories"):
            changed = []
            if (
                wish.title != item.title
                and not Item.objects.filter(space_id=item.space_id, title__iexact=wish.title).exclude(pk=item.pk).exists()
            ):
                item.title = wish.title
                changed.append("title")
            if item.spice == wish.old_spice and wish.spice != item.spice:
                item.spice = wish.spice
                changed.append("spice")
            if item.description.strip() == wish.old_details.strip() and wish.details != item.description:
                item.description = wish.details
                changed.append("description")
            if changed:
                item.save(update_fields=changed)
            if same_names(item.categories.all(), wish.old_categories) and not same_names(
                item.categories.all(), wish.categories
            ):
                item.categories.set(resolve_categories(Category, item.space_id, wish.categories))
            if wish.levels and not Level.objects.filter(item=item).exists():
                Level.objects.bulk_create(
                    Level(item=item, position=position, text=text) for position, text in enumerate(wish.levels)
                )


def remove_unused(apps, schema_editor):
    Item = apps.get_model("items", "Item")
    Level = apps.get_model("items", "Level")
    Assignment = apps.get_model("assignments", "Assignment")
    Reply = apps.get_model("assignments", "Reply")
    for title, categories, spice, details in REMOVED:
        for item in Item.objects.filter(title=title, spice=spice).prefetch_related("categories"):
            untouched = item.description.strip() == details.strip() and same_names(item.categories.all(), categories)
            used = (
                Assignment.objects.filter(item=item).exists()
                or Reply.objects.filter(item=item).exists()
                or Level.objects.filter(item=item).exists()
            )
            if untouched and not used:
                item.delete()


def forwards(apps, schema_editor):
    apply_review(apps, schema_editor)
    remove_unused(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [("assignments", "0004_would_you_rather"), ("items", "0008_levels")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
