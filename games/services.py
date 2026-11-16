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


@transaction.atomic
def record_dare(space, game, user, item, player, done, session=None):
    """Truth or Dare: give a dare to the player, either already done or saved to their To-do.

    The first dare of a night starts a session; later ones join it.
    """
    if session is None:
        session = GameSession.objects.create(space=space, game_type=game.slug, created_by=user)
    assignment = Assignment.objects.create(space=space, item=item, session=session, assigned_by=user)
    assignment.assignees.set([player])
    if done:
        assignment.complete(player)
    return session
