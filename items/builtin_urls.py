from django.urls import path

from . import builtin_views

app_name = "builtins"

urlpatterns = [
    path("", builtin_views.index, name="index"),
    path("<slug:tab>/", builtin_views.page, name="page"),
    path("entry/<int:entry_id>/", builtin_views.row, name="row"),
    path("entry/<int:entry_id>/edit/", builtin_views.edit, name="edit"),
    path("entry/<int:entry_id>/intensity/", builtin_views.set_spice, name="spice"),
    path("entry/<int:entry_id>/reviewed/", builtin_views.toggle_reviewed, name="reviewed"),
    path("entry/<int:entry_id>/remove/", builtin_views.remove, name="remove"),
]
