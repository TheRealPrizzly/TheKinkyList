from django.db import transaction

from assignments.models import Assignment, GameSession


@transaction.atomic
def create_assignments(space, game, user, items, assignee_ids_by_item):
    """Record a game session and one active assignment per picked item."""
    session = GameSession.objects.create(space=space, game_type=game.slug, created_by=user)
    for item in items:
        assignment = Assignment.objects.create(space=space, item=item, session=session, assigned_by=user)
        assignment.assignees.set(assignee_ids_by_item[item.id])
    return session
