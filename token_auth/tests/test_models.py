from django.test import TestCase
from django.core.exceptions import ValidationError
from token_auth.models.user import User
from token_auth.models.organization_unit import OrganizationUnit
from .test_setup import TestSetUp


class UserModelTests(TestSetUp):
    def test_user_creation(self):
        """Test user creation with valid data"""
        self.assertEqual(self.user.username, "employee")
        self.assertEqual(self.user.email, "employee@test.com")
        self.assertEqual(self.user.first_name, "Employee")
        self.assertEqual(self.user.last_name, "Test")
        self.assertEqual(self.user.manager, self.manager)

    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), "Employee Test")

        # Test user without first and last name
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="test123"
        )
        self.assertEqual(str(user), "testuser")

    def test_user_manager_relationship(self):
        """Test manager-employee relationship"""
        self.assertEqual(self.user.manager, self.manager)
        self.assertTrue(self.manager.user.filter(id=self.user.id).exists())

    def test_user_guid_generation(self):
        """Test that GUID is automatically generated"""
        self.assertIsNotNone(self.user.guid)
        self.assertIsNotNone(self.manager.guid)
        self.assertNotEqual(self.user.guid, self.manager.guid)


class OrganizationUnitModelTests(TestSetUp):
    def test_org_unit_creation(self):
        """Test organization unit creation with valid data"""
        self.assertEqual(self.org_unit_parent.name, "Parent Department")
        self.assertEqual(
            self.org_unit_parent.description, "Parent department description"
        )
        self.assertIsNone(self.org_unit_parent.parent)

    def test_org_unit_parent_child_relationship(self):
        """Test parent-child relationship between organization units"""
        self.assertEqual(self.org_unit_child.parent, self.org_unit_parent)
        self.assertTrue(
            OrganizationUnit.objects.filter(
                parent=self.org_unit_parent, id=self.org_unit_child.id
            ).exists()
        )

    def test_org_unit_str_representation(self):
        """Test organization unit string representation"""
        org_unit = OrganizationUnit.objects.create(
            name="Test Department", description="Test description"
        )
        self.assertEqual(str(org_unit), "Test Department")

    def test_org_unit_name_max_length(self):
        """Test organization unit name max length validation"""
        long_name = "x" * 256  # Exceeds max_length of 255
        with self.assertRaises(ValidationError):
            org_unit = OrganizationUnit(name=long_name, description="Test description")
            org_unit.full_clean()

    def test_cascade_delete(self):
        """Test that deleting parent org unit deletes children"""
        # Create a new child org unit
        child = OrganizationUnit.objects.create(
            name="Test Child",
            description="Test child description",
            parent=self.org_unit_parent,
        )

        # Delete parent
        self.org_unit_parent.delete()

        # Verify child was deleted
        self.assertFalse(OrganizationUnit.objects.filter(id=child.id).exists())
