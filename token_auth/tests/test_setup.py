from rest_framework.test import APITestCase
from django.urls import reverse
from token_auth.models.user import User
from token_auth.models.organization_unit import OrganizationUnit


class TestSetUp(APITestCase):
    def setUp(self):
        """
        Set up test data before each test method
        """
        # Create organization units
        self.org_unit_parent = OrganizationUnit.objects.create(
            name="Parent Department", description="Parent department description"
        )

        self.org_unit_child = OrganizationUnit.objects.create(
            name="Child Department",
            description="Child department description",
            parent=self.org_unit_parent,
        )

        # Create test users
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="manager123",
            first_name="Manager",
            last_name="Test",
        )

        self.user = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="employee123",
            first_name="Employee",
            last_name="Test",
            manager=self.manager,
        )

        # # Define common URLs that will be used in tests
        # self.login_url = reverse("token_obtain_pair")
        # self.user_list_url = reverse("user-list")
        # self.org_unit_list_url = reverse("organization-unit-list")

        # Define test data
        self.user_data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "newuser123",
            "first_name": "New",
            "last_name": "User",
        }

        self.org_unit_data = {
            "name": "New Department",
            "description": "New department description",
        }

        return super().setUp()
