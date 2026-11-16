import re
from dataclasses import dataclass, field

from .models import SPICE_CHOICES

MAX_CATEGORY = 40
MAX_TITLE = 140
DEFAULT_SPICE = 1
SPICE_BY_NAME = {label.lower(): value for value, label in SPICE_CHOICES}


@dataclass
class BulkEntry:
    title: str
    categories: list = field(default_factory=list)
    spice: int = DEFAULT_SPICE
    # Set when the line had an intensity we couldn't read, so it fell back to the default.
    bad_spice: bool = False


def parse_bulk(text):
    """Parse pasted lines of "Action | Categories | Intensity" into BulkEntry objects.

    Tabs work as separators too, so rows pasted from a spreadsheet parse. Categories
    and intensity are optional; categories are comma-separated and intensity is a
    level name or number ("Spicy" or "2"). Bullets and numbering are stripped, and
    duplicate actions (ignoring case) are dropped.
    """
    seen = set()
    entries = []
    for raw in text.splitlines():
        line = raw.strip().lstrip("-*•").strip()
        line = _strip_numbering(line)
        sep = "\t" if "\t" in line else "|"
        title, _, rest = line.partition(sep)
        category_text, _, spice_text = rest.partition(sep)
        title = " ".join(title.split())[:MAX_TITLE]
        key = title.lower()
        if not key or key in seen:
            continue
        seen.add(key)
        spice = parse_spice(spice_text)
        entries.append(
            BulkEntry(
                title=title,
                categories=split_categories(category_text),
                spice=spice or DEFAULT_SPICE,
                bad_spice=spice is None,
            )
        )
    return entries


def split_categories(text):
    """"Romance, adventure, romance" gives ["Romance", "adventure"]: trimmed, capped, de-duplicated."""
    names = []
    for part in text.split(","):
        name = " ".join(part.split())[:MAX_CATEGORY].strip()
        if name and name.lower() not in {n.lower() for n in names}:
            names.append(name)
    return names


def parse_spice(text):
    """An intensity level from "2" or "spicy"; DEFAULT_SPICE when blank, None when unreadable."""
    text = text.strip().lower()
    if not text:
        return DEFAULT_SPICE
    if text.isdigit() and int(text) in SPICE_BY_NAME.values():
        return int(text)
    return SPICE_BY_NAME.get(text)


@dataclass
class CardEntry:
    """One line of a pasted Truth or Dare list."""

    kind: str
    text: str
    spice: int = DEFAULT_SPICE
    bad_spice: bool = False


# Item.title caps dares, because a dare saved for later goes on The Kinky List.
MAX_CARD = {"truth": 200, "dare": 140}


def parse_truths_and_dares(text, default_kind="truth"):
    """Parse pasted lines of "Text | Intensity" into CardEntry objects of `default_kind`.

    A line can start with a "Truth" or "Dare" column to say which it is, e.g.
    "Dare | Kiss my neck | Spicy". Separators, bullets and duplicates work as in parse_bulk.
    """
    seen = set()
    entries = []
    for line in _clean_lines(text):
        columns = [" ".join(column.split()) for column in line.split(_separator(line))]
        kind = default_kind
        if len(columns) > 1 and columns[0].lower() in MAX_CARD:
            kind = columns.pop(0).lower()
        card = columns[0][: MAX_CARD[kind]]
        if not card or (kind, card.lower()) in seen:
            continue
        seen.add((kind, card.lower()))
        spice = parse_spice(columns[1] if len(columns) > 1 else "")
        entries.append(CardEntry(kind, card, spice or DEFAULT_SPICE, bad_spice=spice is None))
    return entries


@dataclass
class QuestionEntry:
    """One line of a pasted "Would you rather" list."""

    first: str
    second: str
    spice: int = DEFAULT_SPICE
    bad_spice: bool = False

    @property
    def key(self):
        return f"{self.first.lower()} | {self.second.lower()}"


MAX_CHOICE = 120


def parse_questions(text):
    """Parse pasted "Would you rather" questions. Returns (entries, lines it couldn't read).

    Each line is "First choice | Second choice | Intensity", or the question written out,
    "Would you rather be tied up or do the tying? | Spicy", as long as it has one "or".
    The "Would you rather" and the question mark are optional either way.
    """
    seen = set()
    entries, unreadable = [], []
    for line in _clean_lines(text):
        columns = [" ".join(column.split()) for column in line.split(_separator(line))]
        if len(columns) == 1 or (len(columns) == 2 and parse_spice(columns[1]) and _one_or(columns[0])):
            choices = _one_or(columns[0])
            spice_text = columns[1] if len(columns) > 1 else ""
            if not choices:
                unreadable.append(line)
                continue
        else:
            choices, spice_text = columns[:2], columns[2] if len(columns) > 2 else ""
        first, second = (_tidy_choice(choice) for choice in choices)
        if not first or not second:
            unreadable.append(line)
            continue
        spice = parse_spice(spice_text)
        entry = QuestionEntry(first, second, spice or DEFAULT_SPICE, bad_spice=spice is None)
        if entry.key not in seen:
            seen.add(entry.key)
            entries.append(entry)
    return entries, unreadable


def _one_or(text):
    """Split "A or B" into [A, B], or None unless " or " appears exactly once."""
    parts = re.split(r"\s+or\s+", _tidy_choice(text), flags=re.IGNORECASE)
    return parts if len(parts) == 2 else None


def _tidy_choice(text):
    text = " ".join(text.split()).rstrip("?.!").strip()
    text = re.sub(r"^would you rather\b[\s:,]*", "", text, flags=re.IGNORECASE)
    return text[:MAX_CHOICE].strip()


def _clean_lines(text):
    """Non-empty lines without bullets or numbering."""
    for raw in text.splitlines():
        line = _strip_numbering(raw.strip().lstrip("-*•").strip())
        if line:
            yield line


def _separator(line):
    return "\t" if "\t" in line else "|"


def _strip_numbering(line):
    head, dot, rest = line.partition(".")
    if dot and head.isdigit() and rest.strip():
        return rest.strip()
    return line
