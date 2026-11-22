"""The Built-in lists page, where staff review and edit our built-in lists for every space.

Each change saves right away: new spaces get it, and so does every copy whose space never changed
that field (items/builtins.py). The rows update in place with htmx; without it, each action
redirects back to the page.
"""

from functools import wraps
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import builtins
from .forms import BUILT_IN_FORMS
from .models import SPICE_CHOICES, BuiltIn
from .views import chosen_spice, plural

# The page's tabs: (slug, kind, name, what one entry is called).
TABS = [
    ("wishes", BuiltIn.WISH, "The Kinky List", "wish"),
    ("truths", BuiltIn.TRUTH, "Truths", "truth"),
    ("dares", BuiltIn.DARE, "Dares", "dare"),
    ("questions", BuiltIn.QUESTION, "Would you rather", "question"),
]
TAB_BY_SLUG = {slug: (kind, name, one) for slug, kind, name, one in TABS}
TAB_BY_KIND = {kind: slug for slug, kind, _, _ in TABS}
ONE_BY_KIND = {kind: one for _, kind, _, one in TABS}

SHOW_CHOICES = [("", "All"), ("todo", "To review"), ("done", "Reviewed")]


def staff_required(view):
    """Only staff accounts can open the Built-in lists page. To everyone else, it doesn't exist."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Page not found")
        return view(request, *args, **kwargs)

    return login_required(wrapper)


def is_htmx(request):
    return bool(request.headers.get("HX-Request"))


def saved_note(outcome):
    parts = ["Saved."]
    if outcome.updated:
        parts.append(f"Updated in {plural(outcome.updated, 'space', 'spaces')}.")
    if outcome.kept:
        their = "its" if outcome.kept == 1 else "their"
        parts.append(f"{plural(outcome.kept, 'space', 'spaces')} had changed it and kept {their} own version.")
    return " ".join(parts)


def removed_note(description, outcome):
    # “Have fun.” needs no second full stop after the quote.
    parts = [f"Removed “{description}”" + ("" if description[-1:] in ".?!" else ".")]
    if outcome.deleted:
        parts.append(f"Deleted from {plural(outcome.deleted, 'space', 'spaces')}.")
    if outcome.kept:
        keeps = "keeps its" if outcome.kept == 1 else "keep their"
        parts.append(f"{plural(outcome.kept, 'space', 'spaces')} {keeps} copy, because they changed or used it.")
    return " ".join(parts)


def row_context(entry, **extra):
    return {"entry": entry, "tab": TAB_BY_KIND[entry.kind], "spice_choices": SPICE_CHOICES, **extra}


def back_to_page(entry):
    return redirect(reverse("builtins:page", args=[TAB_BY_KIND[entry.kind]]) + f"#entry-{entry.id}")


def show_row(request, entry, note=""):
    """The entry's row, in place of whatever htmx swapped out; without htmx, the page with a message."""
    if is_htmx(request):
        return render(request, "builtins/_row.html", row_context(entry, note=note))
    if note:
        messages.success(request, note)
    return back_to_page(entry)


def wish_categories():
    names = {}
    for categories in BuiltIn.objects.filter(kind=BuiltIn.WISH).values_list("categories", flat=True):
        for name in categories:
            names.setdefault(name.lower(), name)
    return sorted(names.values(), key=str.lower)


def matches(entry, query):
    haystack = " ".join([entry.text, entry.second, entry.details, *entry.categories, *entry.levels])
    return query.lower() in haystack.lower()


@staff_required
def index(request):
    return redirect("builtins:page", tab=TABS[0][0])


@staff_required
def page(request, tab):
    if tab not in TAB_BY_SLUG:
        raise Http404("No such list")
    kind, name, one = TAB_BY_SLUG[tab]
    query = request.GET.get("q", "").strip()
    show = request.GET.get("show", "")
    spice = chosen_spice(request)
    every = list(builtins.entries(kind))
    shown = [
        entry
        for entry in every
        if (not query or matches(entry, query))
        and (show != "todo" or not entry.reviewed_at)
        and (show != "done" or entry.reviewed_at)
        and (not spice or entry.spice == spice)
    ]

    counts = {
        row["kind"]: row
        for row in BuiltIn.objects.values("kind").annotate(
            total=Count("id"), reviewed=Count("id", filter=Q(reviewed_at__isnull=False))
        )
    }
    tabs = [
        {
            "slug": slug,
            "name": tab_name,
            "total": counts.get(tab_kind, {}).get("total", 0),
            "reviewed": counts.get(tab_kind, {}).get("reviewed", 0),
            "active": slug == tab,
        }
        for slug, tab_kind, tab_name, _ in TABS
    ]

    def link(**changes):
        params = {"q": query, "show": show, "spice": spice or ""}
        params.update(changes)
        return "?" + urlencode({key: value for key, value in params.items() if value})

    return render(
        request,
        "builtins/page.html",
        {
            "tabs": tabs,
            "tab": tab,
            "tab_name": name,
            "one": one,
            "entries": shown,
            "total": len(every),
            "reviewed": sum(1 for entry in every if entry.reviewed_at),
            "query": query,
            "show": show,
            "spice": spice,
            "show_links": [{"label": label, "url": link(show=value), "active": show == value} for value, label in SHOW_CHOICES],
            "spice_links": [{"label": "Every intensity", "url": link(spice=""), "active": not spice}]
            + [{"label": label, "url": link(spice=value), "active": spice == value} for value, label in SPICE_CHOICES],
            "spice_choices": SPICE_CHOICES,
        },
    )


@staff_required
def row(request, entry_id):
    entry = get_object_or_404(BuiltIn, pk=entry_id)
    if not is_htmx(request):
        return back_to_page(entry)
    return render(request, "builtins/_row.html", row_context(entry))


@staff_required
def edit(request, entry_id):
    entry = get_object_or_404(BuiltIn, pk=entry_id)
    form_class = BUILT_IN_FORMS[entry.kind]
    if request.method == "POST":
        form = form_class(request.POST, entry=entry, auto_id=f"entry-{entry.id}-%s")
        if form.is_valid():
            outcome = builtins.update(entry, form.cleaned_data)
            return show_row(request, entry, saved_note(outcome))
    else:
        form = form_class(entry=entry, auto_id=f"entry-{entry.id}-%s")
    context = row_context(entry, form=form, one=ONE_BY_KIND[entry.kind])
    if entry.kind == BuiltIn.WISH:
        context["categories"] = wish_categories()
    template = "builtins/_form.html" if is_htmx(request) else "builtins/edit.html"
    return render(request, template, context)


@staff_required
@require_POST
def set_spice(request, entry_id):
    """Pick an entry's intensity straight from its row, which also marks it as reviewed."""
    entry = get_object_or_404(BuiltIn, pk=entry_id)
    raw = request.POST.get("spice", "")
    if not raw.isdigit() or int(raw) not in dict(SPICE_CHOICES):
        return show_row(request, entry)
    outcome = builtins.update(entry, {"spice": int(raw)})
    return show_row(request, entry, saved_note(outcome))


@staff_required
@require_POST
def toggle_reviewed(request, entry_id):
    entry = get_object_or_404(BuiltIn, pk=entry_id)
    builtins.mark_reviewed(entry, reviewed=not entry.reviewed_at)
    return show_row(request, entry, "Marked as reviewed." if entry.reviewed_at else "Marked as not reviewed.")


@staff_required
@require_POST
def remove(request, entry_id):
    entry = get_object_or_404(BuiltIn, pk=entry_id)
    tab = TAB_BY_KIND[entry.kind]
    description = str(entry)
    outcome = builtins.remove(entry)
    note = removed_note(description, outcome)
    if is_htmx(request):
        return render(request, "builtins/_removed.html", {"note": note})
    messages.success(request, note)
    return redirect("builtins:page", tab=tab)
