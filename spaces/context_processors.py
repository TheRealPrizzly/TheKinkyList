def current_space(request):
    space = getattr(request, "space", None)
    return {"members": list(space.member_users()) if space else []}
