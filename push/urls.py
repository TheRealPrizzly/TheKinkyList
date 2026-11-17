from django.urls import path

from . import views

app_name = "push"

urlpatterns = [
    path("devices/", views.register_device, name="register_device"),
]
