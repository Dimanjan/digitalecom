from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AuthenticationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_register_user(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_with_mismatched_passwords(self):
        url = reverse('register')
        data = self.user_data.copy()
        data['password2'] = 'differentpass'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_with_weak_password(self):
        url = reverse('register')
        data = self.user_data.copy()
        data['password'] = '123'
        data['password2'] = '123'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        url = reverse('get_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_user_profile_unauthenticated(self):
        url = reverse('get_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        user = User.objects.create_user(
            username='testuser',
            email='old@example.com',
            password='testpass123',
            first_name='Old',
            last_name='Name'
        )
        self.client.force_authenticate(user=user)
        url = reverse('update_user')
        data = {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'new@example.com'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.email, 'new@example.com')

    def test_refresh_token(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Get initial tokens
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        refresh_token = login_response.data['refresh']
        
        # Refresh the token
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {
            'refresh': refresh_token
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
