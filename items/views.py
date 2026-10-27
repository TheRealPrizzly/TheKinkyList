from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from assignments.models import Assignment
from spaces.decorators import membership_required

from .forms import BulkForm, ItemForm
from .models import Item
from .utils import parse_bulk


def categories_for(space):
    return sorted(
        set(space.items.exclude(category="").values_list("category", flat=True)),
        key=str.lower,
    )


@membership_required
def item_list(request, space):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.space = space
        item.created_by = request.user
        item.save()
        messages.success(request, f"Added “{item.title}”.")
        return redirect("items:list", space_id=space.id)

    show_archived = request.GET.get("archived") == "1"
    category = request.GET.get("category", "")
    items = space.items.filter(archived=show_archived).annotate(
        active_count=Count("assignments", filter=Q(assignments__status=Assignment.ACTIVE)),
        done_count=Count("assignments", filter=Q(assignments__status=Assignment.COMPLETED)),
    )
    if category:
        items = items.filter(category__iexact=category)
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
    new_items = [
        Item(space=space, title=title, category=category, created_by=request.user)
        for category, title in entries
        if title.lower() not in existing
    ]
    for item in new_items:
        item.save()
    skipped = len(entries) - len(new_items)
    note = f" (skipped {skipped} already on the list)" if skipped else ""
    messages.success(request, f"Added {len(new_items)} item{'s' if len(new_items) != 1 else ''}{note}.")
    return redirect("items:list", space_id=space.id)


@membership_required
def edit(request, space, item_id):
    item = get_object_or_404(Item, pk=item_id, space=space)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
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
