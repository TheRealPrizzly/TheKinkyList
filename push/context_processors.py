from . import fcm


def push(request):
    """Pages only load static/js/push.js when the server can actually send notifications."""
    return {"push_enabled": fcm.is_configured()}
