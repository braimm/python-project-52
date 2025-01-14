from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model


# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=150, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='author'
    )
    status = models.ForeignKey(
        Status,
        blank=False,
        on_delete=models.PROTECT,
        related_name='status'
    )
    executor = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='executor'
    )
    labels = models.ManyToManyField(Label, blank=True, related_name='labels')
