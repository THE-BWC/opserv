from django.db import models
from tinymce.models import HTMLField

from config.settings import base
from opserv.games.models import Game
from opserv.ranks.models import Rank

user_model = base.AUTH_USER_MODEL


class BilletOffice(models.Model):
    office_name = models.CharField(max_length=255)
    office_description = HTMLField(
        blank=True,
        null=True,
        help_text="A brief description of the office.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Billet Office"
        verbose_name_plural = "Billet Offices"
        ordering = ["-created_at"]

    def __str__(self):
        return self.office_name if self.office_name else "Unnamed Office"


class Billet(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField(
        blank=True,
        null=True,
        help_text="A brief description of the billet.",
    )
    is_active = models.BooleanField(default=True)

    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name="billets",
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.PROTECT,
        related_name="billets",
    )
    office = models.ForeignKey(
        BilletOffice,
        on_delete=models.PROTECT,
        related_name="billets",
    )

    user = models.ForeignKey(
        user_model,
        on_delete=models.SET_NULL,
        related_name="billets",
        verbose_name="User",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="billets_created",
        verbose_name="Created By",
    )
    updated_by = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="billets_updated",
        verbose_name="Updated By",
    )

    class Meta:
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name if self.name else "Unnamed Billet"

    def save(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        if not self.pk and request:
            self.created_by = request.user
        if request:
            self.updated_by = request.user
        super().save(*args, **kwargs)

        # Backfill the user's billet field
        if self.user:
            if self.user.billet != self:
                self.user.billet = self
                self.user.save()
        else:
            # Remove the reference if user is set to None
            for user in self.user_set.all():
                if user.billet == self:
                    user.billet = None
                    user.save()
