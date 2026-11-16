from django.contrib import admin

from .models import Category, Item, Truth


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "spice", "space", "archived"]
    list_filter = ["archived", "spice"]
    search_fields = ["title", "categories__name"]
    filter_horizontal = ["categories"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "space"]
    search_fields = ["name"]


@admin.register(Truth)
class TruthAdmin(admin.ModelAdmin):
    list_display = ["text", "spice", "space"]
    list_filter = ["spice"]
    search_fields = ["text"]
