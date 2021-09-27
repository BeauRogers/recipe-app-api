from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
# in general, capital letters are used for constants


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test the Users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@londappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # the "**" is used to 'unwind' all the data from 'res'
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """TEST CREATING A USER THAT ALREADY EXISTS FAILS"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        # Bad request is expected because the user should already exist
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@londappdev.com',
            'password': 'pw',
            'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):

        """Test that a token is created for the user"""
        payload = {
            'email': 'test@londappdev.com',
            'password': 'testpass',
            'name': 'Test',
        }
        create_user(**payload)  # we created this in the data base
        res = self.client.post(TOKEN_URL, payload)
        """ Now we use HTTP to post to the URL, using the info that is now in
        the database"""
        print("\ntest_create_token_for_user: post response data")
        print(res)
        self.assertIn('token', res.data)
        # this checks that there is a key 'token' in the response data
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(
            email='test@londappdev.com',
            password='testpass',
            name='test'
            )
        payload = {  # now we'll post the wrong credentials
            'email': 'test@londappdev.com',
            'password': 'wrong',
            'name': 'test',
        }
        res = self.client.post(TOKEN_URL, payload)
        print("\ntest_create_token_invalid_credentials: post response data")
        print(res)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@londaonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        print("\ntest_create_token_no_user: post response data")
        print(res)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
