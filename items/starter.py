"""What every new space's lists start with, and what "Generate a list" adds back.

The Kinky List starts with The Kinky Bucket List below, as (title, category, intensity, details).
Truth or Dare and "Would you rather" start with the built-ins in games/truths.py, games/dares.py
and games/would_you_rather.py.

Titles are capped at 140 characters (Item.title), so the few longer wishes keep
their first sentence as the title and the rest as details.
"""

SWEET, SPICY, SIZZLING = 1, 2, 3

STARTER_WISHES = [
    ("Be groped in public.", "Public", SPICY, ""),
    (
        "Borrow your partner’s phone and take a dirty picture. They cannot look at it until you have left the house.",
        "Teasing",
        SIZZLING,
        "",
    ),
    ("Do naked yoga.", "Activity", SIZZLING, ""),
    ("Dress up.", "Clothing", SWEET, ""),
    (
        "For an entire session, one of you has to tell the other person what to do to them.",
        "Challenge",
        SPICY,
        "Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.",
    ),
    ("Give a nuru massage.", "Challenge", SWEET, ""),
    (
        "Give him a blow job while he’s driving, or finger her (and/or use toys) while she’s driving.",
        "Challenge",
        SWEET,
        "",
    ),
    ("Go skinny dipping at night.", "Activity", SWEET, ""),
    ("Go to a sex party.", "Activity", SIZZLING, ""),
    ("Go to a sex store together.", "Activity", SPICY, ""),
    ("Go to a swingers’ bar.", "Activity", SIZZLING, ""),
    ("Have a threesome.", "Activity", SIZZLING, ""),
    ("Have mind-blowing vacation sex.", "Activity", SWEET, ""),
    ("Have phone sex.", "Activity", SWEET, ""),
    ("Have sex in every non-bedroom room of your house in one night.", "Challenge", SWEET, ""),
    ("Have sex over video chat.", "Activity", SWEET, ""),
    ("Have sex while other people are close by.", "Challenge", SPICY, ""),
    ("Have stoned sex (aka being high).", "Sensory", SWEET, ""),
    ("Have super-hot quickie sex.", "Challenge", SWEET, ""),
    ("Join the Mile High Club.", "Challenge", SPICY, ""),
    ("Listen to audio porn.", "Activity", SWEET, ""),
    ("Lunchtime sex at work.", "Activity", SWEET, ""),
    ("Make a sex tape.", "Amateur", SIZZLING, ""),
    (
        "Next time your partner receives a telemarketer’s call, he/she cannot hang up!",
        "Challenge",
        SWEET,
        "Give your partner oral sex while they are on the phone. Hang up when the deed is done.",
    ),
    (
        "Record yourself being naughty in a public setting and send it to your partner.",
        "Amateur",
        SIZZLING,
        "Or record yourselves doing naughty things in public (changing room, elevator, etc.).",
    ),
    ("Recreate a porno video (pick at random, or already have one in mind?).", "Activity", SWEET, ""),
    ("Roleplay (play out a fantasy, or explore a theme with it).", "Roleplay", SWEET, ""),
    ("Send your partner a surprise dirty picture.", "Amateur", SWEET, ""),
    ("Take sexy nudes together.", "Amateur", SPICY, ""),
    ("Try a “naked” chef night (cook a meal together with little to no clothes on).", "Activity", SWEET, ""),
    ("Try a new sex position every day for a week.", "Challenge", SWEET, ""),
    ("Try swinging.", "Activity", SIZZLING, ""),
    ("Turn your partner on with your sexting skills.", "Challenge", SWEET, ""),
    ("Use your mouth to put a condom on him.", "Challenge", SWEET, ""),
    ("Vacation at a sex resort.", "Activity", SWEET, ""),
    ("Watch porn with your partner.", "Activity", SWEET, ""),
    ("Whisper dirty talk to each other in public.", "Public", SWEET, ""),
    ("Collar and leash.", "BDSM", SIZZLING, ""),
    ("Be a dominant mistress/master of your partner for a night.", "BDSM", SPICY, ""),
    ("Be a submissive sex slave to your partner for a night.", "BDSM", SPICY, ""),
    ("Bound and blindfolded.", "BDSM", SPICY, ""),
    ("Breath play — safely.", "BDSM", SIZZLING, ""),
    ("Chair ties.", "BDSM", SWEET, ""),
    ("Channel your dominant side in the bedroom.", "BDSM", SWEET, ""),
    ("Channel your submissive side in the bedroom.", "BDSM", SWEET, ""),
    ("Dom/sub switch it up!", "BDSM", SWEET, ""),
    ("Gagged and bound.", "BDSM", SPICY, ""),
    ("Handcuffs.", "BDSM", SWEET, ""),
    ("Hogtie experience.", "BDSM", SPICY, ""),
    ("Kinky dress-up (fishnets, harness, corset, cat ears, collar, etc.).", "Toys", SWEET, ""),
    ("Light hair pulling and biting.", "BDSM", SWEET, ""),
    ("Light spanking.", "BDSM", SWEET, ""),
    (
        "Massage (everything but between the legs… make them wait, then finish them off with a glorious happy ending).",
        "Activity",
        SWEET,
        "",
    ),
    ("Sensual restraint with scarves or a silky necktie.", "BDSM", SWEET, ""),
    ("Shibari rope harness.", "BDSM", SIZZLING, ""),
    ("Spread-eagle bed bondage.", "BDSM", SPICY, ""),
    ("Tell your partner, “Do whatever you want to me.” Just remember to use a safeword!", "Challenge", SPICY, ""),
    ("Temperature play (ice cubes, candle wax, etc.).", "BDSM", SWEET, ""),
    ("Use safewords for practice.", "BDSM", SWEET, ""),
    ("Use your nails on your partner’s back during sex.", "BDSM", SWEET, ""),
    ("Have sex in a car.", "Public", SWEET, ""),
    ("Have sex in public — sort of.", "Public", SPICY, ""),
    ("Have sex in the shower.", "Activity", SWEET, ""),
    ("Have sex on a camping trip.", "Challenge", SPICY, ""),
    ("Have sex on a desk.", "Challenge", SWEET, ""),
    ("Have sex on the beach.", "Public", SPICY, ""),
    ("Have sex on the couch.", "Challenge", SWEET, ""),
    ("Have sex outside.", "Challenge", SWEET, ""),
    ("Hook up in a hot tub.", "Challenge", SWEET, ""),
    ("Take a shower together and focus solely on intense touch and stimulation.", "Challenge", SWEET, ""),
    ("Play a sex game.", "Activity", SWEET, ""),
    ("Play a strip card game, with consequences for losing.", "Activity", SWEET, ""),
    ("Play with sex dice.", "Activity", SWEET, ""),
    ("Bring your perineum into play.", "Challenge", SIZZLING, ""),
    ("Chair sex.", "Activity", SWEET, ""),
    ("Explore squirting.", "Challenge", SPICY, ""),
    ("Fuck her mouth.", "Position", SPICY, ""),
    ("Give and/or receive a rim job.", "Position", SIZZLING, ""),
    ("Give your partner a blended orgasm.", "Challenge", SWEET, ""),
    ("Give/get a facial.", "Position", SPICY, ""),
    ("Give/get a pearl necklace.", "Position", SWEET, ""),
    ("Have a really deep penetrative sex session.", "Position", SWEET, ""),
    ("Have anal sex.", "Position", SIZZLING, ""),
    ("Sit on his face.", "Position", SPICY, ""),
    ("Spit roast.", "Position", SPICY, ""),
    ("Swallow his load.", "Position", SPICY, ""),
    ("Try “Airlock” (DP + BJ).", "Position", SIZZLING, ""),
    ("Try a finger in the butt.", "Position", SPICY, ""),
    ("Try a sex position that uses gym equipment.", "Challenge", SWEET, ""),
    ("Try a titty-fuck.", "Position", SPICY, ""),
    ("Try consensual “non-consensual” play.", "Activity", SIZZLING, ""),
    ("Try deep-throating.", "Position", SIZZLING, ""),
    ("Try double penetration.", "Position", SIZZLING, ""),
    ("Try edging for more powerful orgasms.", "Activity", SWEET, ""),
    ("Try mutual masturbation.", "Activity", SIZZLING, ""),
    ("Try pegging.", "Position", SIZZLING, ""),
    ("Do it in the Amazon sex position.", "Position", SWEET, ""),
    ("Experiment with new oral sex positions.", "Position", SPICY, ""),
    ("Explore tantric sex.", "Position", SWEET, ""),
    ("Explore the joys of a good old-fashioned missionary position.", "Position", SWEET, ""),
    ("Have sex doggy style.", "Position", SWEET, ""),
    ("Have sex in the cowgirl position.", "Position", SWEET, ""),
    ("Have sex in the reverse cowgirl position.", "Position", SWEET, ""),
    ("Have standing sex.", "Position", SWEET, ""),
    ("Try 69-ing.", "Position", SWEET, ""),
    ("Try a new position that neither of you has tried before.", "Position", SWEET, ""),
    ("Try the “anvil” sex position.", "Position", SWEET, ""),
    ("Try the “coconut” move during cowgirl.", "Position", SWEET, ""),
    ("Try the Yab-Yum position.", "Position", SWEET, ""),
    ("Try all the Kama Sutra sex positions.", "Position", SWEET, ""),
    ("Add a mirror to the action.", "Toys", SWEET, ""),
    ("Blend food and sex.", "Toys", SWEET, ""),
    ("Get wet with a body shot.", "Activity", SWEET, ""),
    ("Use a butt plug.", "Toys", SIZZLING, ""),
    ("Use a cock ring.", "Toys", SWEET, ""),
    ("Use a remote-controlled sex toy with a partner (in public?).", "Toys", SWEET, ""),
    ("Use a sex pillow.", "Toys", SWEET, ""),
    ("Use a sex toy with a partner.", "Toys", SWEET, ""),
    ("Use nipple clamps.", "Toys", SWEET, ""),
    ("Become fluent in dirty talk.", "Activity", SIZZLING, ""),
    ("Do a striptease.", "Activity", SPICY, ""),
    ("Do the “anything but penetration” challenge.", "Challenge", SWEET, ""),
    ("Give her a creampie; she decides where she wants it.", "Position", SWEET, ""),
    ("Give her a cumshot; she decides where she wants it.", "Position", SWEET, ""),
    ("Have a wake-up session.", "Activity", SWEET, ""),
    ("Have multiple orgasms in one sex session.", "Challenge", SWEET, ""),
    ("Have rough sex.", "Activity", SPICY, ""),
    ("Have sex with (most of) your clothes on.", "Challenge", SWEET, ""),
    ("Look into each other’s eyes when cumming. Bonus: cum at the same time.", "Challenge", SWEET, ""),
    ("No-kissing session.", "Challenge", SPICY, ""),
    ("One partner rips the other’s clothes off.", "Activity", SWEET, ""),
    ("Sex right after the gym.", "Challenge", SWEET, ""),
    ("Stay in bed with your partner all day long.", "Activity", SWEET, ""),
    ("Surprise each other with a new piece of lingerie or a new sex toy.", "Toys", SWEET, ""),
    ("Try out new lingerie or underwear sets.", "Toys", SWEET, ""),
    ("Wear sexy costumes.", "Toys", SWEET, ""),
]


# Levels some starter wishes come with, from a gentle start to the full thing, keyed by the
# wish's title in lowercase.
STARTER_LEVELS = {}


def starter_levels(title):
    return STARTER_LEVELS.get(title.lower(), [])


def missing_wishes(space):
    """The starter wishes the space's Kinky List doesn't have (ignoring case)."""
    existing = {title.lower() for title in space.items.values_list("title", flat=True)}
    return [wish for wish in STARTER_WISHES if wish[0].lower() not in existing]


def add_starter_list(space, user=None):
    """Give a space the starter wishes, skipping any it already has. Returns how many were added."""
    from .models import Item

    missing = missing_wishes(space)
    for title, category, spice, details in missing:
        item = Item.objects.create(space=space, title=title, description=details, spice=spice, created_by=user)
        item.set_categories([category])
        if starter_levels(title):
            item.set_levels(starter_levels(title))
    return len(missing)


def missing_truths_and_dares(space):
    """The built-in (spice, text) truths and dares the space's Truth or Dare list doesn't have (ignoring case)."""
    from games.dares import BUILT_IN_DARES
    from games.truths import BUILT_IN_TRUTHS

    have_truths = {text.lower() for text in space.truths.values_list("text", flat=True)}
    have_dares = {text.lower() for text in space.dares.values_list("text", flat=True)}
    return (
        [(spice, text) for spice, text in BUILT_IN_TRUTHS if text.lower() not in have_truths],
        [(spice, text) for spice, text in BUILT_IN_DARES if text.lower() not in have_dares],
    )


def add_truth_or_dare_list(space, user=None):
    """Give a space the built-in truths and dares it doesn't have yet. Returns how many were added."""
    from .models import Dare, Truth

    truths, dares = missing_truths_and_dares(space)
    Truth.objects.bulk_create(Truth(space=space, text=text, spice=spice, created_by=user) for spice, text in truths)
    Dare.objects.bulk_create(Dare(space=space, text=text, spice=spice, created_by=user) for spice, text in dares)
    return len(truths) + len(dares)


def missing_questions(space):
    """The built-in (spice, first, second) questions the space's "Would you rather" list doesn't have."""
    from games.would_you_rather import BUILT_IN_QUESTIONS

    have = {question.key for question in space.questions.only("first", "second")}
    return [entry for entry in BUILT_IN_QUESTIONS if f"{entry[1].lower()} | {entry[2].lower()}" not in have]


def add_would_you_rather_list(space, user=None):
    """Give a space the built-in "Would you rather" questions it doesn't have yet. Returns how many were added."""
    from .models import Question

    missing = missing_questions(space)
    Question.objects.bulk_create(
        Question(space=space, first=first, second=second, spice=spice, created_by=user)
        for spice, first, second in missing
    )
    return len(missing)


def fill_new_space(space, user=None):
    """Every new space starts with all three lists ready to play."""
    add_starter_list(space, user)
    add_truth_or_dare_list(space, user)
    add_would_you_rather_list(space, user)
