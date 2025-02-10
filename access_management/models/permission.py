from django.db import models
from .application import Application
import uuid


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}: {self.name}"
