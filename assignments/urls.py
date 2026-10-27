from django.urls import path

from . import views

app_name = "assignments"

urlpatterns = [
    path("", views.assignment_list, name="list"),
    path("<int:assignment_id>/complete/", views.complete, name="complete"),
    path("<int:assignment_id>/release/", views.release, name="release"),
]
