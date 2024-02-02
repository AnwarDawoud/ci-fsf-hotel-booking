import unittest

from django.forms import ValidationError
from hotel_your_choice.forms import CustomRegistrationForm


class TestCustomRegistrationForm(unittest.TestCase):

    def test_clean_contact_number_with_plus(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {'contact_number': '+15551234'}
        contact_number = form.clean_contact_number()
        self.assertEqual(contact_number, '+15551234')

    def test_clean_contact_number_without_plus(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {'contact_number': '15551234'}
        with self.assertRaises(ValidationError):
            form.clean_contact_number()

    def test_clean_with_both_roles(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {'is_hotel_manager': True, 'is_client_user': True}
        with self.assertRaises(ValidationError):
            form.clean()

    def test_save_with_hotel_manager_role(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {'is_hotel_manager': True}
        user = form.save()
        self.assertTrue(user.is_hotel_manager)
        self.assertIn(user.groups.first().name, 'Hotel Managers')

    def test_save_with_client_user_role(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {'is_client_user': True}
        user = form.save()
        self.assertTrue(user.is_client_user)
        self.assertIn(user.groups.first().name, 'Users')
