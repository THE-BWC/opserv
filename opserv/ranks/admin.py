from django.contrib import admin

from .models import Rank


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    exclude = ["users"]

    list_display = ["name", "description", "created_at", "updated_at"]
