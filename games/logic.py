"""Item selection rules for the games.

The query helpers build the candidate pool for a space; the pure functions
below them only work on sequences of items and an injected `random.Random`,
so they are easy to test deterministically.
"""

from collections import Counter
from dataclasses import dataclass
from operator import attrgetter

from django.db.models import Count, Q

from assignments.models import Assignment, Reply
from items.models import SPICE_CHOICES, Item

SPICE_NAMES = dict(SPICE_CHOICES)


def eligible_items(space, game, include_completed=False):
    """Items a game may offer: not archived, not currently assigned, and not turned down by everyone."""
    declined_by_all = (
        Reply.declines(space)
        .filter(user__memberships__space=space)
        .values("item")
        .annotate(people=Count("user", distinct=True))
        .filter(people__gte=space.memberships.count())
        .values("item")
    )
    items = (
        Item.objects.filter(space=space, archived=False)
        .exclude(pk__in=declined_by_all)
        .prefetch_related("categories")
    )
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


@dataclass(frozen=True)
class TruthCard:
    """A question from the space's Truth or Dare list, keyed "t<id>"."""

    key: str
    text: str
    spice: int

    def get_spice_display(self):
        return SPICE_NAMES.get(self.spice, "")


def truth_pool(space, spices=()):
    """The space's truths at the chosen intensities (none chosen means all)."""
    truths = space.truths.all()
    if spices:
        truths = truths.filter(spice__in=spices)
    return [TruthCard(f"t{truth.id}", truth.text, truth.spice) for truth in truths]


# The category a dare from the Truth or Dare list gets once it's saved to The Kinky List.
SAVED_DARE_CATEGORY = "Truth or Dare"


@dataclass(frozen=True)
class DareCard:
    """A dare from the space's Truth or Dare list, shaped like an Item so the same card template shows it.

    Its id is "d<id>", which tells it apart from wishes on The Kinky List.
    """

    id: str
    title: str
    spice: int
    description: str = ""
    category_names: tuple = (SAVED_DARE_CATEGORY,)

    @property
    def pk(self):
        return self.id

    def get_spice_display(self):
        return SPICE_NAMES.get(self.spice, "")


def dare_card(dare):
    return DareCard(f"d{dare.id}", dare.text, dare.spice)


def list_dare(space, key):
    """The DareCard for "d<id>" on the space's Truth or Dare list, or None."""
    if not (key.startswith("d") and key[1:].isdigit()):
        return None
    dare = space.dares.filter(pk=int(key[1:])).first()
    return dare_card(dare) if dare else None


def dare_pool(space, spices=()):
    """The space's dares at the chosen intensities, minus any on The Kinky List (e.g. saved for later)."""
    on_list = {" ".join(title.split()).lower() for title in space.items.values_list("title", flat=True)}
    dares = space.dares.all()
    if spices:
        dares = dares.filter(spice__in=spices)
    return [dare_card(dare) for dare in dares if dare.text.lower() not in on_list]


@dataclass(frozen=True)
class QuestionCard:
    """A "Would you rather" question from the space's list, keyed "q<id>"."""

    key: str
    first: str
    second: str
    spice: int

    @property
    def text(self):
        return f"Would you rather {self.first} or {self.second}?"

    def get_spice_display(self):
        return SPICE_NAMES.get(self.spice, "")


def question_pool(space, spices=()):
    """The space's "Would you rather" questions at the chosen intensities (none chosen means all)."""
    questions = space.questions.all()
    if spices:
        questions = questions.filter(spice__in=spices)
    return [QuestionCard(f"q{q.id}", q.first, q.second, q.spice) for q in questions]


def dares_for(items, player_id, blocked):
    """Drop the dares this player said "Not for me" to. `blocked` is Reply.blocked_until_by_person()."""
    return [item for item in items if (item.id, player_id) not in blocked]


def draw_fresh(pool, seen, rng, key=attrgetter("id"), current=None):
    """A card not seen yet. Once every card has been seen, start over, avoiding the one on screen.

    Returns (card, recycled); card is None only when nothing but `current` is left.
    """
    fresh = [card for card in pool if key(card) not in seen]
    if fresh:
        return rng.choice(fresh), False
    others = [card for card in pool if key(card) != current]
    return (rng.choice(others), True) if others else (None, False)


def parse_keys(raw):
    """Turn "b1, t4,,b1" into ["b1", "t4"]."""
    keys = []
    for part in raw.split(","):
        part = part.strip()
        if part and part not in keys:
            keys.append(part)
    return keys


def parse_ids(raw):
    """Turn "1,2,x,3" or ["1", "2"] into a de-duplicated list of ints in order, ignoring junk."""
    parts = raw.split(",") if isinstance(raw, str) else raw
    ids = []
    for part in parts:
        part = str(part).strip()
        if part.isdigit() and int(part) not in ids:
            ids.append(int(part))
    return ids
