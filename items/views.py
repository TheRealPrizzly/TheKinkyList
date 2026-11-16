from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from assignments.models import Assignment
from spaces.decorators import membership_required

from .forms import BulkForm, ItemForm, TruthForm
from .models import Item, Truth
from .utils import parse_bulk


def categories_for(space):
    return list(space.categories.filter(items__isnull=False).distinct().values_list("name", flat=True))


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
    return render(
        request,
        "items/list.html",
        {
            "space": space,
            "nav": "list",
            "items": items,
            "form": form,
            "bulk_form": BulkForm(),
            "categories": categories_for(space),
            "category": category,
            "show_archived": show_archived,
            "item_total": space.items.count(),
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
    skipped = len(entries) - len(new_entries)
    note = f" (skipped {skipped} already on the list)" if skipped else ""
    messages.success(request, f"Added {len(new_entries)} item{'s' if len(new_entries) != 1 else ''}{note}.")
    bad_spice = sum(entry.bad_spice for entry in new_entries)
    if bad_spice:
        messages.warning(
            request,
            f"{bad_spice} item{'s' if bad_spice != 1 else ''} had an intensity we didn't recognise, so "
            f"{'they were' if bad_spice != 1 else 'it was'} set to Sweet. Use Sweet, Spicy, Sizzling or 1 to 3.",
        )
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
def clear(request, space):
    count = space.items.count()
    # Deleting items cascades to their assignments; drop the now-empty game sessions too.
    space.items.all().delete()
    space.categories.all().delete()
    space.game_sessions.all().delete()
    messages.success(request, f"Cleared {count} item{'s' if count != 1 else ''}. A fresh start.")
    return redirect("items:list", space_id=space.id)


def truths_url(space):
    """Back to Truth or Dare with the "Your own truths" panel open."""
    url = reverse("games:play", kwargs={"space_id": space.id, "slug": "truth-or-dare"})
    return f"{url}?truths=1#own-truths"


@membership_required
@require_POST
def add_truth(request, space):
    form = TruthForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Write a question and pick an intensity.")
    elif space.truths.filter(text__iexact=" ".join(form.cleaned_data["text"].split())).exists():
        messages.info(request, "That question is already one of yours.")
    else:
        truth = form.save(commit=False)
        truth.space = space
        truth.created_by = request.user
        truth.save()
        messages.success(request, f"Added “{truth.text}”.")
    return redirect(truths_url(space))


@membership_required
@require_POST
def delete_truth(request, space, truth_id):
    truth = get_object_or_404(Truth, pk=truth_id, space=space)
    truth.delete()
    messages.success(request, f"Removed “{truth.text}”.")
    return redirect(truths_url(space))
