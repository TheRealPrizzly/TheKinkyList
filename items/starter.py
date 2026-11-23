"""The built-in lists a fresh database starts with.

Migration items/0011 copied these into the database (items.models.BuiltIn), where staff now edit
them on the Built-in lists page. Changing them here changes only what a brand-new database starts
with, never the live lists. (Migration items/0012 also wrote the wishes' details and levels into
the live lists, once.)

The Kinky List starts with The Kinky Bucket List below, as (title, category, intensity, details).
A wish in more than one category has a tuple of category names. A wish's details say what it asks
and why couples enjoy it, then give a tip. Truth or Dare and "Would you rather" start with the
built-ins in games/truths.py, games/dares.py and games/would_you_rather.py.

Titles are capped at 140 characters (Item.title), so the few longer wishes keep
their first sentence as the title and the rest as details.
"""

SWEET, SPICY, SIZZLING = 1, 2, 3

STARTER_WISHES = [
    (
        "Be groped in public.",
        ("Public", "Teasing", "Voyeurism"),
        SPICY,
        (
            "Let your partner’s hands wander over you somewhere public, like a crowded bar, a concert or a busy "
            "train. The thrill is in keeping a straight face while they touch you, knowing someone could notice at "
            "any moment.\n\n"
            "Tip: Strangers never agreed to be part of your game, so keep it discreet in everyday places. Save the "
            "watchers for spaces where watching is welcome, like a play party."
        ),
    ),
    (
        "Borrow your partner’s phone and take a dirty picture. They cannot look at it until one of you has left the "
        "house.",
        "Teasing",
        SPICY,
        (
            "Sneak a sexy photo of yourself onto your partner’s phone, then make them wait: no peeking until one of "
            "you has left the house. It gives them something to remember you by while you’re apart, and turns an "
            "ordinary day into a long tease.\n\n"
            "Tip: Make sure their photos don’t sync to a shared family album or a work account, and tell them where "
            "to look once they’re out the door."
        ),
    ),
    (
        "Do naked yoga.",
        "Activity",
        SPICY,
        (
            "Roll out your mats and do a yoga session together with nothing on. There’s something hot about seeing "
            "your partner in poses that show off every curve and muscle, and it’s hard to stay focused on your "
            "breathing for long.\n\n"
            "Tip: Warm up the room first (goosebumps aren’t sexy), and follow a beginner video so neither of you has "
            "to lead."
        ),
    ),
    (
        "Dress up and have a classy night out.",
        "Clothing",
        SWEET,
        (
            "Put on your best outfits and treat each other to a proper night out: a nice dinner, cocktails, a show. "
            "Seeing your partner all dressed up reminds you why you fell for them, and the whole evening becomes a "
            "slow build-up to getting each other out of those clothes.\n\n"
            "Tip: Keep your outfits a surprise until you’re both ready to leave, so you get the full effect."
        ),
    ),
    (
        "For an entire session, one of you has to tell the other person what to do to them.",
        "Challenge",
        SPICY,
        (
            "One of you directs the whole session, telling the other exactly what to do: where to touch, how fast, "
            "which positions and how to finish. It’s okay to be selfish here, because this one is all about the "
            "person giving the orders, and you’ll both learn exactly what they like.\n\n"
            "Tip: Communication (and dirty talk?) is key! Be specific, like “slower”, “right there” or “don’t stop”."
        ),
    ),
    (
        "Give a nuru massage.",
        "Challenge",
        SWEET,
        (
            "A nuru massage is an erotic full-body massage that originated in Japan. You both get naked and covered "
            "in a slippery, water-based gel, and the giver glides their whole body over the receiver’s. It’s "
            "skin-to-skin contact from head to toe, and as much fun to give as to receive.\n\n"
            "Tip: Use nuru gel or another water-based massage gel, and cover the bed or floor with an old sheet or a "
            "waterproof blanket. Things get slippery, so take care getting up."
        ),
    ),
    (
        "Give him a blow job (or finger her and/or use toys) while he (or she) is driving. Stay safe and park if "
        "needed.",
        "Challenge",
        SPICY,
        (
            "Pleasure your partner with your mouth, your fingers or a toy while they’re behind the wheel. It’s a "
            "classic fantasy because it feels so forbidden: they have to keep their cool while you do your best to "
            "make them lose it.\n\n"
            "Tip: Safety first! Driving needs their full attention, so the safest version is parked somewhere quiet. "
            "If you do drive, pick an empty road with no traffic or pedestrians. Don’t turn this fantasy into a real "
            "nightmare."
        ),
    ),
    (
        "Go skinny dipping at night.",
        "Activity",
        SWEET,
        (
            "Slip into the water together after dark: a pool, a hot tub, a quiet lake, anywhere you can swim, as "
            "long as you both go in naked! It feels wonderfully free, and the cool water and the chance of being "
            "spotted make every kiss more exciting.\n\n"
            "Tip: Pick a spot you know is safe to swim in, don’t swim after drinking, and keep your towels close for "
            "a quick getaway."
        ),
    ),
    (
        "Go to a sex party.",
        "Activity",
        SIZZLING,
        (
            "Go together to a party where sex happens out in the open. You don’t have to do anything once you’re "
            "there: just being in the room, seeing what others enjoy and feeling each other’s reactions can be a "
            "huge turn-on, and a story you’ll share forever.\n\n"
            "Tip: Do your homework first. Agree on your boundaries, read the event’s rules and dress code, pack "
            "safer-sex supplies, and pick a signal that means “let’s go home”."
        ),
    ),
    (
        "Go to a sex store together.",
        "Activity",
        SPICY,
        (
            "Browse a sex shop together, side by side. Seeing what makes your partner curious, laugh or blush is a "
            "great way to discover what they might be into, and it gets you talking about things that can be hard to "
            "bring up out of the blue.\n\n"
            "Tip: No purchase necessary! Good shops have heard every question, so ask the staff anything."
        ),
    ),
    (
        "Go to a swingers’ bar.",
        "Activity",
        SIZZLING,
        (
            "Spend a night at a bar or club for swingers, where couples go to flirt, watch and sometimes swap "
            "partners. Going does NOT mean you have to swing: plenty of couples just enjoy the charged atmosphere "
            "and head home to each other.\n\n"
            "Tip: Get on the same page before you go. Be clear about what you’re both comfortable with and what you "
            "aren’t, and check in with each other during the night."
        ),
    ),
    (
        "Have a threesome.",
        "Activity",
        SIZZLING,
        (
            "Invite a third person into your bed. It’s one of the most popular fantasies, but it stays a fantasy for "
            "most couples because of jealousy and the worry that it could shake what you’ve built together. The "
            "levels below offer a middle ground to work up to it.\n\n"
            "Tip: Talk everything through beforehand: who, where, what’s off-limits and how you’ll check in. Your "
            "relationship comes first, whatever happens."
        ),
    ),
    (
        "Have mind-blowing vacation sex.",
        "Activity",
        SWEET,
        (
            "Make the most of your time off with sex that’s slow, adventurous and completely unhurried. On vacation "
            "there are no chores, no work and no alarms, so you can focus on each other, and a new place makes "
            "everything feel new again.\n\n"
            "Tip: Pack a little kit: lube, a toy and something sexy to wear. And hotel sheets are someone else’s "
            "problem."
        ),
    ),
    (
        "Have phone sex.",
        "Activity",
        SPICY,
        (
            "Get each other going with nothing but your voices: what you’d do if you were together, what you’re "
            "doing right now, what you want next. With nothing to see, your imagination does all the work, and it "
            "keeps you close when you’re apart.\n\n"
            "Tip: Find a spot where no one can overhear, use earbuds to keep your hands free, and don’t worry if you "
            "both giggle at first."
        ),
    ),
    (
        "Have sex in every non-bedroom room of your house in one night.",
        "Challenge",
        SWEET,
        (
            "Turn your home into a tour in one night: the kitchen, the living room, the bathroom, the hallway, even "
            "the laundry room. Every room has its own furniture and possibilities, and you’ll never look at your "
            "place the same way again.\n\n"
            "Tip: Plan your route, close the curtains, and leave water and a towel along the way. Pace yourselves!"
        ),
    ),
    (
        "Have sex over video chat.",
        "Activity",
        SPICY,
        (
            "When you’re apart, get intimate over a video call: flirt, undress for each other and watch each other "
            "get off. Seeing your partner’s reactions up close keeps the spark alive at any distance, and putting on "
            "a show for the camera is a thrill of its own.\n\n"
            "Tip: Use a private app you both trust, check what’s visible behind you, and never screenshot or record "
            "without asking first."
        ),
    ),
    (
        "Have sex while other people are close by.",
        "Challenge",
        SPICY,
        (
            "Get intimate while others are nearby: at a family gathering, a party, or with friends in the next room. "
            "Having to stay quiet makes every touch more intense, and the risk of being heard turns it into a "
            "thrilling secret between you.\n\n"
            "Tip: Stay out of sight and out of earshot. The thrill is in almost getting caught, not in making anyone "
            "else part of it."
        ),
    ),
    (
        "Have stoned sex (aka being high).",
        "Sensory",
        SWEET,
        (
            "Have sex while you’re both a little high, or tipsy. Many people find that it heightens touch and taste, "
            "slows everything down and makes it easier to let go of nerves.\n\n"
            "Tip: Only use legal substances, start low and go slow. You both need to stay clear-headed enough to say "
            "yes, and to say no."
        ),
    ),
    (
        "Join the Mile High Club.",
        "Challenge",
        SPICY,
        (
            "Get intimate on a plane, mid-flight, more than a mile above the ground. It’s one of the most famous "
            "bucket-list fantasies, and the tiny space, the crew walking by and the passengers all around make it a "
            "real test of nerve and stealth.\n\n"
            "Tip: It’s likely illegal and could lead to warnings, fines, a travel ban or worse. With that said… the "
            "blankets on long flights are very convenient, and a sweater works too."
        ),
    ),
    (
        "Lunchtime sex at work.",
        "Activity",
        SIZZLING,
        (
            "Use your lunch break for something other than lunch: meet up at the office, in a parked car, or slip "
            "home for a quickie. The ticking clock and going back to work as if nothing happened make it a real "
            "rush.\n\n"
            "Tip: Getting caught at work could cost you your job, so think twice before using the office itself. "
            "Working from home counts!"
        ),
    ),
    (
        "Make a sex tape.",
        "Amateur",
        SIZZLING,
        (
            "Film yourselves having sex, for your eyes only. Knowing the camera is rolling tends to bring out the "
            "show-off in both of you, and watching it back together can turn you on all over again.\n\n"
            "Tip: Agree on where the video will be kept before you hit record, and turn off cloud backup on the "
            "device you use. Either of you can ask to delete it at any time, no questions asked."
        ),
    ),
    (
        "Next time your partner receives a telemarketer’s call, he/she cannot hang up!",
        "Challenge",
        SWEET,
        (
            "Your partner takes the next telemarketer’s call and has to keep chatting while you go down on them. "
            "Hang up when the deed is done. Trying to sound normal while you do your best to break their "
            "concentration is equal parts hot and hilarious.\n\n"
            "Tip: Muting is cheating. Put the call on speaker so you can enjoy every awkward pause too."
        ),
    ),
    (
        "Record yourself being naughty in a public setting and send it to your partner.",
        "Amateur",
        SIZZLING,
        (
            "Film a short, naughty clip of yourself somewhere public, like a changing room, an elevator or a quiet "
            "corner, and send it to your partner. Or record yourselves doing naughty things together. It’s a daring "
            "tease that lets them share the thrill from wherever they are.\n\n"
            "Tip: Never catch other people on camera, know the local laws, and send it through an app you both trust."
        ),
    ),
    (
        "Recreate a porno video (pick at random, or already have one in mind?).",
        "Activity",
        SWEET,
        (
            "Pick a porn scene, one you love or one chosen at random, and act it out together, from the cheesy setup "
            "to the big finish. It’s part role-play, part comedy and part turn-on, and it shows you what your "
            "partner finds hot on screen.\n\n"
            "Tip: Watch the scene together first, and remember that porn is choreographed by professionals, with "
            "retakes. Skip anything that doesn’t feel good in real life."
        ),
    ),
    (
        "Roleplay (play out a fantasy, or explore a theme with it).",
        "Roleplay",
        SWEET,
        (
            "Step into characters and play out a fantasy together: strangers at a bar, a boss and an employee, or "
            "anything you’ve been curious about. Playing someone else makes it easier to be bold, and brings out "
            "sides of each other you rarely see.\n\n"
            "Tip: Agree on the scenario and any limits before you start, and pick a safeword to step out of "
            "character."
        ),
    ),
    (
        "Send your partner a surprise dirty picture.",
        "Amateur",
        SWEET,
        (
            "Out of the blue, send your partner a sexy photo of yourself. It’s a quick, easy way to let them know "
            "you’re thinking about them, and to keep them thinking about you for the rest of the day.\n\n"
            "Tip: Make sure they’re free to look (not in a meeting or handing their phone to someone), and use an "
            "app you both trust."
        ),
    ),
    (
        "Take sexy nudes together.",
        "Amateur",
        SPICY,
        (
            "Have a private photo shoot, taking turns as photographer and model, or posing together with a timer. "
            "Seeing yourself through your partner’s eyes is a real confidence boost, and the shoot itself tends to "
            "turn into foreplay.\n\n"
            "Tip: Good light does wonders: try a window during the day or a warm lamp at night. Keep the photos "
            "somewhere private you both agree on."
        ),
    ),
    (
        "Try a “naked” chef night (cook a meal together with little to no clothes on).",
        "Activity",
        SWEET,
        (
            "Cook dinner together wearing as little as you both dare: underwear, just an apron, or nothing at all. "
            "An ordinary meal turns into a long, flirty warm-up, with every excuse to brush past each other, feed "
            "each other bites and get a little distracted.\n\n"
            "Tip: Pick a simple dish that won’t splatter (save the bacon for another night), and keep an apron on "
            "near anything hot."
        ),
    ),
    (
        "Try a new sex position every day for a week.",
        "Challenge",
        SWEET,
        (
            "For seven days in a row, have sex in a position you’ve never tried together. It breaks you out of your "
            "usual routine, and you’ll probably find a new favorite, along with a few that are funnier than they are "
            "sexy.\n\n"
            "Tip: Pick all seven in advance, from a book, an app or a deck of cards, so you don’t have to decide in "
            "the moment."
        ),
    ),
    (
        "Try swinging.",
        "Activity",
        SIZZLING,
        (
            "Swap partners with another couple, whether that means kissing, watching each other or going all the "
            "way. For couples who enjoy it, sharing the experience and coming home to each other afterward can be "
            "one of the most exciting things they do together.\n\n"
            "Tip: Talk through your boundaries in detail before meeting anyone, start with experienced and "
            "respectful couples, and always use protection."
        ),
    ),
    (
        "Turn your partner on with your sexting skills.",
        "Challenge",
        SWEET,
        (
            "Text your partner something so steamy they can’t stop thinking about you: what you’re wearing, what you "
            "remember, what you’ll do later. A good sexting session builds anticipation for hours, and makes coming "
            "home the main event.\n\n"
            "Tip: Turn off message previews on your lock screens so nobody else catches a glimpse."
        ),
    ),
    (
        "Use your mouth to put a condom on him.",
        "Challenge",
        SWEET,
        (
            "Roll a condom onto your partner using only your lips and mouth, no hands. It’s a sexy party trick that "
            "turns a practical pause into part of the foreplay.\n\n"
            "Tip: Practice on a banana or a toy first. Pinch the tip of the condom with your lips to leave room at "
            "the end, and keep your teeth out of the way."
        ),
    ),
    (
        "Vacation at a sex resort.",
        "Activity",
        SWEET,
        (
            "Book a getaway at an adults-only, sex-positive resort, where nudity is welcome and flirting with other "
            "guests is part of the fun. Even if you keep to yourselves, the relaxed, anything-goes atmosphere makes "
            "it easy to let loose together.\n\n"
            "Tip: Read the resort’s rules and reviews before booking: some are clothing-optional, some host "
            "lifestyle parties, and some are mostly about the vibe."
        ),
    ),
    (
        "Watch porn with your partner.",
        "Activity",
        SWEET,
        (
            "Pick something to watch together and see where it leads. It’s a low-pressure way to discover what turns "
            "your partner on, and seeing how they react can be hotter than anything on screen.\n\n"
            "Tip: Take turns choosing, and try ethical, performer-friendly sites for more realistic, less scripted "
            "scenes."
        ),
    ),
    (
        "Whisper dirty talk to each other in public.",
        "Public",
        SWEET,
        (
            "Lean in close somewhere public and whisper exactly what you want to do to your partner later. Keeping a "
            "straight face while they describe something filthy, surrounded by people who have no idea, is a "
            "delicious kind of torture.\n\n"
            "Tip: Keep your voice low and mind who’s nearby. The fun is in your partner being the only one who hears."
        ),
    ),
    (
        "Collar and leash.",
        "BDSM",
        SIZZLING,
        (
            "One partner wears a collar, and the other holds the leash. It’s a powerful symbol of trust and "
            "ownership in a dom/sub dynamic: the one wearing it gets to let go, and the one holding it gets to "
            "lead.\n\n"
            "Tip: Leave room for two fingers under the collar, and never pull on the neck. The leash is for guiding, "
            "not yanking."
        ),
    ),
    (
        "Be a dominant mistress/master of your partner for a night.",
        "BDSM",
        SPICY,
        (
            "For one night, you’re in charge: you set the rules, give the orders and decide what your partner gets, "
            "and when. Taking full control can be a thrill for the dominant, and a huge relief for a partner who "
            "loves to let go.\n\n"
            "Tip: Agree on limits and a safeword beforehand, check in now and then, and make time for aftercare when "
            "the night is over."
        ),
    ),
    (
        "Be a submissive sex slave to your partner for a night.",
        "BDSM",
        SPICY,
        (
            "For one night, your partner calls the shots and you obey: their wish is your command. Letting go of "
            "every decision can be incredibly freeing, and it gives your partner the chance to explore their "
            "dominant side.\n\n"
            "Tip: Set your limits and a safeword before the night starts. Your submission is a gift, and you can "
            "take it back at any time."
        ),
    ),
    (
        "Bound and blindfolded.",
        "BDSM",
        SPICY,
        (
            "One of you is tied up and blindfolded while the other takes charge. Without sight or the freedom to "
            "move, every touch, kiss and whisper feels more intense, and handing over control builds a lot of trust "
            "between you.\n\n"
            "Tip: Agree on a safeword before anyone is tied up, keep safety scissors within reach, and check hands "
            "and feet for tingling or numbness. Never leave a tied-up partner alone."
        ),
    ),
    (
        "Breath play — safely.",
        "BDSM",
        SIZZLING,
        (
            "Breath play means controlling your partner’s breathing to heighten arousal and intensify orgasms. "
            "Couples who enjoy it love the extreme trust and surrender it takes. It’s also one of the riskiest "
            "things on this list, so the levels stay on the safer side.\n\n"
            "Tip: Never press on the front of the throat, and never put anything around the neck. Agree on a hand "
            "signal, since your partner may not be able to speak, and stop the moment anything feels off."
        ),
    ),
    (
        "Chair ties.",
        "BDSM",
        SWEET,
        (
            "Tie your partner to a sturdy chair, then tease them while all they can do is sit and watch. It’s an "
            "easy, comfortable way to try bondage, and there’s something irresistible about having them right where "
            "you want them.\n\n"
            "Tip: Use a stable chair without wheels, tie with soft rope, scarves or cuffs, and check that their "
            "hands and feet don’t go numb."
        ),
    ),
    (
        "Channel your dominant side in the bedroom.",
        "BDSM",
        SWEET,
        (
            "Take the lead in bed: decide the pace, the positions and what happens next. You don’t need any gear for "
            "this, just confidence, and many partners love the feeling of being wanted this much.\n\n"
            "Tip: Dominance is about control, not cruelty. Watch your partner’s reactions and adjust as you go."
        ),
    ),
    (
        "Channel your submissive side in the bedroom.",
        "BDSM",
        SWEET,
        (
            "Let your partner take the lead while you follow: no decisions, no planning, just responding to what "
            "they want. Handing over control can be wonderfully relaxing, and it lets you enjoy your partner’s "
            "confident side.\n\n"
            "Tip: Tell your partner beforehand what you’d like to experience, and remember that you can always say "
            "stop."
        ),
    ),
    (
        "Dom/sub switch it up!",
        "BDSM",
        SWEET,
        (
            "Take turns being in charge: one of you dominates, then you swap roles. Playing both sides shows you "
            "what your partner enjoys about each role, and you might discover you love the one you least "
            "expected.\n\n"
            "Tip: Decide how and when you’ll switch before you start, like a timer or a code word, and use the same "
            "safeword for both."
        ),
    ),
    (
        "Gagged and bound.",
        "BDSM",
        SPICY,
        (
            "One of you is tied up and gagged, unable to move or speak, while the other takes control. Taking away "
            "someone’s voice adds an intense layer of helplessness and surrender, and the muffled sounds can be very "
            "hot.\n\n"
            "Tip: A gag takes away the safeword, so agree on a signal that needs no words, like dropping a ball or "
            "tapping three times. Make sure they can breathe easily through the nose, and never leave them alone."
        ),
    ),
    (
        "Handcuffs.",
        "BDSM",
        SWEET,
        (
            "Cuff one partner’s wrists and let the other take over. Handcuffs are one of the easiest ways to try "
            "bondage, and the click of the lock alone can be enough to get you both going.\n\n"
            "Tip: Choose padded or fur-lined cuffs over metal ones, which can bruise and press on nerves, and always "
            "keep the key or the quick release within reach."
        ),
    ),
    (
        "Hogtie experience.",
        "BDSM",
        SPICY,
        (
            "A hogtie binds the wrists and ankles together behind the back, leaving the tied partner completely "
            "helpless. It’s a striking, intense position for couples who already enjoy bondage and want to take it a "
            "step further.\n\n"
            "Tip: Keep it short, especially lying face down, since it can make breathing harder. Keep safety "
            "scissors close, and never leave them alone."
        ),
    ),
    (
        "Kinky dress-up (fishnets, harness, corset, cat ears, collar, etc.).",
        "Toys",
        SWEET,
        (
            "Dress up in kinky gear for each other: fishnets, a harness, a corset, cat ears, a collar, whatever "
            "makes you feel sexy. An outfit changes how you carry yourself, and seeing your partner in something "
            "unexpected is an instant turn-on.\n\n"
            "Tip: Shop together, online or in person, and let each of you pick one piece for the other to wear."
        ),
    ),
    (
        "Light hair pulling and biting.",
        "BDSM",
        SWEET,
        (
            "Add a little bite to your passion: grab a handful of hair, nibble an earlobe, sink your teeth into a "
            "shoulder. These small, primal touches add intensity without any gear, and show your partner just how "
            "much you want them.\n\n"
            "Tip: Grab hair close to the scalp so the pull is spread out, and bite fleshy spots, not bony ones. Ask "
            "whether marks are okay before you leave any."
        ),
    ),
    (
        "Light spanking.",
        "BDSM",
        SWEET,
        (
            "Give your partner a playful smack on the butt during foreplay or in the middle of sex. A little sting "
            "brings blood to the surface, makes the skin extra sensitive and adds a naughty edge to any session.\n\n"
            "Tip: Stick to the fleshy part of the butt, away from the lower back and tailbone. Start with lighter "
            "taps, and rub the spot afterward."
        ),
    ),
    (
        "Massage (everything but between the legs… make them wait, then finish them off with a glorious happy "
        "ending).",
        "Activity",
        SWEET,
        (
            "Give your partner a long, full-body massage that deliberately avoids the one place they want you most. "
            "Making them wait builds anticipation to almost unbearable levels, so when you finally give them their "
            "happy ending, it’s worth every minute.\n\n"
            "Tip: Warm the oil in your hands first, put on some music, and take your time. The longer you wait, the "
            "better it gets."
        ),
    ),
    (
        "Sensual restraint with scarves or a silky necktie.",
        "BDSM",
        SWEET,
        (
            "Use something soft from your closet, like a silk scarf or a necktie, to loosely tie your partner’s "
            "wrists. It’s the gentlest introduction to bondage: more about the feeling of being held than about "
            "being stuck.\n\n"
            "Tip: Tie loose enough to slip a finger underneath, and avoid knots that tighten when pulled. Silk knots "
            "can be hard to undo, so keep scissors nearby."
        ),
    ),
    (
        "Shibari rope harness.",
        "BDSM",
        SIZZLING,
        (
            "Shibari is the Japanese art of rope bondage, where the patterns are as beautiful as they are binding. A "
            "rope harness wraps the chest or body in a decorative pattern, and the slow, careful tying is an "
            "intimate ritual of its own.\n\n"
            "Tip: Learn from a good tutorial or a class, use rope made for bondage (cotton or jute), keep it away "
            "from the neck, and have safety shears within reach."
        ),
    ),
    (
        "Spread-eagle bed bondage.",
        "BDSM",
        SPICY,
        (
            "Tie your partner to the four corners of the bed, arms and legs spread wide, completely open to you. "
            "Being on display and unable to cover up is a thrill of its own, and every inch of them is yours to "
            "explore.\n\n"
            "Tip: An under-the-bed restraint kit makes this easy on any bed. Leave a little slack in the ties, and "
            "check on their circulation."
        ),
    ),
    (
        "Tell your partner, “Do whatever you want to me.” Just remember to use a safeword!",
        "Challenge",
        SPICY,
        (
            "Give your partner free rein over your body for a session, and let them do whatever they’ve been wanting "
            "to try. It’s an exciting act of trust, and a great way to find out what your partner fantasizes "
            "about.\n\n"
            "Tip: “Whatever you want” still has limits. Agree on your hard no’s and a safeword first, and use it if "
            "you need to."
        ),
    ),
    (
        "Temperature play (ice cubes, candle wax, etc.).",
        "BDSM",
        SWEET,
        (
            "Play with hot and cold on your partner’s skin: an ice cube down the spine, a drip of warm wax, a warm "
            "mouth right after something cold. The contrast wakes up every nerve and makes even simple touches feel "
            "electric.\n\n"
            "Tip: Use low-temperature candles made for wax play, or massage candles, never regular ones, and test a "
            "drop on your own wrist first."
        ),
    ),
    (
        "Use safewords for practice.",
        "BDSM",
        SWEET,
        (
            "Pick your safewords together and practice using them, so they feel natural before you ever need them. "
            "Many couples use the traffic light system: green means keep going, yellow means slow down, red means "
            "stop. Knowing you can stop at any moment makes it easier to explore.\n\n"
            "Tip: Choose words you’d never say by accident in bed, and agree on a signal without words too, in case "
            "one of you can’t speak."
        ),
    ),
    (
        "Use your nails on your partner’s back during sex.",
        "BDSM",
        SWEET,
        (
            "Drag your nails down your partner’s back while you’re having sex. It’s an instinctive way to show them "
            "how good it feels, and the light sting adds a jolt of sensation for them.\n\n"
            "Tip: Keep your nails smooth, without sharp edges, and ask first if marks are okay. Some people love "
            "them, some have a beach day coming up."
        ),
    ),
    (
        "Have sex in a car.",
        "Public",
        SWEET,
        (
            "Get it on in a car, parked on a quiet road or in your own driveway. The tight space forces you to get "
            "creative, and it brings back the thrill of being young and sneaking around.\n\n"
            "Tip: Park somewhere private where it’s legal to stop, and use the back seat, where there’s more room. "
            "Fogged-up windows are a bonus."
        ),
    ),
    (
        "Have sex in public — sort of.",
        "Public",
        SPICY,
        (
            "Get the thrill of public sex without truly being in public: on a balcony, in the backyard, in a tent, "
            "in a car with tinted windows. You feel exposed, but nobody can actually see you, so you get all the "
            "excitement with very little risk.\n\n"
            "Tip: Double-check that you really are out of sight. Being seen by strangers isn’t part of the deal, and "
            "it can get you into legal trouble."
        ),
    ),
    (
        "Have sex in the shower.",
        "Activity",
        SWEET,
        (
            "Step into the shower together and let things heat up under the water. Wet skin, steam and soap make "
            "every touch feel slick and new, and you’re already naked.\n\n"
            "Tip: Put down a non-slip mat, and use silicone lube: water washes the regular kind away."
        ),
    ),
    (
        "Have sex on a camping trip.",
        "Challenge",
        SPICY,
        (
            "Take your love life into the great outdoors: in your tent, under the stars, or by the lake at sunrise. "
            "Being out in nature feels wild and free, and the thin tent walls make it a test of how quiet you can "
            "be.\n\n"
            "Tip: Bring an extra blanket or a double sleeping bag, and remember that sound carries a long way at a "
            "campsite."
        ),
    ),
    (
        "Have sex on a desk.",
        "Challenge",
        SWEET,
        (
            "Clear off a desk (dramatically or carefully, your call) and have sex on it. Whether it’s your home "
            "office or a boss-and-assistant role-play, it’s the perfect height for standing positions, and it breaks "
            "up the bedroom routine.\n\n"
            "Tip: Check that the desk can take the weight and doesn’t wobble, and move the laptop first."
        ),
    ),
    (
        "Have sex on the beach.",
        "Public",
        SPICY,
        (
            "Have sex on a secluded beach, with the sound of the waves and the sand under your blanket. It’s a "
            "classic romantic fantasy, and the mix of nature, moonlight and a little risk makes it unforgettable.\n\n"
            "Tip: Bring a big blanket (sand gets everywhere), pick a secluded spot or go at night, and check the "
            "local rules on nudity."
        ),
    ),
    (
        "Have sex on the couch.",
        "Challenge",
        SWEET,
        (
            "Skip the bedroom and have sex on the couch, like you might have when you first got together. The "
            "armrests, cushions and back make it a surprisingly versatile spot for new positions.\n\n"
            "Tip: Try bending over the armrest, or one of you sitting while the other straddles. Throw a blanket "
            "down first."
        ),
    ),
    (
        "Have sex outside.",
        "Challenge",
        SWEET,
        (
            "Take things outdoors: your backyard, a secluded spot in the woods, a field under the stars. The fresh "
            "air, the sounds of nature and the feeling of being exposed make it a wild change from the bedroom.\n\n"
            "Tip: Choose a truly private place, bring a blanket and bug spray, and check for ants before you lie "
            "down."
        ),
    ),
    (
        "Hook up in a hot tub.",
        "Challenge",
        SWEET,
        (
            "Slip into a hot tub together and let the warm water and bubbles do the rest. The heat relaxes your "
            "bodies, the jets add extra sensation, and the water makes you feel almost weightless.\n\n"
            "Tip: Hot water and chlorine wash away natural lubrication and can weaken condoms, so use silicone lube, "
            "and take breaks to cool off and drink water."
        ),
    ),
    (
        "Take a shower together and focus solely on intense touch and stimulation.",
        "Challenge",
        SWEET,
        (
            "Shower together with one goal: touching each other as much as possible, without rushing to sex. Soaping "
            "each other up slowly and exploring every inch turns a routine shower into an intimate, arousing "
            "ritual.\n\n"
            "Tip: Use a body wash you both love the smell of, and the massage setting on the showerhead if you have "
            "one."
        ),
    ),
    (
        "Play a sex game.",
        "Activity",
        SWEET,
        (
            "Turn foreplay into a game: a board game, a card deck, an app, or one you invent together. Games take "
            "the pressure off, bring out your playful side and push you to try things you wouldn’t think of on your "
            "own.\n\n"
            "Tip: Set the rules before you start, including what happens when someone wants to skip a dare."
        ),
    ),
    (
        "Play a strip card game, with consequences for losing.",
        "Activity",
        SWEET,
        (
            "Play a card game you both know, like poker or blackjack, where every lost hand costs a piece of "
            "clothing. Once someone runs out of clothes, the consequences begin. It’s a fun, flirty way to build "
            "anticipation.\n\n"
            "Tip: Agree on the consequences before the first hand, and wear a few extra layers if you’re bad at "
            "cards."
        ),
    ),
    (
        "Play with sex dice.",
        "Activity",
        SWEET,
        (
            "Roll a pair of sex dice, one with actions and one with body parts, and do whatever they say. It takes "
            "the guesswork out of foreplay and leaves it up to chance, which is half the fun.\n\n"
            "Tip: No dice? Make your own with stickers on regular dice, or use a dice app."
        ),
    ),
    (
        "Bring your perineum into play.",
        "Challenge",
        SIZZLING,
        (
            "The perineum, the area between the genitals and the anus, is packed with nerve endings and often "
            "ignored. Touching, pressing or licking it can add a whole new layer to oral sex, handjobs and "
            "penetration, and lead to stronger orgasms.\n\n"
            "Tip: Start with light pressure and a little lube, and keep your nails short and smooth."
        ),
    ),
    (
        "Chair sex.",
        "Activity",
        SWEET,
        (
            "Have sex on a sturdy chair, with one of you seated and the other on their lap, facing them or facing "
            "away. A chair gives you great leverage and deep, close positions, and it gets you out of the "
            "bedroom.\n\n"
            "Tip: Use a stable chair without wheels, and push it against a wall for extra support."
        ),
    ),
    (
        "Explore squirting.",
        "Challenge",
        SPICY,
        (
            "Squirting is the release of fluid during intense arousal or orgasm, usually from G-spot stimulation. "
            "Exploring it together is a fun, messy adventure, and many people find the release itself incredibly "
            "satisfying.\n\n"
            "Tip: Lay down a towel or a waterproof blanket, stay hydrated, and relax. Pressure to squirt is the "
            "fastest way to make it not happen."
        ),
    ),
    (
        "Fuck her mouth.",
        "Position",
        SPICY,
        (
            "She lies back or kneels, and he takes control, thrusting into her mouth instead of her doing the work. "
            "It’s a rough, dominant twist on oral sex that many people find incredibly hot, as long as she’s the one "
            "setting the limits.\n\n"
            "Tip: Agree on a tap-out signal, since she can’t speak, and let her control the depth at first with her "
            "hands on your hips."
        ),
    ),
    (
        "Give and/or receive a rim job.",
        "Position",
        SIZZLING,
        (
            "A rim job is oral sex on the anus: licking and kissing around the opening. The area is full of nerve "
            "endings, and for many people it’s an intensely pleasurable, intimate and deliciously taboo "
            "experience.\n\n"
            "Tip: Shower beforehand, and use a dental dam to protect against infections. Never go from the anus to "
            "the vagina without washing first."
        ),
    ),
    (
        "Give your partner a blended orgasm.",
        "Challenge",
        SWEET,
        (
            "A blended orgasm comes from stimulating two spots at once, usually the clitoris and the G-spot, or the "
            "penis and the prostate. The two sensations build together into a deeper, full-body orgasm.\n\n"
            "Tip: Use your fingers on one spot and your mouth or a toy on the other, and keep a steady rhythm on "
            "both."
        ),
    ),
    (
        "Give/get a facial.",
        "Position",
        SPICY,
        (
            "Finish on your partner’s face at the end of oral sex or a session. It’s a classic from porn that some "
            "love for the dominance and some for the sheer naughtiness of it, and it only works if you’re both into "
            "it.\n\n"
            "Tip: Avoid the eyes (it stings), keep a towel or wipes nearby, and talk about it beforehand, not in the "
            "heat of the moment."
        ),
    ),
    (
        "Give/get a pearl necklace.",
        "Position",
        SWEET,
        (
            "A pearl necklace is when he finishes on his partner’s neck and chest, like a string of pearls. It’s a "
            "naughty, visual finish that’s a thrill to give and to receive.\n\n"
            "Tip: Keep a towel handy, and try it right after a titty-fuck for the full effect."
        ),
    ),
    (
        "Have a really deep penetrative sex session.",
        "Position",
        SWEET,
        (
            "Have sex in positions made for depth, like doggy style, legs over the shoulders, or the receiving "
            "partner on top. Slow, deep thrusts hit spots that shallow ones miss, and the feeling of being "
            "completely filled can be overwhelming in the best way.\n\n"
            "Tip: Go slowly at first, since hitting the cervix can hurt. Let the receiving partner control the depth "
            "until you find the sweet spot."
        ),
    ),
    (
        "Have anal sex.",
        "Position",
        SIZZLING,
        (
            "Try anal penetration, with a finger, a toy, a penis or a strap-on. With patience and plenty of lube, it "
            "can be intensely pleasurable, and for many couples it’s an exciting new frontier built on trust.\n\n"
            "Tip: Use lots of lube (the anus doesn’t make its own), go slowly and stop if it hurts. Never go from "
            "anal to vaginal without a fresh condom or washing up."
        ),
    ),
    (
        "Sit on his face.",
        "Position",
        SPICY,
        (
            "Straddle his face and lower yourself onto his mouth while he licks and kisses you. You control the "
            "angle, the pressure and the pace, and he gets the best seat in the house.\n\n"
            "Tip: Hold the headboard or a wall for balance, hover instead of putting your full weight on him, and "
            "agree on a tap signal for when he needs air."
        ),
    ),
    (
        "Spit roast.",
        "Position",
        SPICY,
        (
            "A spit roast is one partner being taken from both ends at once: in the mouth and from behind. With just "
            "the two of you, a dildo can stand in for the third person. It’s a raw, filthy fantasy about being "
            "completely taken.\n\n"
            "Tip: If a third person joins, agree on everything beforehand and use condoms. With a toy, a suction cup "
            "base makes it much easier."
        ),
    ),
    (
        "Swallow his load.",
        "Position",
        SPICY,
        (
            "At the end of a blowjob, let him finish in your mouth, and swallow. For many men it’s the ultimate "
            "finish, and for the giver it can be a powerful mix of control and devotion.\n\n"
            "Tip: Get tested together first, since oral sex can pass on infections. Taking him deeper as he finishes "
            "means less taste on your tongue."
        ),
    ),
    (
        "Try “Airlock” (DP + BJ).",
        "Position",
        SIZZLING,
        (
            "The “airlock” means every hole filled at once: vaginal, anal and oral. With just the two of you, toys "
            "fill in for the extra partners, so you can explore the fantasy without inviting anyone else.\n\n"
            "Tip: Use lots of lube, go slowly, and build up one toy at a time. If others join, agree on everything "
            "beforehand and use condoms."
        ),
    ),
    (
        "Try a finger in the butt.",
        "Position",
        SPICY,
        (
            "Slip a finger into your partner’s butt during sex or oral. It’s the gentlest way to try anal play, and "
            "the extra sensation, from all those nerve endings or the prostate, can make orgasms much more "
            "intense.\n\n"
            "Tip: Trim and file your nails, use plenty of lube and go slowly. Wait for your partner to relax before "
            "going any further."
        ),
    ),
    (
        "Try a sex position that uses gym equipment.",
        "Challenge",
        SWEET,
        (
            "Use a workout bench, an exercise ball or a pull-up bar to get into positions your bed can’t offer. It’s "
            "a playful way to put your home gym to better use, and the bounce and the angles can be surprisingly "
            "good.\n\n"
            "Tip: Stick to stable equipment at home, not the public gym, and test that it holds you both before you "
            "commit."
        ),
    ),
    (
        "Try a titty-fuck.",
        "Position",
        SPICY,
        (
            "He slides between his partner’s breasts while they press them together around him. It’s a visual, "
            "playful act that gives you both a great view, and it pairs well with a pearl necklace at the end.\n\n"
            "Tip: Use plenty of lube or oil, since dry skin chafes. Lying back with a pillow under the head keeps "
            "the receiver comfortable."
        ),
    ),
    (
        "Try consensual “non-consensual” play.",
        "Activity",
        SIZZLING,
        (
            "Consensual non-consent (CNC) is a role-play where one partner pretends to resist while the other takes "
            "control, all agreed on beforehand. It lets you explore a taboo fantasy of being overpowered, safely, "
            "with someone you trust completely.\n\n"
            "Tip: Talk through the scene and your limits first, and use a safeword that isn’t “no” or “stop”, since "
            "those might be part of the act. Plan aftercare too."
        ),
    ),
    (
        "Try deep-throating.",
        "Position",
        SIZZLING,
        (
            "Take your partner deep into your throat during oral sex. It takes practice and relaxation, and it’s as "
            "much about the giver’s skill and control as the receiver’s pleasure.\n\n"
            "Tip: Lie on your back with your head hanging off the bed to straighten your throat, breathe through "
            "your nose, and go at your own pace."
        ),
    ),
    (
        "Try double penetration.",
        "Position",
        SIZZLING,
        (
            "Double penetration means being filled in two places at once, usually vaginally and anally. For a "
            "couple, that means sex plus a dildo or a plug. The feeling of fullness is intense, and for many it’s an "
            "unforgettable kind of overload.\n\n"
            "Tip: Start small, use plenty of lube and go slowly. A butt plug is the easiest way to begin."
        ),
    ),
    (
        "Try edging for more powerful orgasms.",
        "Activity",
        SWEET,
        (
            "Edging means bringing yourself or your partner right to the brink of orgasm, then stopping before going "
            "over, again and again. Holding back builds up tension that makes the final orgasm much more "
            "powerful.\n\n"
            "Tip: Agree on a word, like “close”, so the person being edged can say when they’re near the edge."
        ),
    ),
    (
        "Try mutual masturbation.",
        "Activity",
        SIZZLING,
        (
            "Touch yourselves side by side or face to face, while you watch each other. It’s intimate and revealing: "
            "you get to see exactly how your partner likes to be touched, and watching can be very hot.\n\n"
            "Tip: Watch closely and take notes. What they do to themselves is a guide to what you can do to them."
        ),
    ),
    (
        "Try pegging.",
        "Position",
        SIZZLING,
        (
            "Pegging is when she wears a strap-on and penetrates him anally. It flips the usual roles: he gets to "
            "enjoy prostate stimulation, and she gets to experience being the one in charge in a whole new way.\n\n"
            "Tip: Start with fingers and a small toy, use lots of lube, and choose a slim, beginner-sized strap-on. "
            "Patience is everything."
        ),
    ),
    (
        "Do it in the Amazon sex position.",
        "Position",
        SWEET,
        (
            "In the Amazon, he lies on his back and pulls his knees toward his chest, while she squats or kneels "
            "over him and lowers herself onto him. It flips missionary on its head and puts her completely in "
            "control of the depth and the rhythm.\n\n"
            "Tip: Bending the wrong way can hurt him, so start slowly and let her move with care."
        ),
    ),
    (
        "Experiment with new oral sex positions.",
        "Position",
        SPICY,
        (
            "Break out of your usual oral routine with new positions: standing, kneeling, face-sitting, 69, or the "
            "receiver at the edge of the bed. Each one changes the angle, the pressure and the view.\n\n"
            "Tip: Comfort matters for the giver, so use pillows under knees, hips and heads."
        ),
    ),
    (
        "Explore tantric sex.",
        "Position",
        SWEET,
        (
            "Tantric sex is about slowing down and connecting: eye contact, breathing in sync and long, deliberate "
            "touch, with no rush to orgasm. It can make sex feel deeper and more intimate, and lead to longer, more "
            "intense orgasms.\n\n"
            "Tip: Set aside a whole evening without phones, and start by breathing together for a few minutes before "
            "you touch."
        ),
    ),
    (
        "Explore the joys of a good old-fashioned missionary position.",
        "Position",
        SWEET,
        (
            "Rediscover the original: face to face, bodies pressed together, kissing as you move. Missionary is "
            "popular for good reason: it’s intimate, comfortable and full of eye contact, and small tweaks can make "
            "it feel brand new.\n\n"
            "Tip: Slide a pillow under the receiver’s hips for a better angle, or try grinding instead of thrusting "
            "(the coital alignment technique)."
        ),
    ),
    (
        "Have sex doggy style.",
        "Position",
        SWEET,
        (
            "One partner on all fours, the other behind them. Doggy style allows deep penetration and a great view, "
            "has a primal feel, and leaves hands free to reach around.\n\n"
            "Tip: Have the receiver lower their chest to the bed to change the angle, and reach around to touch them "
            "while you thrust."
        ),
    ),
    (
        "Have sex in the cowgirl position.",
        "Position",
        SWEET,
        (
            "She straddles her partner, facing them, and rides. Cowgirl puts her in control of the angle, depth and "
            "speed, while her partner gets to enjoy the view with their hands free.\n\n"
            "Tip: Grinding back and forth often feels better than bouncing up and down, and it’s easier on the "
            "thighs."
        ),
    ),
    (
        "Have sex in the reverse cowgirl position.",
        "Position",
        SWEET,
        (
            "She straddles her partner facing their feet, and rides. It gives her a different angle and control over "
            "the pace, and her partner gets an unforgettable view from behind.\n\n"
            "Tip: Keep it slow and controlled, and don’t lift too high: a bad angle in this position can hurt him."
        ),
    ),
    (
        "Have standing sex.",
        "Position",
        SWEET,
        (
            "Have sex standing up: against a wall, a door or the kitchen counter. It feels urgent and passionate, as "
            "if you couldn’t wait to make it to the bed.\n\n"
            "Tip: Height differences make it tricky, so use a step, the stairs or a counter to even things out."
        ),
    ),
    (
        "Try 69-ing.",
        "Position",
        SWEET,
        (
            "Go down on each other at the same time, head to toe. Giving and receiving at once is a fun test of "
            "concentration and an exciting feedback loop: the better you do, the better you get.\n\n"
            "Tip: Lying on your sides is easier on the neck than one of you on top."
        ),
    ),
    (
        "Try a new position that neither of you has tried before.",
        "Position",
        SWEET,
        (
            "Find a position neither of you has ever done, and give it a try. It shakes up your routine, and even if "
            "it doesn’t work out, you’ll have something to laugh about together.\n\n"
            "Tip: Browse a book or a website together, and each pick one that looks fun."
        ),
    ),
    (
        "Try the “anvil” sex position.",
        "Position",
        SWEET,
        (
            "In the anvil, the receiving partner lies on their back with their legs pulled back toward their head, "
            "and the other leans in from above. It allows very deep penetration and a feeling of being completely "
            "taken.\n\n"
            "Tip: It’s intense and very deep, so start slowly, and let the receiving partner hold their legs to "
            "control the angle."
        ),
    ),
    (
        "Try the “coconut” move during cowgirl.",
        "Position",
        SWEET,
        (
            "While riding in cowgirl, roll your hips as if you were spelling the word “coconut” with them, letter by "
            "letter. It started as a joke online and became a viral challenge, but the mix of circles, curves and "
            "grinds can hit spots that bouncing misses.\n\n"
            "Tip: Slow down on the curvy letters, and don’t worry about spelling it right. Laughing is part of the "
            "fun."
        ),
    ),
    (
        "Try the Yab-Yum position.",
        "Position",
        SWEET,
        (
            "Yab-Yum is a tantric position: one partner sits cross-legged, and the other sits in their lap, facing "
            "them, legs wrapped around their waist. It’s more about closeness than thrusting: chests pressed "
            "together, eyes locked and breathing in sync.\n\n"
            "Tip: Sit on a firm pillow for support, and rock slowly instead of bouncing."
        ),
    ),
    (
        "Try all the Kama Sutra sex positions.",
        "Position",
        SWEET,
        (
            "The Kama Sutra is an ancient Indian text on love and pleasure, famous for its many sex positions. "
            "Working your way through them is a long-term adventure: some are easy, some are acrobatic, and all of "
            "them make for a good story.\n\n"
            "Tip: Get an illustrated guide and tick the positions off as you go."
        ),
    ),
    (
        "Add a mirror to the action.",
        "Toys",
        SWEET,
        (
            "Have sex in front of a mirror so you can watch yourselves. Seeing your bodies together from a new angle "
            "is a turn-on, and it lets you see your partner’s face even when you’re behind them.\n\n"
            "Tip: A full-length mirror leaned against the wall or a closet door works perfectly. Dim the lights for "
            "a flattering glow."
        ),
    ),
    (
        "Blend food and sex.",
        "Toys",
        SWEET,
        (
            "Bring food into the bedroom: whipped cream, chocolate sauce, strawberries, honey. Licking it off each "
            "other’s bodies is playful, sensual and a little messy, which is half the fun.\n\n"
            "Tip: Keep sugary foods away from the vagina, since they can cause yeast infections, and put a towel "
            "down first."
        ),
    ),
    (
        "Get wet with a body shot.",
        "Activity",
        SWEET,
        (
            "Take a shot off your partner’s body: lick the salt from their neck, drink from their belly button and "
            "take the lime from their lips. It’s a flirty party game that turns your partner’s body into a "
            "playground.\n\n"
            "Tip: Drink responsibly, and keep alcohol away from sensitive areas: it stings."
        ),
    ),
    (
        "Use a butt plug.",
        "Toys",
        SIZZLING,
        (
            "A butt plug is a toy that sits inside the anus, with a flared base that keeps it in place. Wearing one "
            "adds a feeling of fullness and can make orgasms more intense, and it’s a great first step into anal "
            "play.\n\n"
            "Tip: Only use plugs with a flared base, start small and use plenty of lube. Silicone toys need "
            "water-based lube."
        ),
    ),
    (
        "Use a cock ring.",
        "Toys",
        SWEET,
        (
            "A cock ring fits around the base of the penis and slows the blood flow out, making erections firmer and "
            "longer-lasting. Many come with a vibrator, which adds stimulation for both partners during sex.\n\n"
            "Tip: Start with a stretchy silicone ring, and take it off after 20 to 30 minutes, or right away if it "
            "feels numb or cold."
        ),
    ),
    (
        "Use a remote-controlled sex toy with a partner (in public?).",
        "Toys",
        SWEET,
        (
            "One partner wears a remote-controlled vibrator, and the other holds the remote, or the app. They decide "
            "when it buzzes and how hard, which makes it an amazing tease at home, and an even better one in "
            "public.\n\n"
            "Tip: Charge it and test the range or the connection before you go out, and choose a quiet model."
        ),
    ),
    (
        "Use a sex pillow.",
        "Toys",
        SWEET,
        (
            "A sex pillow is a firm wedge or ramp that lifts the hips, making new angles and deeper positions "
            "comfortable. It takes the strain off knees, backs and arms, so you can focus on the pleasure.\n\n"
            "Tip: No sex pillow yet? A firm pillow or a folded blanket under the hips gives you an idea."
        ),
    ),
    (
        "Use a sex toy with a partner.",
        "Toys",
        SWEET,
        (
            "Bring a toy into your sex life, whether a vibrator, a dildo, a wand or a stroker, and use it on each "
            "other. Toys add new sensations and help both partners finish. Think of them as a teammate, not a "
            "replacement.\n\n"
            "Tip: Pick a toy together, and use water-based lube with silicone toys."
        ),
    ),
    (
        "Use nipple clamps.",
        "Toys",
        SWEET,
        (
            "Nipple clamps pinch the nipples for a mix of pressure, pain and pleasure. They heighten sensitivity, "
            "especially when they come off, and they’re a great introduction to sensation play.\n\n"
            "Tip: Start with adjustable clamps on a light setting, and limit wear to 10 to 15 minutes. Taking them "
            "off hurts more than putting them on, so go slowly."
        ),
    ),
    (
        "Become fluent in dirty talk.",
        "Activity",
        SIZZLING,
        (
            "Learn to say exactly what you want, what you’re doing and how it feels, out loud and without blushing. "
            "Dirty talk turns up the heat for both of you, and it doubles as great communication in bed.\n\n"
            "Tip: Start by describing what you feel (“that feels amazing”), then work up to what you want and what "
            "you’re about to do."
        ),
    ),
    (
        "Do a striptease.",
        "Activity",
        SPICY,
        (
            "Put on some music and slowly take off your clothes for your partner, one piece at a time. A striptease "
            "is a confidence boost for the performer and an irresistible tease for the one watching.\n\n"
            "Tip: Choose a song you know well, wear clothes that come off easily, and remember that confidence is "
            "sexier than perfect moves."
        ),
    ),
    (
        "Do the “anything but penetration” challenge.",
        "Challenge",
        SWEET,
        (
            "Have a whole session where everything is allowed except penetration. Taking it off the table pushes you "
            "to get creative with hands, mouths, toys and bodies, and you’ll likely discover new favorites.\n\n"
            "Tip: Use the extra time on spots that usually get rushed: necks, inner thighs, backs and ears."
        ),
    ),
    (
        "Give her a creampie; she decides where she wants it.",
        "Position",
        SWEET,
        (
            "He finishes inside her, wherever she chooses. Letting her choose puts her in charge of the finale, and "
            "for many the feeling of being filled is a real turn-on.\n\n"
            "Tip: Talk about birth control and get tested together first, since this means no condom."
        ),
    ),
    (
        "Give her a cumshot; she decides where she wants it.",
        "Position",
        SWEET,
        (
            "He finishes on her, and she chooses where: her stomach, her back, her chest or somewhere more daring. "
            "Letting her choose puts her in charge of the finale and makes it a shared, visual moment.\n\n"
            "Tip: Keep a towel handy, and keep it away from the eyes."
        ),
    ),
    (
        "Have a wake-up session.",
        "Activity",
        SWEET,
        (
            "Wake your partner up with kisses, touches or oral sex, and start the day the best way possible. Morning "
            "sex is relaxed, cozy and full of energy, and it puts you both in a great mood for the rest of the "
            "day.\n\n"
            "Tip: Ask first. Agree the night before that waking up this way is a yes, since nobody can consent while "
            "they’re asleep."
        ),
    ),
    (
        "Have multiple orgasms in one sex session.",
        "Challenge",
        SWEET,
        (
            "Aim for more than one orgasm in a single session, for one of you or both. It takes patience, varied "
            "stimulation and good communication, and it can turn an ordinary night into a marathon of pleasure.\n\n"
            "Tip: Switch up the stimulation after the first orgasm, since sensitivity changes, and take short breaks "
            "for water and cuddles."
        ),
    ),
    (
        "Have rough sex.",
        "Activity",
        SPICY,
        (
            "Let go of gentleness: grabbing, pinning, hair pulling, harder thrusting and a lot of passion. Rough sex "
            "can feel raw and primal, and it’s a great release for both partners when it’s fully agreed on.\n\n"
            "Tip: Agree on what “rough” means for each of you, use a safeword, and check in afterward."
        ),
    ),
    (
        "Have sex with (most of) your clothes on.",
        "Challenge",
        SWEET,
        (
            "Have sex while keeping most of your clothes on: push aside or unzip only what you need. It feels urgent "
            "and spontaneous, like you couldn’t wait, and the half-dressed look is a turn-on of its own.\n\n"
            "Tip: Skirts, dresses and easy zippers help. Plan your outfits!"
        ),
    ),
    (
        "Look into each other’s eyes when cumming. Bonus: cum at the same time.",
        "Challenge",
        SWEET,
        (
            "Keep eye contact as you orgasm instead of closing your eyes or looking away. It’s one of the most "
            "intimate things you can share, and it makes you feel deeply connected in your most vulnerable "
            "moment.\n\n"
            "Tip: Face-to-face positions like missionary or cowgirl make this much easier."
        ),
    ),
    (
        "No-kissing session.",
        "Challenge",
        SPICY,
        (
            "Have a whole session where kissing on the lips is off-limits. Taking away something so natural builds "
            "tension and pushes you to find other ways to show desire, and it makes the first kiss afterward even "
            "better.\n\n"
            "Tip: Keep your lips busy elsewhere: necks, shoulders and thighs are still fair game."
        ),
    ),
    (
        "One partner rips the other’s clothes off.",
        "Activity",
        SWEET,
        (
            "Let passion take over: one partner tears the other’s clothes off, buttons flying. It’s a dramatic show "
            "of desire that feels straight out of a movie.\n\n"
            "Tip: Pick a shirt you don’t mind losing, like a thrift-store find, and agree on which clothes are fair "
            "game."
        ),
    ),
    (
        "Sex right after the gym.",
        "Challenge",
        SWEET,
        (
            "Skip the shower and go straight from your workout to each other. Your blood is pumping, your endorphins "
            "are high, and there’s something primal about sweaty, flushed skin.\n\n"
            "Tip: Drink plenty of water first. If sweat isn’t your thing, a quick rinse together can be part of the "
            "fun."
        ),
    ),
    (
        "Stay in bed with your partner all day long.",
        "Activity",
        SWEET,
        (
            "Spend an entire day in bed together: sleep in, have breakfast in bed, watch movies, nap, and have sex "
            "as often as you like. It’s a rare chance to slow down and reconnect, with nowhere to be but with each "
            "other.\n\n"
            "Tip: Stock up on snacks and water the night before, and turn off your notifications."
        ),
    ),
    (
        "Surprise each other with a new piece of lingerie or a new sex toy.",
        "Toys",
        SWEET,
        (
            "Pick out a gift for your partner, like lingerie, sexy underwear or a new toy, and surprise them with "
            "it. It shows you’ve been thinking about them, and the unwrapping almost always turns into a test "
            "run.\n\n"
            "Tip: Sneak a peek at their sizes and favorite colors beforehand, or choose a toy you can both enjoy."
        ),
    ),
    (
        "Try out new lingerie or underwear sets.",
        "Toys",
        SWEET,
        (
            "Shop for new lingerie or underwear, together or as a surprise, and try it on for each other. A new look "
            "can boost your confidence and make your partner see you with fresh eyes.\n\n"
            "Tip: Comfort is sexy too, so choose something that fits well. Everyone looks better when they feel good."
        ),
    ),
    (
        "Wear sexy costumes.",
        "Toys",
        SWEET,
        (
            "Dress up in sexy costumes, like a nurse, a pirate, a cop or a superhero, and let the outfits set the "
            "mood. Costumes make it easy to slip into a role, and they add a playful touch to the bedroom.\n\n"
            "Tip: Pick costumes that come off easily, and pair them with a role-play scenario for the full "
            "experience."
        ),
    ),
]


# Each starter wish's three levels, from a gentle start to the kinkiest version, keyed by the
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
        "Dressing up is how it started, undressing each other is how it ends. Bonus if this happened before you "
        "made it back home.",
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
        "You made it, congrats! Look around and both of you should share your observations. Your likes and dislikes.",
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
        "You and your partner have sex. The 3rd person can only watch and tell the couple what to do to each other, "
        "but remains an observer.",
        "Include the 3rd person, they also get to have fun. Bonus: all 3 were able to finish.",
    ],
    "have mind-blowing vacation sex.": [
        "You have sex while you are on vacation, home is fine.",
        "You have sex during a vacation somewhere else. Frankly, anywhere else but home.",
        "You have sex somewhere far away. Maybe you had to take a plane to get there. Maybe at a resort, a cruise. "
        "Bonus: in a different country.",
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
    "make a sex tape.": [
        "Start with sound only: record a session with your phone’s voice recorder, then listen back together.",
        "Prop up the camera and film a whole session from start to finish. Play to the camera, and try a POV shot "
        "or two.",
        "Watch your tape together and let it play while you go for round two. Bonus: film that one too.",
    ],
    "next time your partner receives a telemarketer’s call, he/she cannot hang up!": [
        "Kiss and touch them all over while they’re on the call. They have to sound completely normal.",
        "Go down on them while they keep the conversation going. No muting, no hanging up.",
        "They finish before the call ends. Bonus: they still politely turn down whatever was on offer.",
    ],
    "record yourself being naughty in a public setting and send it to your partner.": [
        "Flash a little on camera, like lifting your shirt in a changing room, and hit send.",
        "Touch yourself on camera somewhere public but out of sight, like a fitting room, and send it right away.",
        "Film the two of you doing something naughty together in public, without anyone noticing.",
    ],
    "recreate a porno video (pick at random, or already have one in mind?).": [
        "Act out the setup: the cheesy lines, the outfits, the pizza delivery. Laughing is allowed.",
        "Recreate the scene’s main positions in order, as close to the video as you can.",
        "Recreate the whole scene, finish included. Bonus: film your version and compare.",
    ],
    "roleplay (play out a fantasy, or explore a theme with it).": [
        "Agree on a scenario and stay in character while you flirt, before anything gets physical.",
        "Dress the part, with costumes or props, and play the scene all the way to the bedroom.",
        "Play out a scene that pushes your comfort zone, like a power dynamic or a taboo, and stay in character to "
        "the end.",
    ],
    "send your partner a surprise dirty picture.": [
        "Send a suggestive photo with your clothes on: a low neckline, an open shirt, a look that says it all.",
        "Send a photo in your underwear or lingerie, showing a little more skin than usual.",
        "Send a full nude, with a message saying what you want to do when you see them.",
    ],
    "take sexy nudes together.": [
        "Take sexy shots in lingerie or underwear, playing with poses, angles and light.",
        "Go fully nude: take turns behind the camera and direct each other’s poses.",
        "Use a timer or a tripod to capture the two of you together, mid-action.",
    ],
    "try a “naked” chef night (cook a meal together with little to no clothes on).": [
        "Cook in your underwear or in nothing but an apron. Flirting with your sous-chef is encouraged.",
        "Cook completely naked, and every time a step of the recipe is done, kiss each other somewhere new.",
        "Dessert comes first: turn off the stove and have sex right there in the kitchen before you sit down to eat.",
    ],
    "try a new sex position every day for a week.": [
        "Try three new positions over the week, whenever the mood strikes.",
        "A new position every day for seven days straight, no skipping.",
        "Seven days, seven positions, and you both finish every time. Bonus: one of them is truly acrobatic.",
    ],
    "try swinging.": [
        "Same-room play: have sex with your own partner while another couple does the same nearby.",
        "Soft swap: kiss and touch the other couple, but keep intercourse with your own partner.",
        "Full swap: each of you has sex with someone from the other couple. Check in before, during and after.",
    ],
    "turn your partner on with your sexting skills.": [
        "Send a flirty message that hints at what you want later, and keep them guessing.",
        "Describe in detail what you’ll do to them tonight, one message at a time.",
        "Keep it going until one of you gives in and touches themselves, or races home to finish what you started.",
    ],
    "use your mouth to put a condom on him.": [
        "Practice on a banana or a toy until you can roll it on without using your hands.",
        "Do it for real, hands-free, as part of foreplay. Eye contact encouraged.",
        "Put it on hands-free, keep teasing with your mouth, then climb on and put it to use right away.",
    ],
    "vacation at a sex resort.": [
        "Spend your days by the pool and soak up the atmosphere. Bonus: go clothing-optional for an afternoon.",
        "Join a theme night or a party, and see where the evening takes you.",
        "Play in one of the resort’s playrooms, or with other guests if you’re both up for it.",
    ],
    "watch porn with your partner.": [
        "Watch a scene side by side, and talk about what you like and what you don’t.",
        "Touch each other while you watch, but no sex until the video ends.",
        "Have sex while it plays, and try to finish when the performers do.",
    ],
    "whisper dirty talk to each other in public.": [
        "Whisper a compliment about their body, and one thing you’d like to do to them later.",
        "Describe, in detail, what you’ll do once you’re alone, while they try to keep a straight face.",
        "Keep it up until one of you cracks and drags the other somewhere private.",
    ],
    "collar and leash.": [
        "Wear the collar during sex, as a symbol of who’s in charge tonight.",
        "Add the leash: your partner leads you around the house and into the bedroom.",
        "Stay collared for a whole evening, follow every order, and crawl when you’re told to.",
    ],
    "be a dominant mistress/master of your partner for a night.": [
        "Give the orders for the evening: what they wear, where they sit and what they do to you.",
        "Add rules and punishments: they ask permission for everything, and every broken rule earns a spanking.",
        "Use restraints and toys, and take full control over when, and if, they get to finish.",
    ],
    "be a submissive sex slave to your partner for a night.": [
        "Obey every request for the evening, and call your partner by the title they choose.",
        "Serve them: undress them, pamper them and pleasure them however they demand.",
        "Let them tie you up and use you as they please, within your limits, and finish only when they say so.",
    ],
    "bound and blindfolded.": [
        "Blindfold only. Keep your hands to yourself while your partner teases you with their fingers, lips and "
        "breath.",
        "Blindfolded with your wrists tied (a scarf or necktie works). Your partner decides what happens next, and "
        "you never know what’s coming.",
        "Wrists and ankles tied, eyes covered. Your partner adds surprises like ice, a feather or a vibrator, and "
        "decides when you get to finish.",
    ],
    "breath play — safely.": [
        "Rest a hand on your partner’s throat with no pressure at all. Feeling held there is often the whole thrill.",
        "Control their breathing with words: tell them when to breathe in, when to hold it and when to let go.",
        "Have them hold their breath as they reach the edge, and let it all out as they finish.",
    ],
    "chair ties.": [
        "Tie their wrists to the chair and give them a slow lap dance they can’t touch.",
        "Tie their wrists and ankles, then tease them with your hands and mouth until they beg.",
        "Keep them tied up and have sex right there in the chair.",
    ],
    "channel your dominant side in the bedroom.": [
        "Initiate sex and take charge of the pace and positions from start to finish.",
        "Give clear commands, like “lie down” or “don’t move”, and pin their wrists while you take what you want.",
        "Add some power play: blindfold or tie them, and make them ask before they can finish.",
    ],
    "channel your submissive side in the bedroom.": [
        "Let your partner decide everything for one session, and follow their lead without suggesting anything.",
        "Obey their commands, ask permission before you touch them, and thank them when they let you.",
        "Let them restrain or blindfold you, and give up control over when you get to finish.",
    ],
    "dom/sub switch it up!": [
        "Switch who leads halfway through a session: the first one in charge sets the pace, then hands it over.",
        "Each of you gets a full session as the dominant, with the other following every order.",
        "Switch mid-scene on a code word, and the new dom gets to pay back every tease.",
    ],
    "gagged and bound.": [
        "Start soft: tie their wrists and cover their mouth with your hand or a scarf while you tease them.",
        "Use a real gag, like a ball or bit gag, with wrists and ankles tied, for a short scene.",
        "Fully bound and gagged for a longer scene, while you use toys and take your time.",
    ],
    "handcuffs.": [
        "Cuff their wrists in front of them, and let them watch as you tease them.",
        "Cuff their wrists behind their back or to the bed, so they can’t touch you at all.",
        "Cuff them to the bed and keep them there until you’ve both finished at least once.",
    ],
    "hogtie experience.": [
        "Tie your partner’s wrists behind their back and their ankles together, without joining the two.",
        "Connect the wrists and ankles loosely, leaving some slack, for a few minutes.",
        "A full hogtie, while you tease and touch them until they squirm.",
    ],
    "kinky dress-up (fishnets, harness, corset, cat ears, collar, etc.).": [
        "Wear one kinky piece under your everyday clothes, and reveal it at the end of the day.",
        "Dress up in a full kinky outfit and wear it for an entire evening at home.",
        "Wear your kinky outfit out, to a fetish night or under a long coat, and keep it on during sex.",
    ],
    "light hair pulling and biting.": [
        "Run your fingers through their hair with a gentle tug, and nibble their ears and neck.",
        "Grab a firm handful of hair during sex, and bite their shoulders, chest or inner thighs.",
        "Use your grip on their hair to guide them where you want them, and leave a love bite only you two will see.",
    ],
    "light spanking.": [
        "A few playful smacks on the butt during sex, just enough to make them gasp.",
        "Bend them over your knee for a proper spanking, with a warm-up and a count.",
        "Use a paddle or a firm hand until their cheeks turn pink, as a reward or a punishment.",
    ],
    "massage (everything but between the legs… make them wait, then finish them off with a glorious happy ending).": [
        "Massage everywhere but between their legs for at least 20 minutes, no matter how much they squirm.",
        "Brush closer and closer, inner thighs included, without ever touching, until they beg.",
        "Finish them off with a glorious happy ending, then switch places.",
    ],
    "sensual restraint with scarves or a silky necktie.": [
        "Loosely tie their wrists together in front of them, and kiss them all over.",
        "Tie their wrists to the headboard and use a second scarf as a blindfold.",
        "Tie their wrists and ankles to the bed, and tease them slowly until they finish.",
    ],
    "shibari rope harness.": [
        "Learn a simple chest harness and tie it on your partner, over their clothes to start.",
        "Tie a full body harness on bare skin, and take photos of your work.",
        "Have sex while your partner wears the harness, using the ropes to hold and guide them.",
    ],
    "spread-eagle bed bondage.": [
        "Tie just their wrists to the corners of the bed, and explore them with your hands and mouth.",
        "Tie wrists and ankles, spread-eagle, and add a blindfold.",
        "Spread-eagle and blindfolded, while you use a toy on them until they finish more than once.",
    ],
    "tell your partner, “do whatever you want to me.” just remember to use a safeword!": [
        "Let them take over for a set time, like 15 minutes, then carry on as usual.",
        "Hand over a whole session: they decide everything from start to finish.",
        "Give them free rein for a whole night, including toys, restraints and anything else on their wish list.",
    ],
    "temperature play (ice cubes, candle wax, etc.).": [
        "Trail an ice cube over their body, followed by your warm mouth.",
        "Drip warm wax from a massage candle on their back or chest, from high enough that it cools a little first.",
        "Blindfold them and alternate ice and wax, so they never know which is coming next.",
    ],
    "use safewords for practice.": [
        "Agree on your safewords, and say “yellow” or “red” at least once during regular sex, just to practice.",
        "Check in during a spicier session by asking “What’s your color?”, and adjust to the answer.",
        "Try something new and intense, like restraints or spanking, trusting your safewords to keep you both safe.",
    ],
    "use your nails on your partner’s back during sex.": [
        "Lightly trace your nails over their back, arms and thighs during foreplay.",
        "Dig in and drag your nails down their back as things heat up.",
        "Leave marks they’ll still feel the next day, as a reminder of the night.",
    ],
    "have sex in a car.": [
        "Make out and get handsy in a parked car, like teenagers.",
        "Have sex in the back seat, in your own garage or driveway.",
        "Have sex in a parked car somewhere out in the world, like a quiet lookout or an empty lot.",
    ],
    "have sex in public — sort of.": [
        "Have sex by an open window or on a dark balcony, where you could be seen but aren’t.",
        "Have sex outdoors somewhere private, like your backyard or a secluded campsite.",
        "Have sex somewhere that feels truly public but hidden, like a fitting room or a rooftop at night.",
    ],
    "have sex in the shower.": [
        "Shower together and wash each other slowly, from head to toe.",
        "Use your hands or mouths on each other under the water.",
        "Have sex standing up in the shower, with one of you pressed against the wall.",
    ],
    "have sex on a camping trip.": [
        "Fool around in your sleeping bag, as quietly as you can.",
        "Have sex in your tent while other campers are nearby.",
        "Leave the tent behind and have sex outside, under the stars.",
    ],
    "have sex on a desk.": [
        "Make out at the desk, with one of you sitting on it and the other standing between their legs.",
        "Have sex on the desk, with one of you sitting or lying back on it.",
        "Role-play the office fantasy, boss and employee, dressed for work, and finish on the desk.",
    ],
    "have sex on the beach.": [
        "Make out on a blanket on the beach at sunset.",
        "Get each other off on a secluded beach, under a blanket or in the water.",
        "Go all the way on the beach, under the stars.",
    ],
    "have sex on the couch.": [
        "Make out on the couch during a movie, and let your hands wander.",
        "Have sex on the couch, with one of you sitting and the other straddling them.",
        "Use every part of the couch, the armrest, the back and the cushions, until you’ve both finished.",
    ],
    "have sex outside.": [
        "Make out and touch each other outside, in your backyard or on a balcony.",
        "Have sex outdoors somewhere private, like your backyard at night.",
        "Go further afield: have sex out in nature, in the woods or a secluded field, in broad daylight.",
    ],
    "hook up in a hot tub.": [
        "Get in together and kiss and touch under the water.",
        "Get each other off underwater, with your hands or the jets.",
        "Have sex in the hot tub, sitting on the edge or straddling on the bench.",
    ],
    "take a shower together and focus solely on intense touch and stimulation.": [
        "Wash each other from head to toe, taking your time on every part.",
        "Focus on the most sensitive spots with soapy hands and the showerhead, but no sex.",
        "Keep touching each other until you both climax, with your hands or the showerhead only.",
    ],
    "play a sex game.": [
        "Play a flirty question-and-answer game, like truth or dare, with your clothes on.",
        "Play a game where the loser of each round removes a piece of clothing or takes a dare.",
        "Play until someone wins, and the winner gets to do whatever they want to the loser.",
    ],
    "play a strip card game, with consequences for losing.": [
        "Play strip poker, or any game, until one of you is down to their underwear.",
        "Play until someone is completely naked, then the winner picks a consequence, like a lap dance or a massage.",
        "Once naked, every lost hand means a sexual dare chosen by the winner, until someone gives in.",
    ],
    "play with sex dice.": [
        "Roll the action and body part dice and follow them: kiss, lick, touch.",
        "Add a third die for positions or places, and follow wherever it leads.",
        "Make your own dice with your kinkiest ideas, and roll until someone finishes.",
    ],
    "bring your perineum into play.": [
        "Gently massage your partner’s perineum with your fingers during oral or a handjob.",
        "Use your tongue on it, or press on it firmly as they’re about to finish.",
        "Use a vibrator on it during sex, or let it lead into anal play.",
    ],
    "chair sex.": [
        "Give your partner a lap dance while they sit in the chair, hands off.",
        "Have sex in the chair facing each other, with one of you seated and the other straddling.",
        "Try every chair position: facing away, legs over the armrests, then bent over the back of the chair.",
    ],
    "explore squirting.": [
        "Explore the G-spot with your fingers, with no expectations at all.",
        "Use a come-hither motion or a G-spot toy, with firm, steady pressure, and let it build.",
        "Squirt! Bonus: more than once in the same session.",
    ],
    "fuck her mouth.": [
        "She guides the pace with her hands on your hips while you thrust gently.",
        "Hold her head and set the pace yourself, watching her reactions closely.",
        "With her head hanging off the edge of the bed for a deeper angle, go until you finish.",
    ],
    "give and/or receive a rim job.": [
        "Kiss and lick your way around their butt cheeks and lower back, getting closer each time.",
        "Give a rim job with a dental dam, or right after a shower together.",
        "Rim them while you stroke or touch them, until they finish.",
    ],
    "give your partner a blended orgasm.": [
        "Stimulate both spots at the same time, without aiming to finish.",
        "Use a dual toy, like a rabbit vibrator or a prostate massager, during sex.",
        "Bring your partner to a blended orgasm. Bonus: they have more than one.",
    ],
    "give/get a facial.": [
        "Finish on your partner’s chest or neck, close to their face.",
        "Finish on their chin or cheeks, avoiding the eyes.",
        "A full facial, while they look up at you.",
    ],
    "give/get a pearl necklace.": [
        "Finish on your partner’s stomach or lower chest.",
        "Give them a proper pearl necklace, across the chest and neck.",
        "End a titty-fuck with a pearl necklace, while they watch you.",
    ],
    "have a really deep penetrative sex session.": [
        "Take it slow and deep in missionary, with a pillow under their hips.",
        "Go deeper in doggy style, or with their legs over your shoulders.",
        "Pull their knees up to their chest for the deepest angle, and go until you both finish.",
    ],
    "have anal sex.": [
        "Start with a lubed finger or a small toy, during oral or while you touch them.",
        "Try just the tip, going slowly and letting the receiving partner control the pace.",
        "Have full anal sex, with plenty of lube, in a position they choose.",
    ],
    "sit on his face.": [
        "Kneel over his face and hover, holding the headboard while he licks and kisses you.",
        "Lower yourself fully and grind on his face, setting the pace and pressure yourself.",
        "Ride his face until you finish. Bonus: lean forward into a 69.",
    ],
    "spit roast.": [
        "Have sex from behind while they suck on a dildo, as if a third person were there.",
        "Switch ends: they go down on you while a suction-cup dildo on the wall fills them from behind.",
        "Invite a third person to make it real, if you’re both into it.",
    ],
    "swallow his load.": [
        "Let him finish in your mouth, then spit or swallow, your choice.",
        "Swallow every drop.",
        "Swallow it all while looking him in the eyes, then show him your empty mouth.",
    ],
    "try “airlock” (dp + bj).": [
        "Fill two at once: have sex while your partner sucks on a dildo or wears a plug.",
        "Fill all three, with you inside them, a dildo or plug, and a toy for their mouth.",
        "Make it real with more partners, if you’re all into it and everything is agreed beforehand.",
    ],
    "try a finger in the butt.": [
        "Circle the outside with a lubed fingertip during oral or sex, without going in.",
        "Slide one finger in slowly while you go down on them or have sex.",
        "Use a finger or two to make them finish. For him, curl it toward his belly to find the prostate.",
    ],
    "try a sex position that uses gym equipment.": [
        "Make out and touch each other on a workout bench or a yoga mat.",
        "Have sex on a weight bench or an exercise ball, using it for support and bounce.",
        "Try a position that takes strength, like holding your partner up against a pull-up bar or a squat rack.",
    ],
    "try a titty-fuck.": [
        "Lube up and slide between their breasts while they press them together.",
        "Have them lie back while you straddle them and set the pace.",
        "Let them lick the tip on every stroke, until you finish on their chest.",
    ],
    "try consensual “non-consensual” play.": [
        "Talk through the fantasy in detail: what happens, what’s off-limits, and your safeword.",
        "Play a light version: a playful struggle, pinned wrists, and pretend reluctance.",
        "Play out the full scene you agreed on, staying in character to the end, then take time for aftercare.",
    ],
    "try deep-throating.": [
        "Take them a little deeper each time, at your own pace, with a hand at the base for control.",
        "Lie with your head off the edge of the bed and take them deeper, breathing through your nose.",
        "Take them all the way down and hold it there for a few seconds.",
    ],
    "try double penetration.": [
        "Have sex while they wear a small butt plug.",
        "Have sex while you use a dildo in the other hole.",
        "Go bigger with a larger toy or a double strap-on, or with a third person if you’re both into it.",
    ],
    "try edging for more powerful orgasms.": [
        "Edge once: stop just before the orgasm, wait a minute, then finish.",
        "Edge three times before letting them finish.",
        "Edge them for 30 minutes or more, and they only finish when you say so.",
    ],
    "try mutual masturbation.": [
        "Touch yourselves under the sheets, side by side, while you kiss.",
        "Sit across from each other with the lights on, and watch each other.",
        "Bring yourselves to orgasm while you watch. Bonus: finish at the same time.",
    ],
    "try pegging.": [
        "Explore with a lubed finger or a small toy while you go down on him.",
        "Strap on a small dildo and try gentle, shallow penetration, letting him set the pace.",
        "Have full pegging sex, in whatever position he likes, until he finishes.",
    ],
    "do it in the amazon sex position.": [
        "Try the position slowly, with him holding his knees and her steadying herself on them.",
        "She sets the rhythm and takes control, with his hands on her hips.",
        "She stays in charge until you both finish, and decides when he gets to.",
    ],
    "experiment with new oral sex positions.": [
        "Try oral with the receiver at the edge of the bed and the giver kneeling.",
        "Try two new positions in one session, like standing up or face-sitting.",
        "Try a bold one, like the receiver upside down on the couch, and keep going until they finish.",
    ],
    "explore tantric sex.": [
        "Sit facing each other, eyes locked, and breathe together for five minutes before touching.",
        "Spend an hour exploring each other’s bodies slowly, without rushing toward orgasm.",
        "Have slow tantric sex in the Yab-Yum position, holding off your orgasms as long as you can.",
    ],
    "explore the joys of a good old-fashioned missionary position.": [
        "Take it slow in missionary, with lots of kissing and eye contact.",
        "Try a variation: a pillow under the hips, legs wrapped around the waist, or ankles on the shoulders.",
        "Pin their wrists above their head as you go, and don’t stop until you both finish.",
    ],
    "have sex doggy style.": [
        "Try classic doggy style on the bed, slow and steady.",
        "Add a reach-around, and grab their hips or hair as you go faster.",
        "Do it in front of a mirror or bent over a table, rougher and faster, until you both finish.",
    ],
    "have sex in the cowgirl position.": [
        "Ride slowly, leaning forward to kiss them.",
        "Sit up and find the angle that feels best, while their hands roam all over you.",
        "Ride until you finish, then keep going until they do.",
    ],
    "have sex in the reverse cowgirl position.": [
        "Try it slowly, with your hands on their thighs for balance.",
        "Lean forward to change the angle, and let them grab your hips.",
        "Lean back against their chest and touch yourself while you ride, until you finish.",
    ],
    "have standing sex.": [
        "Have sex standing up from behind, with the front partner leaning on a wall or table.",
        "Face to face against a wall, with one leg raised around your partner’s waist.",
        "Lift your partner up against the wall, with their legs wrapped around you.",
    ],
    "try 69-ing.": [
        "Try it lying on your sides, taking turns if it’s hard to focus on both.",
        "Try the classic version, one on top, until one of you finishes.",
        "Keep going until you both finish. Bonus: at the same time.",
    ],
    "try a new position that neither of you has tried before.": [
        "Pick a new position together and try it, even if only for a minute.",
        "Make it work long enough for one of you to finish.",
        "Pick the most acrobatic one you can find, and make it work until you both finish.",
    ],
    "try the “anvil” sex position.": [
        "Start with their legs over your shoulders, a gentler version of the anvil.",
        "Pull their knees back toward their chest for the full anvil, going slowly.",
        "Go deeper and faster in the anvil until you both finish.",
    ],
    "try the “coconut” move during cowgirl.": [
        "Spell “coconut” once, slowly, while your partner tries to guess the letters.",
        "Spell it again and again, faster, and linger on the letters that feel best.",
        "Keep spelling until one of you finishes. Bonus: spell your partner’s name next.",
    ],
    "try the yab-yum position.": [
        "Sit in Yab-Yum, clothes on or off, and breathe together while you kiss.",
        "Have sex in Yab-Yum, rocking slowly and keeping eye contact.",
        "Stay in Yab-Yum until you both finish, without breaking eye contact.",
    ],
    "try all the kama sutra sex positions.": [
        "Try five positions from the Kama Sutra.",
        "Try twenty, including a few acrobatic ones.",
        "Try them all. Bonus: find a favorite you’d never have discovered otherwise.",
    ],
    "add a mirror to the action.": [
        "Undress each other in front of a mirror, and watch yourselves kiss and touch.",
        "Have sex in front of the mirror, with one of you watching the reflection.",
        "Have sex from behind facing the mirror, keeping eye contact in the reflection until you finish.",
    ],
    "blend food and sex.": [
        "Blindfold your partner and feed them something sweet, with kisses between bites.",
        "Lick whipped cream or chocolate off each other’s bodies.",
        "Turn your partner into a dessert plate, and eat every bite off them.",
    ],
    "get wet with a body shot.": [
        "Do the classic: salt on the neck, the shot, and a lime between their lips.",
        "Pour the shot somewhere more daring, like their chest or the small of their back.",
        "Take body shots from wherever you dare, and skip the lime: their lips are the chaser.",
    ],
    "use a butt plug.": [
        "Insert a small, well-lubed plug during foreplay, then take it out.",
        "Wear the plug during sex.",
        "Wear it for a while before sex, even out of the house, as a secret only the two of you share.",
    ],
    "use a cock ring.": [
        "Try a stretchy ring during a handjob or oral.",
        "Wear it during sex and see how long you last.",
        "Use a vibrating ring so you both feel it, and hold off until you can’t anymore.",
    ],
    "use a remote-controlled sex toy with a partner (in public?).": [
        "Use it at home: one wears it while the other teases them from across the room.",
        "Wear it out to dinner, and keep a straight face while your partner plays with the remote.",
        "Wear it somewhere busy, like a party, and see if your partner can make you finish without anyone noticing.",
    ],
    "use a sex pillow.": [
        "Use it under the hips in missionary for a better angle.",
        "Try it for doggy style or oral, and find your favorite angle.",
        "Combine it with toys or restraints for your most adventurous session yet.",
    ],
    "use a sex toy with a partner.": [
        "Use a vibrator on each other during foreplay.",
        "Use the toy during sex, adding to what you’re already doing.",
        "Let your partner use the toy on you until you finish, more than once.",
    ],
    "use nipple clamps.": [
        "Try adjustable clamps on the lightest setting for a few minutes.",
        "Wear them during sex, and give the chain a gentle tug now and then.",
        "Tighten them a little more, and take them off right as your partner finishes.",
    ],
    "become fluent in dirty talk.": [
        "Say what feels good, out loud, during sex.",
        "Tell your partner what you want them to do to you, in explicit detail.",
        "Keep up a filthy running commentary from foreplay to finish, without breaking character.",
    ],
    "do a striptease.": [
        "Strip down to your underwear to one song while your partner watches.",
        "Go all the way, and finish with a lap dance.",
        "Put on a full show: a costume, mood lighting, a chair, and no touching from your audience until you say so.",
    ],
    "do the “anything but penetration” challenge.": [
        "Spend 30 minutes on foreplay, with no penetration at all.",
        "Make each other finish without any penetration, using hands, mouths or toys.",
        "Go a whole week of sex without penetration, and see what you discover.",
    ],
    "give her a creampie; she decides where she wants it.": [
        "She picks the position, and he finishes inside her.",
        "She tells him exactly when, and he holds back until she gives the word.",
        "She picks somewhere more daring, like anal, and he finishes there.",
    ],
    "give her a cumshot; she decides where she wants it.": [
        "She picks a spot, like her stomach or back, and he finishes there.",
        "She chooses somewhere more daring, like her chest or her butt.",
        "She asks for it on her face or in her mouth, and he obliges.",
    ],
    "have a wake-up session.": [
        "Wake them with kisses and cuddles, and let them decide where it goes.",
        "Wake them up with oral sex.",
        "Wake them up and have sex before the alarm goes off, until you both finish.",
    ],
    "have multiple orgasms in one sex session.": [
        "One of you has two orgasms in the same session.",
        "You both have more than one orgasm.",
        "One of you has three or more. Bonus: both of you do.",
    ],
    "have rough sex.": [
        "Get a little rougher: pin their wrists, grab their hips and kiss them hard.",
        "Add hair pulling, spanking and harder thrusting.",
        "Go fully primal: rip clothes off, throw each other on the bed, and leave a few marks.",
    ],
    "have sex with (most of) your clothes on.": [
        "Make out and touch each other with your clothes on, hands under the fabric.",
        "Have sex with only the essentials pushed aside or unzipped.",
        "Have a fully dressed quickie somewhere you could get caught, like right before guests arrive.",
    ],
    "look into each other’s eyes when cumming. bonus: cum at the same time.": [
        "Keep eye contact during sex for as long as you can.",
        "One of you keeps eye contact while finishing.",
        "Finish together while looking into each other’s eyes.",
    ],
    "no-kissing session.": [
        "No kissing on the lips during foreplay.",
        "No kissing on the lips from start to finish.",
        "No kissing at all, anywhere, for a whole session.",
    ],
    "one partner rips the other’s clothes off.": [
        "Undress them fast and impatiently, tugging and throwing clothes aside.",
        "Rip a shirt open, buttons flying.",
        "Tear everything off, then have sex right where you are.",
    ],
    "sex right after the gym.": [
        "Make out right after your workout, while you’re still sweaty.",
        "Have sex as soon as you get home from the gym, no shower.",
        "Work out together and have sex right there in your home gym.",
    ],
    "stay in bed with your partner all day long.": [
        "Spend the morning in bed together, cuddling, talking and having sex.",
        "Stay in bed until dinner, getting up only for the essentials.",
        "Stay in bed all day, and have sex at least three times.",
    ],
    "surprise each other with a new piece of lingerie or a new sex toy.": [
        "Give them the gift, and let them try it on, or out, later.",
        "Give it to them and ask them to try it on, or out, right away.",
        "Give it, try it, and use it together until you both finish.",
    ],
    "try out new lingerie or underwear sets.": [
        "Try on new underwear for your partner, one piece at a time.",
        "Wear it under your clothes all evening, and reveal it at the end of the night.",
        "Model it for your partner, then let them take it off you slowly.",
    ],
    "wear sexy costumes.": [
        "Wear a sexy costume for an evening, and let your partner enjoy the view.",
        "Wear costumes together, and play your characters while you flirt.",
        "Stay in costume and in character all the way through sex.",
    ],
}


def category_names(category):
    """A starter wish's categories as a list: its one category name, or its tuple of them."""
    return [category] if isinstance(category, str) else list(category)
