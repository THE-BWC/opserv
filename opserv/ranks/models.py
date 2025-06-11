from django.db import models
from tinymce.models import HTMLField

from config.settings import base

user_model = base.AUTH_USER_MODEL


# Create your models here.
class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = HTMLField(
        blank=True,
        null=True,
        help_text="A detailed description of the rank.",
    )
    icon = models.ImageField(upload_to="ranks/icon/")
    fs_icon = models.ImageField(upload_to="ranks/fs/")
    color_hex = models.CharField(max_length=7, default="#FFFFFF")
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(
        user_model,
        related_name="ranks",
        blank=True,
        help_text="Users who have this rank.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "is_active"],
                name="unique_active_rank_name",
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.color_hex.startswith("#"):
            self.color_hex = "#" + self.color_hex
        super().save(*args, **kwargs)
