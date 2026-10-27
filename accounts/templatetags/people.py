from django import template

from accounts.models import profile_for

register = template.Library()


@register.inclusion_tag("partials/avatar.html")
def avatar(user, size="md"):
    profile = profile_for(user)
    return {"profile": profile, "size": size}


@register.filter
def display_name(user):
    return profile_for(user).name
