from django.contrib import admin

# Register your models here.
from .models.access import Access
from .models.application import Application
from .models.access_permission import AccessPermission
from .models.permission import Permission

admin.site.register(Access)
admin.site.register(Application)
admin.site.register(AccessPermission)
admin.site.register(Permission)
