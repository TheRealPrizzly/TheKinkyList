"""The built-in lists a fresh database starts with.

Migration items/0011 copied these into the database (items.models.BuiltIn), where staff now edit
them on the Built-in lists page. Changing them here changes only what a brand-new database starts
with, never the live lists.

The Kinky List starts with The Kinky Bucket List below, as (title, category, intensity, details).
A wish in more than one category has a tuple of category names. Truth or Dare and "Would you
rather" start with the built-ins in games/truths.py, games/dares.py and games/would_you_rather.py.

Titles are capped at 140 characters (Item.title), so the few longer wishes keep
their first sentence as the title and the rest as details.
"""

SWEET, SPICY, SIZZLING = 1, 2, 3

STARTER_WISHES = [
    (
        "Be groped in public.",
        ("Public", "Teasing", "Voyeurism"),
        SPICY,
        "Have your partner grope you in a public setting.",
    ),
    (
        "Borrow your partner’s phone and take a dirty picture. They cannot look at it until one of you has left "
        "the house.",
        "Teasing",
        SPICY,
        "Leave your partner something to remember for when you are away.",
    ),
    (
        "Do naked yoga.",
        "Activity",
        SPICY,
        (
            "There is something hot about seeing your partner in certain poses that may or may not accentuate their "
            "curves and/or muscles. Let's explore that!"
        ),
    ),
    ("Dress up and have a classy night out.", "Clothing", SWEET, ""),
    (
        "For an entire session, one of you has to tell the other person what to do to them.",
        "Challenge",
        SPICY,
        "Communication (and dirty talk?) is key! It’s okay to be selfish; this one’s all about the requester.",
    ),
    (
        "Give a nuru massage.",
        "Challenge",
        SWEET,
        (
            "What is a nuru massage?\n\nIt is a form of erotic full-body massage that originated in Japan. It is "
            "characterized by the use of a water-soluble, slippery gel that allows extensive skin-to-skin contact. "
            "The giver glides their naked body over the receiver's body to create a sensual experience."
        ),
    ),
    (
        "Give him a blow job (or finger her and/or use toys) while he (or she) is driving. Stay safe and park if "
        "needed.",
        "Challenge",
        SPICY,
        (
            "Important: Safety first! As you can imagine, this can be very distracting and driving requires your full "
            "attention. Maybe, pick a place where there is no traffic, no pedestrian. You don't want to turn this "
            "fantasy into a real nightmare. If driving is too distracting, park somewhere but the idea is that this "
            "happens in the vehicle."
        ),
    ),
    (
        "Go skinny dipping at night.",
        "Activity",
        SWEET,
        (
            "You can pick a pool, or a hot tub, or any place with water that you can swim... but you both have to go "
            "in naked!"
        ),
    ),
    (
        "Go to a sex party.",
        "Activity",
        SIZZLING,
        (
            "If you are not familiar with sex parties, you will need to do some homework. Preparing for a sex party "
            "involves clarifying your boundaries, checking event rules and dress codes, packing safer-sex supplies, "
            "and getting ready physically and emotionally."
        ),
    ),
    (
        "Go to a sex store together.",
        "Activity",
        SPICY,
        (
            "Look around and talk! It's a great way to discover what your partner might be into. No purchase "
            "necessary."
        ),
    ),
    (
        "Go to a swingers’ bar.",
        "Activity",
        SIZZLING,
        (
            "Before going, make sure both of you are on the same page. Be clear on what you're both comfortable with, "
            "and what you aren't. Going to a swinger's bar does NOT mean you have to swing."
        ),
    ),
    (
        "Have a threesome.",
        "Activity",
        SIZZLING,
        (
            "Adding another person to a sex session is one of the most popular fantasies. However, this remains a "
            "fantasy for most because of concerns around jealousy and other considerations that could disrupt what "
            "the couple has built. See the levels below for options that could help with reaching a middle ground."
        ),
    ),
    ("Have mind-blowing vacation sex.", "Activity", SWEET, ""),
    ("Have phone sex.", "Activity", SPICY, ""),
    ("Have sex in every non-bedroom room of your house in one night.", "Challenge", SWEET, ""),
    ("Have sex over video chat.", "Activity", SPICY, ""),
    ("Have sex while other people are close by.", "Challenge", SPICY, ""),
    ("Have stoned sex (aka being high).", "Sensory", SWEET, "Disclaimer: Only use legal substances."),
    (
        "Join the Mile High Club.",
        "Challenge",
        SPICY,
        (
            "Disclaimer: Likely illegal, and could lead to warnings, fines, banned travel, or law enforcement "
            "involvement. With that said...\n\nSome companies provide small blankets on longer flights, how "
            "convenient. Using a sweater, or other piece of clothing can work."
        ),
    ),
    ("Lunchtime sex at work.", "Activity", SIZZLING, ""),
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
STARTER_LEVELS = {
    "be groped in public.": [
        "Sneaky and no one needs to notice.",
        "Have someone (or a group) watch.",
        "Groped by someone other than your partner (if you are both into that).",
    ],
    "borrow your partner’s phone and take a dirty picture. they cannot look at it until one of you has left the "
    "house.": [
        'Clothes stay on but show your best "features".',
        "Underwear is showing... maybe a glimpse of skin that doesn't usually get much sun?",
        "You are now showing some skin, and private parts. Be provocative, have fun with this one!",
    ],
    "do naked yoga.": [
        "Keep your yoga-wear, it's likely that curves are already showing.",
        "Yoga in your underwear is fine... real fine.",
        "Nothing but skin, and poses, and maybe you use yoga poses to try a new position or two?",
    ],
    "dress up and have a classy night out.": [
        "Enjoy your night out, but take a good look at your partner, stunning!",
        'Compliment your partner, flirt, tease, be "touchy".',
        "Dressing up is how it started, undressing each other is how it ends. Bonus if this happened before "
        "you made it back home.",
    ],
    "for an entire session, one of you has to tell the other person what to do to them.": [
        "You lead the session. You decide what your partner does to you, the positions, and how you finish.",
        "You need to have requested your partner to perform some form of dirty talk, some form of foreplay, and a "
        "mix of at least 2 sex positions.",
        "With proper guidance, your partner makes you orgasm multiple times.",
    ],
    "give a nuru massage.": [
        "Both of you are naked, simply be generous with the massage oil/gel and use your body (and body parts) to "
        "rub your partner.",
        "Massages (at least the Nuru kind) have to have a happy ending.",
        "Either one or both of you finish, BUT no penetration allowed. Be creative and good use of your body "
        "(parts).",
    ],
    "give him a blow job (or finger her and/or use toys) while he (or she) is driving. stay safe and park if "
    "needed.": [
        "Do it, if only for a brief moment just to check it off the kinky (bucket) list.",
        "The person in the driver seat needs to finish.",
        "Once the first driver finishes, you swap seats and return the favor.",
    ],
    "go skinny dipping at night.": [
        "What's the point if you aren't sharing at least a kiss.",
        "Maybe that kiss leads to some foreplay.",
        "Both of you manage to finish while still in the water.",
    ],
    "go to a sex party.": [
        "You showed up and that already took a lot of courage. Congrats, you made it!",
        "Maybe you're not interested in sharing, but your curious side leads you to watch others do their thing.",
        "Explore, maybe including someone else in your activities, or both going your separate ways to discover "
        "something else, if only for a moment.",
    ],
    "go to a sex store together.": [
        "You made it, congrats! Look around and both of you should share your observations. Your likes and "
        "dislikes.",
        "Buy something! Maybe it's lingerie, or edible massage oil, or a toy, or whatever else that seemed "
        "interesting to both of you.",
        "Whatever you bought gets used that same day. Don't wait, have fun!",
    ],
    "go to a swingers’ bar.": [
        "You made it! Look around and share with your partner the things that make you uncomfortable, and the "
        "things that make you curious.",
        'Engage with others, and find out what they are into. Who knows, maybe you\'ll find "interesting" people.',
        "Embrace your options. Take the opportunity to invite others into your partnership or be invited to meet "
        "other people in an intimate way.",
    ],
    "have a threesome.": [
        "Invite someone into your partnership with limits. Kiss & touch your partner while the 3rd person is "
        "watching, but maybe that's all, for now.",
        "You and your partner have sex. The 3rd person can only watch and tell the couple what to do to each "
        "other, but remains an observer.",
        "Include the 3rd person, they also get to have fun. Bonus: all 3 were able to finish.",
    ],
    "have mind-blowing vacation sex.": [
        "You have sex while you are on vacation, home is fine.",
        "You have sex during a vacation somewhere else. Frankly, anywhere else but home.",
        "You have sex somewhere far away. Maybe you had to take a plane to get there. Maybe at a resort, a "
        "cruise. Bonus: in a different country.",
    ],
    "have phone sex.": [
        "Flirt, talk dirty to each other.",
        "Do level 1 but add masturbation.",
        "One of you was able to finish (Bonus: both finished)",
    ],
    "have sex in every non-bedroom room of your house in one night.": [
        "Any kind of touching is fine, as long as you have done so in every room.",
        "Every room means trying a different position.",
        "Each room requires an orgasm before moving on to the next. Godspeed!",
    ],
    "have sex over video chat.": [
        "Flirt, talk dirty and have fun. No need to show what's going on down there.",
        "Undress each other (by asking the other which piece of clothing to remove).",
        "This video chat has naturally progressed to one (or both) of you to masturbate and finish. Bonus if both "
        "were able to finish.",
    ],
    "have sex while other people are close by.": [
        "Some touching, maybe some foreplay if you dare!",
        "You have sex where at least one of you finished.",
        'Level 2 but by "other people", we really mean "a lot of people".',
    ],
    "have stoned sex (aka being high).": [
        "Drunk sex is fine at this level.",
        "Have sex under a very light influence of substances.",
        "Have sex under a stronger influence of substances (responsibly, of course).",
    ],
    "join the mile high club.": [
        "Use your hands to pleasure your partner while they're at their seat. Bonus: Orgasm",
        "Figure out a way to perform oral sex discreetly. Bonus: Orgasm",
        "Figure out a way to perform penetrative sex. Bonus: Orgasm",
    ],
    "lunchtime sex at work.": [
        "Maybe some kissing, maybe some inappropriate touching.",
        "Any kind of sex, even if it's just to check it off the kinky (bucket) list.",
        "One (or both) of you were able to finish.",
    ],
}


def category_names(category):
    """A starter wish's categories as a list: its one category name, or its tuple of them."""
    return [category] if isinstance(category, str) else list(category)
