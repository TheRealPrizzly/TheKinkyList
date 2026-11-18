from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    path("profile/google/disconnect/", views.google_disconnect, name="google_disconnect"),
    path("google/start/", views.google_start, name="google_start"),
    path("google/callback/", views.google_callback, name="google_callback"),
    path("google/token/", views.google_token, name="google_token"),
    path("signup/google/", views.google_signup, name="google_signup"),
    path("privacy/", views.privacy, name="privacy"),
]
