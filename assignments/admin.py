from django.contrib import admin

from .models import Assignment, GameSession, Reply


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["item", "status", "space", "created_at", "completed_at"]
    list_filter = ["status"]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ["item", "user", "kind", "requester", "created_at", "seen"]
    list_filter = ["kind", "seen"]


admin.site.register(GameSession)
