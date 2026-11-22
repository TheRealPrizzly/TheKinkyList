"""Our built-in lists (BuiltIn): copying them into spaces, and editing them for everyone.

Every new space gets a copy of each entry, and "Generate a list" adds back the ones a space is
missing. Each copy links back to its entry. When staff save a change on the Built-in lists page,
every copy gets it too, one field at a time, wherever the space never changed that field.
"""

from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone

from assignments.models import Assignment, Reply

from .models import BuiltIn, Dare, Item, Question, Truth

COPY_MODELS = {BuiltIn.WISH: Item, BuiltIn.TRUTH: Truth, BuiltIn.DARE: Dare, BuiltIn.QUESTION: Question}

# The fields of an entry each kind uses.
FIELDS = {
    BuiltIn.WISH: ("text", "details", "spice", "categories", "levels"),
    BuiltIn.TRUTH: ("text", "spice"),
    BuiltIn.DARE: ("text", "spice"),
    BuiltIn.QUESTION: ("text", "second", "spice"),
}

# Where a copy keeps each field, for the fields that are plain columns.
COLUMNS = {
    BuiltIn.WISH: {"text": "title", "details": "description", "spice": "spice"},
    BuiltIn.TRUTH: {"text": "text", "spice": "spice"},
    BuiltIn.DARE: {"text": "text", "spice": "spice"},
    BuiltIn.QUESTION: {"text": "first", "second": "second", "spice": "spice"},
}


def entries(kind):
    return BuiltIn.objects.filter(kind=kind).order_by("position", "id")


def count(kind):
    return BuiltIn.objects.filter(kind=kind).count()


def category_names():
    """Every category the built-in wishes use, spelled as first seen, in alphabetical order."""
    names = {}
    for categories in BuiltIn.objects.filter(kind=BuiltIn.WISH).values_list("categories", flat=True):
        for name in categories:
            names.setdefault(name.lower(), name)
    return sorted(names.values(), key=str.lower)


def _key(kind, text, second=""):
    """Matches the same entry however it was capitalized."""
    return f"{text.lower()} | {second.lower()}" if kind == BuiltIn.QUESTION else text.lower()


def missing(space, kind):
    """The entries of this kind the space has no copy of: none linked to it, and none with the same text."""
    texts = ["first", "second"] if kind == BuiltIn.QUESTION else [COLUMNS[kind]["text"]]
    columns = ["built_in_id", *texts]
    linked, have = set(), set()
    for built_in_id, *texts in COPY_MODELS[kind].objects.filter(space=space).values_list(*columns):
        linked.add(built_in_id)
        have.add(_key(kind, *texts))
    return [entry for entry in entries(kind) if entry.pk not in linked and _key(kind, entry.text, entry.second) not in have]


def add_missing(space, kind, user=None):
    """Give the space a copy of each entry of this kind it doesn't have. Returns how many were added."""
    new = missing(space, kind)
    if kind == BuiltIn.WISH:
        for entry in new:
            item = Item.objects.create(
                space=space,
                built_in=entry,
                title=entry.text,
                description=entry.details,
                spice=entry.spice,
                created_by=user,
            )
            item.set_categories(entry.categories)
            if entry.levels:
                item.set_levels(entry.levels)
    elif kind == BuiltIn.QUESTION:
        Question.objects.bulk_create(
            Question(space=space, built_in=e, first=e.text, second=e.second, spice=e.spice, created_by=user)
            for e in new
        )
    else:
        COPY_MODELS[kind].objects.bulk_create(
            COPY_MODELS[kind](space=space, built_in=e, text=e.text, spice=e.spice, created_by=user) for e in new
        )
    return len(new)


def fill_new_space(space, user=None):
    """Every new space starts with all three lists ready to play."""
    for kind, _ in BuiltIn.KIND_CHOICES:
        add_missing(space, kind, user)


# ---------- Editing an entry for everyone ----------


@dataclass
class Outcome:
    # Copies that changed, and copies that kept something the space had changed itself.
    updated: int = 0
    kept: int = 0
    # Removing: copies deleted along with the entry.
    deleted: int = 0


def values(entry):
    """The entry's fields, copied so that later changes to the entry leave them as they were."""
    return {
        field: list(value) if isinstance(value, list) else value
        for field, value in ((field, getattr(entry, field)) for field in FIELDS[entry.kind])
    }


def _copy_value(kind, copy, field):
    if field == "categories":
        return copy.category_names
    if field == "levels":
        return [level.text for level in copy.levels.all()]
    return getattr(copy, COLUMNS[kind][field])


def _same(field, a, b):
    if field == "details":
        return a.strip() == b.strip()
    if field == "categories":
        return sorted(name.lower() for name in a) == sorted(name.lower() for name in b)
    return a == b


def _clashes(kind, copy, new):
    """Whether the space already has another entry with the new text, so renaming would duplicate it."""
    others = COPY_MODELS[kind].objects.filter(space_id=copy.space_id).exclude(pk=copy.pk)
    if kind == BuiltIn.QUESTION:
        return others.filter(first__iexact=new["text"], second__iexact=new["second"]).exists()
    return others.filter(**{f"{COLUMNS[kind]['text']}__iexact": new["text"]}).exists()


def _update_copy(kind, copy, old, new, changed):
    """Give one copy each changed field it still has as it was. Returns (updated, kept)."""
    apply = [field for field in changed if _same(field, _copy_value(kind, copy, field), old[field])]
    if {"text", "second"} & set(apply) and _clashes(kind, copy, new):
        apply = [field for field in apply if field not in ("text", "second")]
    columns = []
    for field in apply:
        if field == "categories":
            copy.set_categories(new["categories"])
        elif field == "levels":
            copy.set_levels(new["levels"])
        else:
            setattr(copy, COLUMNS[kind][field], new[field])
            columns.append(COLUMNS[kind][field])
    if columns:
        copy.save(update_fields=columns)
    return bool(apply), len(apply) < len(changed)


def copies(entry):
    found = COPY_MODELS[entry.kind].objects.filter(built_in=entry)
    if entry.kind == BuiltIn.WISH:
        found = found.prefetch_related("categories", "levels")
    return found


@transaction.atomic
def update(entry, changes):
    """Save changes to an entry, mark it as reviewed, and give every copy the fields its space never changed."""
    old = values(entry)
    for field, value in changes.items():
        setattr(entry, field, value)
    entry.reviewed_at = timezone.now()
    entry.save()
    new = values(entry)
    changed = [field for field in FIELDS[entry.kind] if new[field] != old[field]]
    outcome = Outcome()
    if not changed:
        return outcome
    for copy in copies(entry):
        updated, kept = _update_copy(entry.kind, copy, old, new, changed)
        outcome.updated += updated
        outcome.kept += kept
    return outcome


def mark_reviewed(entry, reviewed=True):
    entry.reviewed_at = timezone.now() if reviewed else None
    entry.save(update_fields=["reviewed_at", "updated_at"])


def _used(kind, copy):
    """Whether removing the copy would lose something: a wish that was given in a game, replied to or levelled."""
    if kind != BuiltIn.WISH:
        return False
    return (
        Assignment.objects.filter(item=copy).exists()
        or Reply.objects.filter(item=copy).exists()
        or copy.levels.filter(done_at__isnull=False).exists()
    )


@transaction.atomic
def remove(entry):
    """Take an entry off the built-in lists.

    Copies that are just as the entry has them and were never used go too. The others stay, as the
    space's own.
    """
    old = values(entry)
    outcome = Outcome()
    for copy in copies(entry):
        untouched = all(_same(field, _copy_value(entry.kind, copy, field), old[field]) for field in old)
        if untouched and not _used(entry.kind, copy):
            copy.delete()
            outcome.deleted += 1
        else:
            outcome.kept += 1
    entry.delete()
    return outcome
