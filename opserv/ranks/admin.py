from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import Rank


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Ranks.
    """

    save_as = True
    fieldsets = (
        (None, {"fields": ("name", "description", "color_hex", "order")}),
        ("Image", {"fields": ("icon", "fs_icon")}),
        ("Permissions", {"fields": ("is_active", "is_default", "permissions")}),
        ("Users", {"classes": ("collapse",), "fields": ("users_display",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    list_display = [
        "name",
        "is_default_display",
        "description",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["created_at", "updated_at", "users_display"]
    search_fields = ["name", "description"]
    filter_horizontal = ["permissions"]

    @admin.display(
        description="Users",
    )
    def users_display(self, obj):
        if obj and obj.users.exists():
            return format_html_join(
                mark_safe("<br>"),
                "{}",
                ((user.username,) for user in obj.users.all()),
            )
        return "No users assigned"

    @admin.display(
        description="Default Rank",
        boolean=True,
        ordering="is_default",
    )
    def is_default_display(self, obj):
        return obj.is_default
