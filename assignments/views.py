from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from spaces.decorators import membership_required

from .models import Assignment

TABS = {"active": Assignment.ACTIVE, "completed": Assignment.COMPLETED}


def list_context(request, space, params):
    tab = params.get("tab") if params.get("tab") in TABS else "active"
    who = "all" if params.get("who") == "all" else "mine"
    assignments = (
        Assignment.objects.filter(space=space, status=TABS[tab])
        .select_related("item", "session", "completed_by__profile")
        .prefetch_related("assignees__profile")
    )
    if who == "mine":
        assignments = assignments.filter(assignees=request.user)
    if tab == "completed":
        assignments = assignments.order_by("-completed_at")
    assignments = list(assignments)
    for assignment in assignments:
        assignment.mine = request.user in assignment.assignees.all()
    return {"space": space, "tab": tab, "who": who, "assignments": assignments}


@membership_required
def assignment_list(request, space):
    context = list_context(request, space, request.GET)
    if request.headers.get("HX-Request"):
        return render(request, "assignments/_list.html", context)
    return render(request, "assignments/list.html", {**context, "nav": "assignments"})


def respond(request, space, celebrate=False):
    if request.headers.get("HX-Request"):
        response = render(request, "assignments/_list.html", list_context(request, space, request.POST))
        if celebrate:
            response["HX-Trigger"] = "celebrate"
        return response
    url = reverse("assignments:list", kwargs={"space_id": space.id})
    return redirect(f"{url}?tab={request.POST.get('tab', 'active')}&who={request.POST.get('who', 'mine')}")


@membership_required
@require_POST
def complete(request, space, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id, space=space, status=Assignment.ACTIVE)
    if not assignment.is_assignee(request.user):
        return HttpResponseForbidden("Only the people this is assigned to can check it off.")
    assignment.complete(request.user, request.POST.get("note", "")[:1000])
    if not request.headers.get("HX-Request"):
        messages.success(request, f"“{assignment.item.title}” is checked off. 💞")
    return respond(request, space, celebrate=True)


@membership_required
@require_POST
def release(request, space, assignment_id):
    """Put an active item back on the list (e.g. it was drawn but isn't happening)."""
    assignment = get_object_or_404(Assignment, pk=assignment_id, space=space, status=Assignment.ACTIVE)
    if not (assignment.is_assignee(request.user) or assignment.assigned_by_id == request.user.id):
        return HttpResponseForbidden("Only the assignees or whoever drew it can put it back.")
    assignment.delete()
    if not request.headers.get("HX-Request"):
        messages.success(request, f"“{assignment.item.title}” is back on the list.")
    return respond(request, space)
