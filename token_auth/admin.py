from django.contrib import admin

# Register your models here.
from .models.organization_unit import OrganizationUnit
from .models.user import User

admin.site.register(OrganizationUnit)
admin.site.register(User)
