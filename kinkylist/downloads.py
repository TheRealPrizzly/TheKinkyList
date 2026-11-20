"""The Android app as a direct download from the website.

The APK isn't in the repository. It's built on a computer and uploaded to the server (see the
README, "Android download on the website"). Until it's there, the "Get the Android app" section
stays hidden and the download address answers 404. The apps never show the section (app.css).
"""

from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_safe

APK_TYPE = "application/vnd.android.package-archive"


def apk_size():
    """The APK's size in bytes, or None when it isn't on the server."""
    path = Path(settings.ANDROID_APK_FILE)
    return path.stat().st_size if path.is_file() else None


def android_app(request):
    """Context processor for templates/partials/get_app.html."""
    return {"android_apk_size": apk_size()}


@require_safe
@cache_control(no_cache=True)
def android_apk(request):
    path = Path(settings.ANDROID_APK_FILE)
    if not path.is_file():
        raise Http404("The Android app isn't available yet.")
    return FileResponse(path.open("rb"), as_attachment=True, filename="the-kinky-list.apk", content_type=APK_TYPE)
