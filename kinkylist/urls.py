from django.contrib import admin
from django.urls import include, path

from spaces.views import home

from . import pwa

urlpatterns = [
    path("", home, name="home"),
    path("manifest.webmanifest", pwa.manifest, name="manifest"),
    path("sw.js", pwa.service_worker, name="service_worker"),
    path("offline/", pwa.offline, name="offline"),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("spaces.urls")),
    path("push/", include("push.urls")),
    path("s/<int:space_id>/list/", include("items.urls")),
    path("s/<int:space_id>/play/", include("games.urls")),
    path("s/<int:space_id>/assignments/", include("assignments.urls")),
]
