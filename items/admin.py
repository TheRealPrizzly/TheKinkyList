from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "spice", "space", "archived"]
    list_filter = ["archived", "spice"]
    search_fields = ["title", "category"]
