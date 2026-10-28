from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from accounts.models import profile_for
from assignments.models import Assignment
from games.registry import GAMES

from .decorators import membership_required
from .forms import JoinForm, SpaceForm
from .models import Membership, Space, generate_invite_code

RING_RADIUS = 52
RING_CIRCUMFERENCE = 2 * 3.14159 * RING_RADIUS


def home(request):
    if not request.user.is_authenticated:
        return render(request, "landing.html", {"games": GAMES.values()})
    last_space = profile_for(request.user).last_space
    if last_space and last_space.has_member(request.user):
        return redirect("spaces:dashboard", space_id=last_space.id)
    return redirect("spaces:index")


@login_required
def index(request):
    memberships = Membership.objects.filter(user=request.user).select_related("space").order_by("joined_at")
    return render(
        request,
        "spaces/index.html",
        {"memberships": memberships, "create_form": SpaceForm(), "join_form": JoinForm()},
    )


@login_required
@require_POST
def create(request):
    form = SpaceForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            space = form.save(commit=False)
            space.created_by = request.user
            space.save()
            Membership.objects.create(space=space, user=request.user, role=Membership.OWNER)
        messages.success(request, f"“{space.name}” is ready. Share code {space.invite_code} with your partner.")
        return redirect("spaces:dashboard", space_id=space.id)
    messages.error(request, "Please give your space a name.")
    return redirect("spaces:index")


@login_required
@require_POST
def join(request):
    form = JoinForm(request.POST)
    if form.is_valid():
        space = form.space
        _, created = Membership.objects.get_or_create(space=space, user=request.user)
        messages.success(request, f"You joined “{space.name}”." if created else f"You're already in “{space.name}”.")
        return redirect("spaces:dashboard", space_id=space.id)
    for error in form.errors.get("code", []):
        messages.error(request, error)
    return redirect("spaces:index")


def dashboard_context(space):
    items = space.items.filter(archived=False)
    total = items.count()
    done = items.filter(assignments__status=Assignment.COMPLETED).distinct().count()
    percent = round(done * 100 / total) if total else 0
    active = list(
        Assignment.objects.filter(space=space, status=Assignment.ACTIVE)
        .select_related("item")
        .prefetch_related("item__categories", "assignees")
    )
    columns = [
        {"user": member, "assignments": [a for a in active if member in a.assignees.all()]}
        for member in space.member_users()
    ]
    memories = (
        Assignment.objects.filter(space=space, status=Assignment.COMPLETED)
        .select_related("item", "completed_by")
        .prefetch_related("item__categories")
        .order_by("-completed_at")[:4]
    )
    return {
        "total": total,
        "done": done,
        "active_count": len(active),
        "percent": percent,
        "ring_circumference": f"{RING_CIRCUMFERENCE:.1f}",
        "ring_offset": f"{RING_CIRCUMFERENCE * (1 - percent / 100):.1f}",
        "columns": columns,
        "memories": memories,
    }


@membership_required
def dashboard(request, space):
    context = {"space": space, "games": GAMES.values(), "nav": "home", **dashboard_context(space)}
    return render(request, "spaces/dashboard.html", context)


@membership_required
def dashboard_live(request, space):
    return render(request, "spaces/_live.html", {"space": space, **dashboard_context(space)})


@membership_required
def settings(request, space):
    is_owner = request.membership.role == Membership.OWNER
    form = SpaceForm(instance=space)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "rename":
            form = SpaceForm(request.POST, instance=space)
            if form.is_valid():
                form.save()
                messages.success(request, "Space renamed.")
                return redirect("spaces:settings", space_id=space.id)
        elif action == "new_code" and is_owner:
            space.invite_code = generate_invite_code()
            space.save(update_fields=["invite_code"])
            messages.success(request, "New invite code created. The old one no longer works.")
            return redirect("spaces:settings", space_id=space.id)
    memberships = space.memberships.select_related("user__profile").order_by("joined_at")
    return render(
        request,
        "spaces/settings.html",
        {"space": space, "form": form, "memberships": memberships, "is_owner": is_owner, "nav": "settings"},
    )


@membership_required
@require_POST
def leave(request, space):
    with transaction.atomic():
        was_owner = request.membership.role == Membership.OWNER
        request.membership.delete()
        remaining = space.memberships.order_by("joined_at")
        if not remaining.exists():
            space.delete()
        elif was_owner and not remaining.filter(role=Membership.OWNER).exists():
            heir = remaining.first()
            heir.role = Membership.OWNER
            heir.save(update_fields=["role"])
    messages.success(request, f"You left “{space.name}”.")
    return redirect("spaces:index")
