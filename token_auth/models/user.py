from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    manager = models.ForeignKey(
        "self",
        verbose_name=_("Manager"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user",
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else f"{self.username}"
        )
