from rest_framework.test import APITestCase
from ..models.access import Access
from ..models.application import Application
from ..models.permission import Permission
from ..models.access_permission import AccessPermission
from token_auth.models.user import User
from token_auth.models.organization_unit import OrganizationUnit


class TestSetUp(APITestCase):
    def setUp(self):
        super().setUp()  # Call parent setup first

        # Create test data
        self.user = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="employee123",
            first_name="Employee",
            last_name="Test",
        )
        self.org_unit = OrganizationUnit.objects.create(
            name="Test Department", description="Test department description"
        )
        self.application: Application = Application.objects.create(
            name="Test Application", description="Test application description"
        )
        self.permission: Permission = Permission.objects.create(
            name="Test Permission", code="1000", application=self.application
        )
        self.access = Access.objects.create(
            user=self.user, application=self.application
        )
        self.access_with_organization = Access.objects.create(
            user=self.user,
            application=self.application,
            organization_unit=self.org_unit,
        )

        self.access_permission = AccessPermission.objects.create(
            access=self.access, permission=self.permission
        )
        self.access_permission_with_organization = AccessPermission.objects.create(
            access=self.access_with_organization,
            permission=self.permission,
        )
