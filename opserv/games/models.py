from django.db import models
from django.db.models import Count
from django.db.models import Prefetch
from django.db.models import Q
from django.utils import timezone

from config.settings import base

user_model = base.AUTH_USER_MODEL


class GameQuerySet(models.QuerySet):
    """
    Custom QuerySet for the Game model.
    """

    def with_upcoming_operations(self):
        """
        Returns games with upcoming operations.
        """
        from opserv.operations.models import Operation

        now = timezone.now()
        upcoming_ops = Operation.objects.filter(start_date__gte=now).select_related(
            "type_id",
        )
        return (
            self.annotate(
                upcoming_ops_count=Count(
                    "operation",
                    filter=Q(operation__start_date__gte=now),
                ),
            )
            .filter(
                upcoming_ops_count__gt=0,
            )
            .prefetch_related(
                Prefetch(
                    "operation_set",
                    queryset=upcoming_ops,
                    to_attr="upcoming_operations",
                ),
            )
        )


class Game(models.Model):
    """
    Model representing a game.
    """

    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=10, unique=True)
    icon = models.ImageField(upload_to="games/")
    retired = models.BooleanField(default=False)
    opsec = models.BooleanField(default=False)
    opsec_user_group = models.IntegerField(null=True, blank=True, default=None)
    opsec_discord_role = models.CharField(max_length=255, blank=True, default="")
    objects = GameQuerySet.as_manager()

    def __str__(self):
        return self.name
