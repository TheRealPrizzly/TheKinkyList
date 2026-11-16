from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.item_list, name="list"),
    path("bulk/", views.bulk_add, name="bulk"),
    path("clear/", views.clear, name="clear"),
    path("<int:item_id>/edit/", views.edit, name="edit"),
    path("<int:item_id>/archive/", views.toggle_archive, name="archive"),
    path("truths/add/", views.add_truth, name="add_truth"),
    path("truths/<int:truth_id>/delete/", views.delete_truth, name="delete_truth"),
]
