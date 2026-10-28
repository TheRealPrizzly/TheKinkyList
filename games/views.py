import random

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from assignments.models import GameSession
from spaces.decorators import membership_required

from . import logic
from .registry import GAMES
from .services import create_assignments

FAVORITE_OPTIONS = 10
SEARCH_LIMIT = 40


def get_game(slug):
    try:
        return GAMES[slug]
    except KeyError:
        raise Http404("No such game")


def wants_completed(game, params):
    return game.allows_completed and params.get("completed") == "1"


@membership_required
def index(request, space):
    return render(request, "games/index.html", {"space": space, "games": GAMES.values(), "nav": "play"})


@membership_required
def play(request, space, slug):
    game = get_game(slug)
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
    if slug == "randomize":
        context["item"] = logic.draw_random(pool, set(), rng)
    elif slug == "favorite":
        context["options"] = logic.sample_options(pool, FAVORITE_OPTIONS, rng)
    elif slug == "search":
        results = logic.search_items(pool)
        context.update(
            results=results[:SEARCH_LIMIT],
            hidden_count=max(len(results) - SEARCH_LIMIT, 0),
            categories=sorted({name for item in pool for name in item.category_names}, key=str.lower),
        )
    elif slug == "new":
        context["item"] = logic.draw_new(pool, logic.completed_counts_by_category(space), set(), rng)
    return render(request, f"games/{slug}.html", context)


@membership_required
def feed(request, space, slug):
    """HTMX endpoint: the next card(s) for a game."""
    game = get_game(slug)
    pool = list(logic.eligible_items(space, game, wants_completed(game, request.GET)))
    ids = set(logic.parse_ids(request.GET.get("exclude", "")))
    rng = random.Random()
    context = {"space": space, "game": game}

    if slug == "favorite":
        context["options"] = logic.sample_options(pool, FAVORITE_OPTIONS, rng, keep_ids=ids)
        return render(request, "games/_pick_grid.html", context)
    if slug == "search":
        results = logic.search_items(pool, request.GET.get("q", ""), request.GET.get("category", ""))
        context.update(options=results[:SEARCH_LIMIT], hidden_count=max(len(results) - SEARCH_LIMIT, 0))
        return render(request, "games/_pick_grid.html", context)

    if slug == "new":
        item = logic.draw_new(pool, logic.completed_counts_by_category(space), ids, rng)
    else:
        item = logic.draw_random(pool, ids, rng)
    if item is None:
        return render(request, "games/_exhausted.html", context)
    return render(request, f"games/_{slug}_card.html", {**context, "item": item})


@membership_required
@require_POST
def assign(request, space, slug):
    """Step two of every game: choose who each picked item is for, then confirm."""
    game = get_game(slug)
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

    members = list(space.member_users())
    member_ids = {member.id for member in members}
    chosen, errors = {}, {}
    if request.POST.get("confirm"):
        for item in items:
            chosen[item.id] = [i for i in logic.parse_ids(request.POST.getlist(f"assign-{item.id}")) if i in member_ids]
            if not chosen[item.id]:
                errors[item.id] = "Choose at least one person."
        if not errors:
            session = create_assignments(space, game, request.user, items, chosen)
            return redirect("games:done", space_id=space.id, session_id=session.id)

    rows = [{"item": item, "chosen": chosen.get(item.id, []), "error": errors.get(item.id)} for item in items]
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
