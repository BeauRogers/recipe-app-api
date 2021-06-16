from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    # Let's make a set up function
    def setUp(self):
        self.client = Client()
        print("BACR setUp")
        print(self.client)
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londaonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londappdev.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        print("BACR test_users_listed")
        print(url)
        res = self.client.get(url)  # res=response

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        print("BACR test_user_change_page")
        print(url)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)  # HTTP 200 = OK

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        print("BACR test_create_user_page")
        print(url)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
