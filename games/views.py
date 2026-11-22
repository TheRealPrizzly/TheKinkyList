import random

from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.models import profile_for
from accounts.templatetags.people import display_name
from assignments.models import Assignment, GameSession, Reply
from items.models import SPICE_CHOICES, Item
from spaces.decorators import membership_required

from . import logic
from .registry import GAMES, MENU, modes_of
from .services import create_assignments, record_dare

FAVORITE_OPTIONS = 8
SEARCH_LIMIT = 40
TRUTH_OR_DARE = "truth-or-dare"
WOULD_YOU_RATHER = "would-you-rather"


def get_game(slug, playable=False):
    """The game for `slug`. With `playable`, a game you only choose modes from doesn't count."""
    game = GAMES.get(slug)
    if game is None or (playable and game.has_modes):
        raise Http404("No such game")
    return game


def wants_completed(game, params):
    return game.allows_completed and params.get("completed") == "1"


def chosen_spices(params):
    valid = {value for value, _ in SPICE_CHOICES}
    return [spice for spice in logic.parse_ids(params.get("spice", "")) if spice in valid]


def chosen_member(space, raw):
    """The space member whose id is `raw`, or None."""
    ids = logic.parse_ids(raw or "")
    return space.member_users().filter(pk=ids[0]).first() if ids else None


def draw_filters(params):
    """Randomize's filters, e.g. "spice=2,3" and "category=4,7,none" (none means uncategorized)."""
    categories = params.get("category", "")
    return {
        "spices": logic.parse_ids(params.get("spice", "")),
        "category_ids": logic.parse_ids(categories),
        "uncategorized": "none" in categories.split(","),
    }


@membership_required
def index(request, space):
    return render(request, "games/index.html", {"space": space, "games": MENU, "nav": "play"})


@membership_required
def play(request, space, slug):
    game = get_game(slug)
    if game.has_modes:
        return choose_mode(request, space, game)
    include_completed = wants_completed(game, request.GET)
    pool = list(logic.eligible_items(space, game, include_completed))
    rng = random.Random()
    context = {
        "space": space,
        "game": game,
        "nav": "play",
        "include_completed": include_completed,
        "pool_size": len(pool),
    }
    if game.mode_of:
        context.update(parent=GAMES[game.mode_of], modes=modes_of(GAMES[game.mode_of]))
    if slug == "randomize":
        categories = {category.id: category for item in pool for category in item.categories.all()}
        context.update(
            spice_choices=SPICE_CHOICES,
            filter_categories=sorted(categories.values(), key=lambda category: category.name.lower()),
            has_uncategorized=any(not item.category_names for item in pool),
        )
    elif slug == "favorite":
        context["options"] = logic.sample_options(pool, FAVORITE_OPTIONS, rng)
        logic.attach_history(context["options"])
    elif slug == "search":
        results = logic.search_items(pool)
        context.update(
            results=results[:SEARCH_LIMIT],
            hidden_count=max(len(results) - SEARCH_LIMIT, 0),
            categories=sorted({name for item in pool for name in item.category_names}, key=str.lower),
        )
        logic.attach_history(context["results"])
    elif slug == "new":
        context["item"] = logic.draw_new(pool, logic.completed_counts_by_category(space), set(), rng)
        logic.attach_history([context["item"]])
    elif slug == TRUTH_OR_DARE:
        context.update(truth_or_dare_context(space, game))
    elif slug == WOULD_YOU_RATHER:
        context.update(
            spice_choices=SPICE_CHOICES,
            question_count=len(logic.question_pool(space)),
            config={"feedUrl": reverse("games:feed", kwargs={"space_id": space.id, "slug": game.slug})},
        )
    return render(request, f"games/{slug.replace('-', '_')}.html", context)


def choose_mode(request, space, game):
    """A game played in modes, like Kinky List, starts by choosing one."""
    return render(
        request,
        "games/modes.html",
        {
            "space": space,
            "game": game,
            "nav": "play",
            "modes": modes_of(game),
            "pool_size": logic.eligible_items(space, game).count(),
        },
    )


def truth_or_dare_context(space, game):
    players = []
    for member in space.member_users():
        profile = profile_for(member)
        players.append({"id": member.id, "name": profile.name, "color": profile.avatar_color, "initial": profile.initial})
    dare_count = len(logic.dare_pool(space))
    return {
        "spice_choices": SPICE_CHOICES,
        "truth_count": space.truths.count(),
        "dare_count": dare_count,
        "players": players,
        "config": {
            "feedUrl": reverse("games:feed", kwargs={"space_id": space.id, "slug": game.slug}),
            "dareUrl": reverse("games:dare", kwargs={"space_id": space.id}),
            "players": players,
            "dareCount": dare_count,
            # Wishes from The Kinky List that can be mixed in as dares, without and with the ones already lived.
            "wishCount": logic.eligible_items(space, game).count(),
            "wishCountWithDone": logic.eligible_items(space, game, include_completed=True).count(),
        },
    }


def truth_or_dare_feed(request, space, game):
    """HTMX endpoint: a truth or a dare for whoever's turn it is."""
    params = request.GET
    player = chosen_member(space, params.get("player"))
    if player is None:
        raise Http404("No such player")
    spices = chosen_spices(params)
    rng = random.Random()
    context = {"space": space, "game": game, "player": player}
    if params.get("kind") == "truth":
        pool = logic.truth_pool(space, spices)
        seen = set(logic.parse_keys(params.get("exclude", "")))
        truth, recycled = logic.draw_fresh(pool, seen, rng, key=lambda card: card.key, current=params.get("current"))
        if truth is None:
            return render(request, "games/_exhausted.html", context)
        return render(request, "games/_truth_card.html", {**context, "truth": truth, "recycled": recycled})

    pool = logic.dare_pool(space, spices)
    if params.get("mix") == "1":
        # Wishes from The Kinky List join the dares, except ones this player turned down.
        items = logic.filter_pool(logic.eligible_items(space, game, wants_completed(game, params)), spices=spices)
        pool += logic.dares_for(items, player.id, Reply.blocked_until_by_person(space))
    seen = set(logic.parse_keys(params.get("exclude", "")))
    item, recycled = logic.draw_fresh(pool, seen, rng, key=lambda card: str(card.id), current=params.get("current"))
    if item is None:
        return render(request, "games/_exhausted.html", context)
    # A wish from The Kinky List has details to show; a dare from the Truth or Dare list doesn't.
    wish = isinstance(item, Item)
    logic.attach_history([item])
    return render(request, "games/_dare_card.html", {**context, "item": item, "recycled": recycled, "wish": wish})


def would_you_rather_feed(request, space, game):
    """HTMX endpoint: the next "Would you rather" question."""
    pool = logic.question_pool(space, chosen_spices(request.GET))
    seen = set(logic.parse_keys(request.GET.get("exclude", "")))
    question, recycled = logic.draw_fresh(
        pool, seen, random.Random(), key=lambda card: card.key, current=request.GET.get("current")
    )
    context = {"space": space, "game": game}
    if question is None:
        return render(request, "games/_exhausted.html", context)
    return render(request, "games/_question_card.html", {**context, "question": question, "recycled": recycled})


@membership_required
@require_POST
def dare(request, space):
    """Truth or Dare: the player did the dare on the spot ("done") or saves it to their To-do ("later").

    The dare is "d<id>" from the Truth or Dare list, or a wish's id when The Kinky List is mixed in.
    """
    game = GAMES[TRUTH_OR_DARE]
    player = chosen_member(space, request.POST.get("player"))
    outcome = request.POST.get("outcome")
    if player is None or outcome not in ("done", "later"):
        return JsonResponse({"error": "Something went wrong. Try again."}, status=400)
    name = display_name(player)
    card = logic.list_dare(space, request.POST.get("item", ""))
    if card is not None:
        # Dares from the Truth or Dare list aren't wishes, so doing one on the spot leaves nothing to record.
        if outcome == "done":
            return JsonResponse({"session": request.POST.get("session", ""), "message": f"{name} did it!"})
        item = saved_dare(space, request.user, card)
    else:
        item_ids = logic.parse_ids(request.POST.get("item", ""))
        eligible = logic.eligible_items(space, game, wants_completed(game, request.POST))
        item = eligible.filter(pk__in=item_ids[:1]).first() if item_ids else None
    if item is None:
        return JsonResponse({"error": "That dare isn't available any more. Someone may have just drawn it."}, status=409)
    if (item.id, player.id) in Reply.blocked_until_by_person(space):
        return JsonResponse({"error": f"{name} said this isn't for them."}, status=409)
    session_ids = logic.parse_ids(request.POST.get("session", ""))
    session = (
        GameSession.objects.filter(space=space, game_type=game.slug, created_by=request.user, pk=session_ids[0]).first()
        if session_ids
        else None
    )
    session = record_dare(space, game, request.user, item, player, outcome == "done", session)
    message = f"{name} did it! It's on your list as lived." if outcome == "done" else f"Saved to {name}'s To-do."
    return JsonResponse({"session": session.id, "message": message})


def saved_dare(space, user, card):
    """Put a Truth or Dare dare on The Kinky List so it can go on someone's To-do. None if it's in progress there."""
    item = space.items.filter(title__iexact=card.title, archived=False).first()
    if item is None:
        item = Item.objects.create(space=space, title=card.title, spice=card.spice, created_by=user)
        item.set_categories([logic.SAVED_DARE_CATEGORY])
        return item
    return item if not item.assignments.filter(status=Assignment.ACTIVE).exists() else None


@membership_required
def feed(request, space, slug):
    """HTMX endpoint: the next card(s) for a game."""
    game = get_game(slug, playable=True)
    if slug == WOULD_YOU_RATHER:
        return would_you_rather_feed(request, space, game)
    if game.live:
        return truth_or_dare_feed(request, space, game)
    items = logic.eligible_items(space, game, wants_completed(game, request.GET))
    if slug == "randomize":
        items = logic.filter_pool(items, **draw_filters(request.GET))
    pool = list(items)
    ids = set(logic.parse_ids(request.GET.get("exclude", "")))
    rng = random.Random()
    context = {"space": space, "game": game}

    if slug == "favorite":
        context["options"] = logic.sample_options(pool, FAVORITE_OPTIONS, rng, keep_ids=ids)
        logic.attach_history(context["options"])
        return render(request, "games/_pick_grid.html", context)
    if slug == "search":
        results = logic.search_items(pool, request.GET.get("q", ""), request.GET.get("category", ""))
        context.update(options=results[:SEARCH_LIMIT], hidden_count=max(len(results) - SEARCH_LIMIT, 0))
        logic.attach_history(context["options"])
        return render(request, "games/_pick_grid.html", context)

    if slug == "new":
        item = logic.draw_new(pool, logic.completed_counts_by_category(space), ids, rng)
    else:
        # Randomize starts over avoiding what was on screen, unless nothing else is left.
        avoid = ids | set(logic.parse_ids(request.GET.get("avoid", "")))
        item = logic.draw_random(pool, avoid, rng) or logic.draw_random(pool, ids, rng)
    if item is None:
        return render(request, "games/_exhausted.html", context)
    logic.attach_history([item])
    return render(request, f"games/_{slug}_card.html", {**context, "item": item})


@membership_required
@require_POST
def assign(request, space, slug):
    """Step two of the Kinky List modes: choose who each picked item is for, then confirm."""
    game = get_game(slug, playable=True)
    if game.live:
        raise Http404("This game has no assign step")
    include_completed = wants_completed(game, request.POST)
    item_ids = logic.parse_ids(request.POST.getlist("item"))
    eligible = {item.id: item for item in logic.eligible_items(space, game, include_completed)}
    items = [eligible[item_id] for item_id in item_ids if item_id in eligible]

    if not item_ids:
        messages.error(request, "Pick at least one item first.")
        return redirect("games:play", space_id=space.id, slug=slug)
    if len(item_ids) > game.max_picks:
        messages.error(request, f"{game.name} allows up to {game.max_picks} picks.")
        return redirect("games:play", space_id=space.id, slug=slug)
    if len(items) < len(item_ids):
        messages.error(request, "Some of those picks aren't available any more. Someone may have just drawn them.")
        return redirect("games:play", space_id=space.id, slug=slug)

    members = {member.id: member for member in space.member_users()}
    blocked = Reply.blocked_until_by_person(space)
    chosen, errors = {}, {}
    if request.POST.get("confirm"):
        for item in items:
            chosen[item.id] = [i for i in logic.parse_ids(request.POST.getlist(f"assign-{item.id}")) if i in members]
            declined = [members[i] for i in chosen[item.id] if (item.id, i) in blocked]
            if declined:
                errors[item.id] = f"{display_name(declined[0])} said this isn't for them."
            elif not chosen[item.id]:
                errors[item.id] = "Choose at least one person."
        if not errors:
            session = create_assignments(space, game, request.user, items, chosen)
            return redirect("games:done", space_id=space.id, session_id=session.id)

    rows = [
        {
            "item": item,
            "members": [(member, blocked.get((item.id, member.id))) for member in members.values()],
            "chosen": chosen.get(item.id, []),
            "error": errors.get(item.id),
        }
        for item in items
    ]
    return render(
        request,
        "games/assign.html",
        {
            "space": space,
            "game": game,
            "nav": "play",
            "rows": rows,
            "include_completed": include_completed,
            "has_errors": bool(errors),
        },
    )


@membership_required
def done(request, space, session_id):
    session = get_object_or_404(GameSession, pk=session_id, space=space)
    assignments = session.assignments.select_related("item").prefetch_related("item__categories", "assignees__profile")
    return render(
        request,
        "games/done.html",
        {"space": space, "game": GAMES.get(session.game_type), "assignments": assignments, "nav": "play"},
    )
