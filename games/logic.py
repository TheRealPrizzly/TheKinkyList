"""Item selection rules for the four games.

The query helpers build the candidate pool for a space; the pure functions
below them only work on sequences of items and an injected `random.Random`,
so they are easy to test deterministically.
"""

from collections import Counter

from django.db.models import Q

from assignments.models import Assignment
from items.models import Item


def eligible_items(space, game, include_completed=False):
    """Items a game may offer: not archived and not currently assigned."""
    items = Item.objects.filter(space=space, archived=False).prefetch_related("categories")
    if not game.allows_completed:
        return items.filter(assignments__isnull=True)
    items = items.exclude(assignments__status=Assignment.ACTIVE)
    if not include_completed:
        items = items.exclude(assignments__status=Assignment.COMPLETED)
    return items.distinct()


def filter_pool(items, spices=(), category_ids=(), uncategorized=False):
    """Narrow an item queryset to the chosen intensities and categories.

    Choosing nothing in a row leaves it unrestricted. Several categories match
    items in any of them; `uncategorized` also lets in items with no category.
    """
    if spices:
        items = items.filter(spice__in=spices)
    if category_ids or uncategorized:
        wanted = Q(categories__in=category_ids)
        if uncategorized:
            wanted |= Q(categories__isnull=True)
        items = items.filter(wanted).distinct()
    return items


def completed_counts_by_category(space):
    """Times each category was lived; an item in several categories counts toward each."""
    counts = Counter()
    for category in Assignment.objects.filter(space=space, status=Assignment.COMPLETED).values_list(
        "item__categories__name", flat=True
    ):
        counts[category_key(category)] += 1
    return counts


def category_key(category):
    return (category or "").strip().lower()


def category_keys(item):
    """An item's category keys; an uncategorized item has the single key ""."""
    return {category_key(name) for name in item.category_names} or {""}


def draw_random(pool, exclude_ids, rng):
    candidates = [item for item in pool if item.id not in exclude_ids]
    return rng.choice(candidates) if candidates else None


def sample_options(pool, count, rng, keep_ids=()):
    """Up to `count` items: the kept (already selected) ones first, then random others."""
    kept = [item for item in pool if item.id in keep_ids]
    others = [item for item in pool if item.id not in keep_ids]
    room = max(count - len(kept), 0)
    return kept + rng.sample(others, min(room, len(others)))


def search_items(pool, query="", category=""):
    """Case-insensitive search where every word must appear; title matches rank first."""
    tokens = query.lower().split()
    wanted_category = category_key(category)
    title_hits, other_hits = [], []
    for item in pool:
        if wanted_category and wanted_category not in category_keys(item):
            continue
        title = item.title.lower()
        haystack = " ".join([title, item.description.lower(), *category_keys(item)])
        if all(token in haystack for token in tokens):
            (title_hits if tokens and all(t in title for t in tokens) else other_hits).append(item)
    key = lambda item: item.title.lower()  # noqa: E731
    return sorted(title_hits, key=key) + sorted(other_hits, key=key)


def category_weights(categories, completed_counts):
    """Less-explored categories weigh more: 1 / (1 + times completed)."""
    return {category: 1 / (1 + completed_counts.get(category, 0)) for category in categories}


def draw_new(pool, completed_counts, exclude_ids, rng):
    """Pick a category weighted toward the unexplored, then an item within it.

    An item in several categories can be reached through any of them.
    """
    by_category = {}
    for item in pool:
        if item.id not in exclude_ids:
            for key in category_keys(item):
                by_category.setdefault(key, []).append(item)
    if not by_category:
        return None
    categories = sorted(by_category)
    weights = category_weights(categories, completed_counts)
    category = rng.choices(categories, weights=[weights[c] for c in categories])[0]
    return rng.choice(by_category[category])


def parse_ids(raw):
    """Turn "1,2,x,3" or ["1", "2"] into a de-duplicated list of ints in order, ignoring junk."""
    parts = raw.split(",") if isinstance(raw, str) else raw
    ids = []
    for part in parts:
        part = str(part).strip()
        if part.isdigit() and int(part) not in ids:
            ids.append(int(part))
    return ids
