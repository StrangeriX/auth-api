from django.db import models
from .access import Access
from .permission import Permission


class AccessPermission(models.Model):
    access = models.ForeignKey(Access, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.access.user} - {self.permission.name}"

    class Meta:
        unique_together = ["access", "permission"]
