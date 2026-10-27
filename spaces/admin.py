from django.contrib import admin

from .models import Membership, Space


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "invite_code", "created_at"]
    inlines = [MembershipInline]
