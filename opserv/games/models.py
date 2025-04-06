from django.db import models

from config.settings import base

user_model = base.AUTH_USER_MODEL


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

    def __str__(self):
        return self.name
