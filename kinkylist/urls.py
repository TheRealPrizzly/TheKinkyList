from django.contrib import admin
from django.urls import include, path

from spaces.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("spaces.urls")),
    path("s/<int:space_id>/list/", include("items.urls")),
    path("s/<int:space_id>/play/", include("games.urls")),
    path("s/<int:space_id>/assignments/", include("assignments.urls")),
]
