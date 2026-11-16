from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    # The Kinky List
    path("", views.item_list, name="list"),
    path("bulk/", views.bulk_add, name="bulk"),
    path("<int:item_id>/edit/", views.edit, name="edit"),
    path("<int:item_id>/archive/", views.toggle_archive, name="archive"),
    path("<int:item_id>/delete/", views.delete_item, name="delete"),
    # Truth or Dare
    path("truth-or-dare/", views.truth_or_dare, name="truth_or_dare"),
    path("truth-or-dare/import/", views.import_truth_or_dare, name="import_truth_or_dare"),
    path("truths/<int:truth_id>/delete/", views.delete_truth, name="delete_truth"),
    path("dares/<int:dare_id>/delete/", views.delete_dare, name="delete_dare"),
    # Would you rather
    path("would-you-rather/", views.would_you_rather, name="would_you_rather"),
    path("would-you-rather/import/", views.import_questions, name="import_questions"),
    path("questions/<int:question_id>/delete/", views.delete_question, name="delete_question"),
    # Every list
    path("<slug:list_slug>/generate/", views.generate, name="generate"),
    path("<slug:list_slug>/clear/", views.clear, name="clear"),
]
