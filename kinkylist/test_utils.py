from django.contrib.auth import get_user_model

from items.models import Item
from spaces.models import Membership, Space


def make_user(username, display_name=""):
    user = get_user_model().objects.create_user(username=username, password="pw-for-tests-123")
    if display_name:
        user.profile.display_name = display_name
        user.profile.save()
    return user


def make_space(owner, *members, name="Us"):
    space = Space.objects.create(name=name, created_by=owner)
    Membership.objects.create(space=space, user=owner, role=Membership.OWNER)
    for member in members:
        Membership.objects.create(space=space, user=member)
    return space


def make_items(space, *titles, categories=()):
    items = [Item.objects.create(space=space, title=title) for title in titles]
    for item in items:
        item.set_categories(categories)
    return items
