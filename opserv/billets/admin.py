from django.contrib import admin

from .models import Billet
from .models import BilletOffice


@admin.register(Billet)
class BilletAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Billet objects.
    """

    save_as = True
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "office",
                    "game",
                    "rank",
                    "user",
                ),
            },
        ),
        ("Permissions", {"fields": ("permissions",)}),
        (
            "Information",
            {
                "fields": (
                    "created_by",  # Read-only field
                    "updated_by",  # Read-only field
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",  # Read-only field
                    "updated_at",  # Read-only field
                ),
            },
        ),
    )
    list_display = ["name", "office", "game", "user", "updated_at", "updated_by"]
    search_fields = ["name", "description"]
    list_filter = ["created_at", "updated_at"]
    filter_horizontal = ["permissions"]

    def save_model(self, request, obj, form, change):
        # Automatically set created_by and updated_by
        if not obj.pk:  # Object is being created
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        # Make fields read-only
        return ["created_by", "updated_by", "created_at", "updated_at"]

    def get_fields(self, request, obj=None):
        # Exclude fields during creation
        if not obj:  # Creating a new object
            return [
                field
                for field in super().get_fields(request, obj)
                if field not in ["created_by", "updated_by"]
            ]
        return super().get_fields(request, obj)


@admin.register(BilletOffice)
class BilletOfficeAdmin(admin.ModelAdmin):
    list_display = (
        "office_name",
        "office_description",
        "created_at",
        "updated_at",
    )
    search_fields = ("office_name", "office_description")
    list_filter = ("created_at", "updated_at")
