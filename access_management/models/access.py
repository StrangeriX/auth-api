from django.db import models
from .application import Application
from token_auth.models.user import User
from token_auth.models.organization_unit import OrganizationUnit
from django.utils.timezone import now


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    organization_unit = models.ForeignKey(
        OrganizationUnit, on_delete=models.CASCADE, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    date_from = models.DateField(default=now)
    date_to = models.DateField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ["user", "application", "organization_unit"]

    def __str__(self):
        return f"{self.user} - {self.application}"
