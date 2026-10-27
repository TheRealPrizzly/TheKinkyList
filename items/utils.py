MAX_CATEGORY = 40
MAX_TITLE = 140


def parse_bulk(text):
    """Parse pasted lines into (category, title) pairs.

    "Romance: Candlelit bath" gives a category; a line without a short prefix
    before the first colon is all title. Bullets and numbering are stripped,
    and duplicate titles (ignoring case) are dropped.
    """
    seen = set()
    entries = []
    for raw in text.splitlines():
        line = raw.strip().lstrip("-*•").strip()
        line = _strip_numbering(line)
        if not line:
            continue
        category, title = "", line
        prefix, sep, rest = line.partition(":")
        if sep and rest.strip() and 0 < len(prefix.strip()) <= MAX_CATEGORY:
            category, title = prefix.strip(), rest.strip()
        title = " ".join(title.split())[:MAX_TITLE]
        key = title.lower()
        if key and key not in seen:
            seen.add(key)
            entries.append((" ".join(category.split()), title))
    return entries


def _strip_numbering(line):
    head, dot, rest = line.partition(".")
    if dot and head.isdigit() and rest.strip():
        return rest.strip()
    return line
