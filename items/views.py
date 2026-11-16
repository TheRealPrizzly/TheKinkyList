from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from assignments.models import Assignment
from spaces.decorators import membership_required

from .forms import BulkForm, ItemForm, QuestionForm, QuestionImportForm, TruthOrDareForm, TruthOrDareImportForm
from .lists import KINKY_LIST, LISTS, TRUTH_OR_DARE, WOULD_YOU_RATHER
from .models import SPICE_CHOICES, Dare, Item, Question, Truth
from .utils import parse_bulk, parse_questions, parse_truths_and_dares


def categories_for(space):
    return list(space.categories.filter(items__isnull=False).distinct().values_list("name", flat=True))


def plural(count, one, many):
    return f"{count} {one if count == 1 else many}"


def chosen_spice(request):
    """The intensity filter from "?spice=2", or None."""
    raw = request.GET.get("spice", "")
    return int(raw) if raw.isdigit() and int(raw) in dict(SPICE_CHOICES) else None


def list_page(request, space, game_list, template, context):
    """Render one tab of "Our lists", with the tabs and the Generate / Clear toolbar every list shares."""
    count = game_list.count(space)
    tabs = [
        {"list": other, "count": count if other is game_list else other.count(space), "active": other is game_list}
        for other in LISTS.values()
    ]
    return render(
        request,
        template,
        {
            "space": space,
            "nav": "list",
            "tabs": tabs,
            "game_list": game_list,
            "count": count,
            "count_label": game_list.describe(count),
            "missing": game_list.missing(space),
            "spice_choices": SPICE_CHOICES,
            "spice": chosen_spice(request),
            **context,
        },
    )


def warn_bad_spice(request, entries):
    bad_spice = sum(entry.bad_spice for entry in entries)
    if bad_spice:
        messages.warning(
            request,
            f"{bad_spice} line{'s' if bad_spice != 1 else ''} had an intensity we didn't recognise, so "
            f"{'they were' if bad_spice != 1 else 'it was'} set to Sweet. Use Sweet, Spicy, Sizzling or 1 to 3.",
        )


def added_message(request, added, skipped, one, many):
    note = f" (skipped {skipped} already on the list)" if skipped else ""
    messages.success(request, f"Added {plural(added, one, many)}{note}.")


# ---------- All lists ----------


def get_list(slug):
    try:
        return LISTS[slug]
    except KeyError:
        raise Http404("No such list")


def to_list(space, game_list):
    return redirect(f"items:{game_list.url_name}", space_id=space.id)


@membership_required
@require_POST
def generate(request, space, list_slug):
    """Add whatever of our built-in entries the list doesn't have: a full list when it's empty."""
    game_list = get_list(list_slug)
    with transaction.atomic():
        added = game_list.generate(space, request.user)
    if added:
        messages.success(request, f"Added {game_list.describe(added)} to {game_list.name}.")
    else:
        messages.info(request, f"Everything we have for {game_list.name} is already on your list.")
    return to_list(space, game_list)


@membership_required
@require_POST
def clear(request, space, list_slug):
    game_list = get_list(list_slug)
    count = game_list.count(space)
    with transaction.atomic():
        game_list.clear(space)
    messages.success(request, f"Cleared {game_list.describe(count)} from {game_list.name}. A fresh start.")
    return to_list(space, game_list)


# ---------- The Kinky List ----------


@membership_required
def item_list(request, space):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.space = space
        item.created_by = request.user
        item.save()
        item.set_categories(form.cleaned_data["categories"])
        messages.success(request, f"Added “{item.title}”.")
        return redirect("items:list", space_id=space.id)

    show_archived = request.GET.get("archived") == "1"
    category = request.GET.get("category", "")
    items = space.items.filter(archived=show_archived)
    if category:
        items = items.filter(categories__name__iexact=category)
    items = items.annotate(
        active_count=Count("assignments", filter=Q(assignments__status=Assignment.ACTIVE)),
        done_count=Count("assignments", filter=Q(assignments__status=Assignment.COMPLETED)),
    ).prefetch_related("categories")
    return list_page(
        request,
        space,
        KINKY_LIST,
        "items/list.html",
        {
            "items": items,
            "form": form,
            "bulk_form": BulkForm(),
            "categories": categories_for(space),
            "category": category,
            "show_archived": show_archived,
            "open_add": request.method == "POST",
        },
    )


@membership_required
@require_POST
def bulk_add(request, space):
    form = BulkForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Paste at least one line.")
        return redirect("items:list", space_id=space.id)
    entries = parse_bulk(form.cleaned_data["lines"])
    existing = {title.lower() for title in space.items.values_list("title", flat=True)}
    new_entries = [entry for entry in entries if entry.title.lower() not in existing]
    with transaction.atomic():
        for entry in new_entries:
            item = Item.objects.create(space=space, title=entry.title, spice=entry.spice, created_by=request.user)
            item.set_categories(entry.categories)
    added_message(request, len(new_entries), len(entries) - len(new_entries), "wish", "wishes")
    warn_bad_spice(request, new_entries)
    return redirect("items:list", space_id=space.id)


@membership_required
def edit(request, space, item_id):
    item = get_object_or_404(Item, pk=item_id, space=space)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        item.set_categories(form.cleaned_data["categories"])
        messages.success(request, "Saved.")
        return redirect("items:list", space_id=space.id)
    return render(
        request,
        "items/edit.html",
        {"space": space, "nav": "list", "item": item, "form": form, "categories": categories_for(space)},
    )


@membership_required
@require_POST
def toggle_archive(request, space, item_id):
    item = get_object_or_404(Item, pk=item_id, space=space)
    item.archived = not item.archived
    item.save(update_fields=["archived"])
    messages.success(request, f"“{item.title}” {'archived' if item.archived else 'restored'}.")
    return redirect("items:list", space_id=space.id)


@membership_required
@require_POST
def delete_item(request, space, item_id):
    item = get_object_or_404(Item, pk=item_id, space=space)
    # Its to-dos and memories go with it; sessions left with nothing in them go too.
    sessions = list(item.assignments.values_list("session", flat=True))
    item.delete()
    space.game_sessions.filter(pk__in=sessions, assignments__isnull=True).delete()
    messages.success(request, f"Removed “{item.title}”.")
    return redirect("items:list", space_id=space.id)


# ---------- Truth or Dare ----------


@membership_required
def truth_or_dare(request, space):
    form = TruthOrDareForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            add_truth_or_dare(request, space, form.cleaned_data)
            return redirect("items:truth_or_dare", space_id=space.id)
    spice = chosen_spice(request)
    truths, dares = space.truths.all(), space.dares.all()
    if spice:
        truths, dares = truths.filter(spice=spice), dares.filter(spice=spice)
    return list_page(
        request,
        space,
        TRUTH_OR_DARE,
        "items/truth_or_dare.html",
        {
            "truths": truths,
            "dares": dares,
            "form": form,
            "import_form": TruthOrDareImportForm(),
            "open_add": request.method == "POST",
        },
    )


def add_truth_or_dare(request, space, data):
    model = Truth if data["kind"] == "truth" else Dare
    text = " ".join(data["text"].split())
    if model.objects.filter(space=space, text__iexact=text).exists():
        messages.info(request, f"That {data['kind']} is already on the list.")
        return
    model.objects.create(space=space, text=text, spice=data["spice"], created_by=request.user)
    messages.success(request, f"Added “{text}”.")


@membership_required
@require_POST
def import_truth_or_dare(request, space):
    form = TruthOrDareImportForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Paste at least one line.")
        return redirect("items:truth_or_dare", space_id=space.id)
    entries = parse_truths_and_dares(form.cleaned_data["lines"], form.cleaned_data["kind"])
    existing = {
        "truth": {text.lower() for text in space.truths.values_list("text", flat=True)},
        "dare": {text.lower() for text in space.dares.values_list("text", flat=True)},
    }
    new_entries = [entry for entry in entries if entry.text.lower() not in existing[entry.kind]]
    models = {"truth": Truth, "dare": Dare}
    with transaction.atomic():
        for kind, model in models.items():
            model.objects.bulk_create(
                model(space=space, text=entry.text, spice=entry.spice, created_by=request.user)
                for entry in new_entries
                if entry.kind == kind
            )
    truths = sum(entry.kind == "truth" for entry in new_entries)
    dares = len(new_entries) - truths
    skipped = len(entries) - len(new_entries)
    note = f" (skipped {skipped} already on the list)" if skipped else ""
    messages.success(
        request, f"Added {plural(truths, 'truth', 'truths')} and {plural(dares, 'dare', 'dares')}{note}."
    )
    warn_bad_spice(request, new_entries)
    return redirect("items:truth_or_dare", space_id=space.id)


@membership_required
@require_POST
def delete_truth(request, space, truth_id):
    truth = get_object_or_404(Truth, pk=truth_id, space=space)
    truth.delete()
    messages.success(request, f"Removed “{truth.text}”.")
    return redirect("items:truth_or_dare", space_id=space.id)


@membership_required
@require_POST
def delete_dare(request, space, dare_id):
    dare = get_object_or_404(Dare, pk=dare_id, space=space)
    dare.delete()
    messages.success(request, f"Removed “{dare.text}”.")
    return redirect("items:truth_or_dare", space_id=space.id)


# ---------- Would you rather ----------


@membership_required
def would_you_rather(request, space):
    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        question = form.save(commit=False)
        question.space = space
        question.created_by = request.user
        # Normalizes the choices, so the duplicate check sees them as they'll be saved.
        question.first, question.second = (" ".join(choice.split()) for choice in (question.first, question.second))
        if any(other.key == question.key for other in space.questions.only("first", "second")):
            messages.info(request, "That question is already on the list.")
        else:
            question.save()
            messages.success(request, f"Added “{question.text}”.")
        return redirect("items:would_you_rather", space_id=space.id)
    questions = space.questions.all()
    spice = chosen_spice(request)
    if spice:
        questions = questions.filter(spice=spice)
    return list_page(
        request,
        space,
        WOULD_YOU_RATHER,
        "items/would_you_rather.html",
        {
            "questions": questions,
            "form": form,
            "import_form": QuestionImportForm(),
            "open_add": request.method == "POST",
        },
    )


@membership_required
@require_POST
def import_questions(request, space):
    form = QuestionImportForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Paste at least one line.")
        return redirect("items:would_you_rather", space_id=space.id)
    entries, unreadable = parse_questions(form.cleaned_data["lines"])
    existing = {question.key for question in space.questions.only("first", "second")}
    new_entries = [entry for entry in entries if entry.key not in existing]
    Question.objects.bulk_create(
        Question(space=space, first=entry.first, second=entry.second, spice=entry.spice, created_by=request.user)
        for entry in new_entries
    )
    added_message(request, len(new_entries), len(entries) - len(new_entries), "question", "questions")
    if unreadable:
        messages.warning(
            request,
            f"Couldn't read {plural(len(unreadable), 'line', 'lines')}, starting with “{unreadable[0]}”. "
            "Separate the two choices with |, or write the question with a single “or”.",
        )
    warn_bad_spice(request, new_entries)
    return redirect("items:would_you_rather", space_id=space.id)


@membership_required
@require_POST
def delete_question(request, space, question_id):
    question = get_object_or_404(Question, pk=question_id, space=space)
    question.delete()
    messages.success(request, f"Removed “{question.text}”.")
    return redirect("items:would_you_rather", space_id=space.id)
