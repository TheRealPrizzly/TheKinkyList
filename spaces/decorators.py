from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import Http404

from accounts.models import profile_for

from .models import Membership


def membership_required(view):
    """Resolve `space_id` to a Space the user belongs to (404 otherwise) and pass it as `space`."""

    @wraps(view)
    def wrapper(request, space_id, *args, **kwargs):
        membership = Membership.objects.select_related("space").filter(space_id=space_id, user=request.user).first()
        if membership is None:
            raise Http404("Space not found")
        space = membership.space
        request.space = space
        request.membership = membership
        profile = profile_for(request.user)
        if profile.last_space_id != space.id:
            profile.last_space = space
            profile.save(update_fields=["last_space"])
        return view(request, space, *args, **kwargs)

    return login_required(wrapper)
