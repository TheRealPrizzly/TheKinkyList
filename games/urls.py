from django.urls import path

from . import views

app_name = "games"

urlpatterns = [
    path("", views.index, name="index"),
    path("done/<int:session_id>/", views.done, name="done"),
    path("<slug:slug>/", views.play, name="play"),
    path("<slug:slug>/feed/", views.feed, name="feed"),
    path("<slug:slug>/assign/", views.assign, name="assign"),
]
