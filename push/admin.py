from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["user", "platform", "created_at", "updated_at"]
    list_filter = ["platform"]
    readonly_fields = ["user", "token", "platform", "created_at", "updated_at"]
