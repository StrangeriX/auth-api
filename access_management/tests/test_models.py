from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models.access import Access
from ..models.application import Application
from ..models.permission import Permission
from ..models.access_permission import AccessPermission
from .test_setup import TestSetUp


class ApplicationModelTests(TestSetUp):
    def test_application_creation(self):
        """Test application creation with valid data"""
        self.assertEqual(self.application.name, "Test Application")
        self.assertEqual(self.application.description, "Test application description")

    def test_application_str_representation(self):
        """Test application string representation"""
        self.assertEqual(str(self.application), "Application: Test Application")

    def test_application_name_max_length(self):
        """Test application name max length validation"""
        long_name = "x" * 256  # Exceeds max_length
        with self.assertRaises(ValidationError):
            app = Application(name=long_name, description="Test")
            app.full_clean()


class PermissionModelTests(TestSetUp):
    def test_permission_creation(self):
        """Test permission creation with valid data"""
        self.assertEqual(self.permission.name, "Test Permission")
        self.assertEqual(self.permission.code, "1000")

    def test_permission_str_representation(self):
        """Test permission string representation"""
        self.assertEqual(str(self.permission), "1000: Test Permission")

    def test_unique_code_constraint(self):
        """Test that permission code must be unique"""
        with self.assertRaises(ValidationError):
            duplicate_permission = Permission(
                name="Another Permission",
                code="1000",  # Same code as existing permission
            )
            duplicate_permission.full_clean()


class AccessModelTests(TestSetUp):
    def test_access_creation(self):
        """Test access creation with valid data"""
        self.assertEqual(self.access.user, self.user)
        self.assertEqual(self.access.application, self.application)
        self.assertIsNone(self.access.organization_unit)

    def test_access_with_organization(self):
        """Test access creation with organization unit"""
        self.assertEqual(self.access_with_organization.user, self.user)
        self.assertEqual(self.access_with_organization.application, self.application)
        self.assertEqual(self.access_with_organization.organization_unit, self.org_unit)

    def test_unique_access_constraint(self):
        """Test that user-application-organization combination must be unique"""
        with self.assertRaises(ValidationError):
            duplicate_access = Access(
                user=self.user,
                application=self.application,
                organization_unit=self.org_unit,
            )
            duplicate_access.full_clean()


class AccessPermissionModelTests(TestSetUp):
    def test_access_permission_creation(self):
        """Test access permission creation with valid data"""
        self.assertEqual(self.access_permission.access, self.access)
        self.assertEqual(self.access_permission.permission, self.permission)

    def test_access_permission_with_organization(self):
        """Test access permission with organization unit"""
        self.assertEqual(
            self.access_permission_with_organization.access,
            self.access_with_organization,
        )
        self.assertEqual(
            self.access_permission_with_organization.permission, self.permission
        )

    def test_unique_access_permission_constraint(self):
        """Test that access-permission combination must be unique"""
        with self.assertRaises(ValidationError):
            duplicate_access_permission = AccessPermission(
                access=self.access, permission=self.permission
            )
            duplicate_access_permission.full_clean()

    def test_cascade_delete(self):
        """Test that deleting access deletes related access permissions"""
        access_permission_id = self.access_permission.id
        self.access.delete()
        self.assertFalse(
            AccessPermission.objects.filter(id=access_permission_id).exists()
        )
