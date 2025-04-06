from django.db import models

from config.settings import base

user_model = base.AUTH_USER_MODEL


# Create your models here.
class OperationType(models.Model):
    """
    OperationType model to define the type of operation.
    """

    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=10)
    color_hex = models.CharField(max_length=7)
    live_fire = models.BooleanField(default=False)
    retired = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Operation(models.Model):
    """
    Operation model to define the operation.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    type_id = models.ForeignKey(OperationType, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    leader_user_id = models.ForeignKey(
        user_model,
        related_name="operation_leader",
        on_delete=models.PROTECT,
    )
    aar_notes = models.TextField(blank=True)
    is_opsec = models.BooleanField(default=False)
    discord_voice_channel = models.CharField(max_length=255, blank=True)
    discord_event_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
