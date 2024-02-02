import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'hotels_booking.settings'

import django
django.setup() 

import unittest
from hotel_your_choice.models import CustomUser
from django.core.exceptions import ValidationError


class TestCustomUser(unittest.TestCase):

    def setUp(self):
        # Create any initial data or setup required for the tests
        pass

    def tearDown(self):
        # Clean up any data or resources created during the tests
        CustomUser.objects.all().delete()

    def test_custom_user_saved_with_valid_data(self):
        user = CustomUser(username='test1', email='test1@example.com', password='password123')
        user.save()
        self.assertIsNotNone(user.id)

    def test_custom_user_raises_error_with_invalid_data(self):
        user = CustomUser(username='')  # Empty username to trigger the validation error
        with self.assertRaises(ValidationError):
            user.full_clean()  # Validate the user without saving

    def test_generate_reset_token(self):
        user = CustomUser(username='test2', email='test2@example.com', password='password123')
        user.save()
        token = user.generate_reset_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    def test_fields(self):
        user = CustomUser(username='test3', email='test3@example.com', password='password123')
        user.save()
        self.assertEqual(user.username, 'test3')
