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


def _strip_numbering(line):
    head, dot, rest = line.partition(".")
    if dot and head.isdigit() and rest.strip():
        return rest.strip()
    return line
