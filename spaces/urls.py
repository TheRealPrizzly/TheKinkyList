from django.urls import path

from . import views

app_name = "spaces"

urlpatterns = [
    path("spaces/", views.index, name="index"),
    path("spaces/create/", views.create, name="create"),
    path("spaces/join/", views.join, name="join"),
    path("s/<int:space_id>/", views.dashboard, name="dashboard"),
    path("s/<int:space_id>/live/", views.dashboard_live, name="dashboard_live"),
    path("s/<int:space_id>/settings/", views.settings, name="settings"),
    path("s/<int:space_id>/leave/", views.leave, name="leave"),
]
