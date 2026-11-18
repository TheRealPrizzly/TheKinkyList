from . import google as google_signin


def google(request):
    return {"google_enabled": google_signin.is_configured()}
