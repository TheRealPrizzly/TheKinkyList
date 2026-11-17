"""Who gets a push notification, and what it says.

Notifications show on lock screens, so each one has a discreet wording that never names a wish.
People who turn on "Show wish titles in notifications" on their profile get the detailed one.

Sending waits until the database transaction commits, so a notification never announces
something that was rolled back, and a slow or failing Firebase can't break the request.
"""

import logging
from collections import defaultdict

from django.db import transaction
from django.urls import reverse

from accounts.models import profile_for

from . import fcm
from .models import Device

log = logging.getLogger(__name__)

TITLE_LIMIT = 60


def wishes_drawn(space, drawer, assignments):
    """Someone drew wishes and gave them to other members."""
    titles_by_user = defaultdict(list)
    users = {}
    for assignment in assignments:
        for user in assignment.assignees.all():
            if user.pk != drawer.pk:
                titles_by_user[user.pk].append(assignment.item.title)
                users[user.pk] = user
    name = profile_for(drawer).name
    url = reverse("assignments:list", args=[space.id])
    for user_id, titles in titles_by_user.items():
        count = len(titles)
        detailed = f"{name} drew {_quote(titles[0])} for you."
        if count > 1:
            detailed = f"{name} drew {_quote(titles[0])} and {count - 1} more for you."
        _queue(
            [users[user_id]],
            title="New on your to-do list",
            discreet=f"{name} drew {'something' if count == 1 else f'{count} wishes'} for you 💌",
            detailed=detailed,
            url=url,
        )


REPLY_WORDS = {
    "interested": "is interested in",
    "later": "would like to try someday",
    "not_for_me": "passed on",
}


def reply_given(assignment, user, kind):
    """An assignee answered a wish someone else drew for them."""
    requester = assignment.assigned_by
    if requester is None or requester.pk == user.pk:
        return
    name = profile_for(user).name
    _queue(
        [requester],
        title="New answer",
        discreet=f"{name} answered a wish you drew.",
        detailed=f"{name} {REPLY_WORDS.get(kind, 'answered')} {_quote(assignment.item.title)}.",
        url=reverse("assignments:list", args=[assignment.space_id]),
    )


def wish_completed(assignment, user):
    """Someone checked off a wish: tell the others on it and whoever drew it."""
    recipients = {u.pk: u for u in assignment.assignees.all()}
    if assignment.assigned_by is not None:
        recipients[assignment.assigned_by.pk] = assignment.assigned_by
    recipients.pop(user.pk, None)
    name = profile_for(user).name
    _queue(
        recipients.values(),
        title="Checked off 💞",
        discreet=f"{name} checked something off your list.",
        detailed=f"{name} checked off {_quote(assignment.item.title)}.",
        url=reverse("assignments:list", args=[assignment.space_id]) + "?tab=completed&who=all",
    )


def member_joined(space, user):
    others = [member for member in space.member_users() if member.pk != user.pk]
    name = profile_for(user).name
    _queue(
        others,
        title="New member",
        discreet=f"{name} joined your space.",
        detailed=f"{name} joined “{space.name}”.",
        url=reverse("spaces:dashboard", args=[space.id]),
    )


def _quote(title):
    if len(title) > TITLE_LIMIT:
        title = title[: TITLE_LIMIT - 1].rstrip() + "…"
    return f"“{title}”"


def _queue(users, *, title, discreet, detailed, url):
    if not fcm.is_configured():
        return
    messages = []
    for user in users:
        body = detailed if profile_for(user).notification_previews else discreet
        for token in Device.objects.filter(user=user).values_list("token", flat=True):
            messages.append((token, title, body, url))
    if messages:
        transaction.on_commit(lambda: deliver(messages))


def deliver(messages):
    for token, title, body, url in messages:
        try:
            fcm.send(token, title, body, url)
        except fcm.InvalidToken:
            Device.objects.filter(token=token).delete()
        except Exception:
            # Never let a notification problem surface to the person who triggered it.
            log.exception("Push notification failed")
