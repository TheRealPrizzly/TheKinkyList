from django.contrib import admin

from .models import Assignment, GameSession


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["item", "status", "space", "created_at", "completed_at"]
    list_filter = ["status"]


admin.site.register(GameSession)
