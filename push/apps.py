from django.apps import AppConfig


class PushConfig(AppConfig):
    name = "push"
    verbose_name = "Push notifications"

    def ready(self):
        from . import signals  # noqa: F401
