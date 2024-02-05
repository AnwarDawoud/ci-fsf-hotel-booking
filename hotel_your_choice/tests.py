# tests case
import os
import django
import unittest

from django.test import TestCase
from .models import CustomUser, Hotel, Booking
from django.urls import reverse
from datetime import datetime, timedelta
from django.forms import ValidationError
from hotel_your_choice.forms import CustomRegistrationForm
from django.core.exceptions import ValidationError


class HotelYourChoiceTests(TestCase):
    def setUp(self):
        # Create a custom user using create_user method from CustomUser manager
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            is_hotel_manager=True,  # Adjust as needed
        )

        # Create a hotel using the custom user as the manager
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test address",
            night_rate=100.0,
            capacity=10,
            room_number=5,
            main_photo="path/to/main_photo.jpg",  # Adjust as needed
            manager=self.user,  # Use the custom user as the manager
        )

        # Create a booking for the hotel
        check_in_date = datetime.now().date()
        check_out_date = check_in_date + timedelta(days=5)
        self.booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guests=2,
            status="active",
        )

    def test_hotel_model(self):
        self.assertEqual(str(self.hotel), "Test Hotel")

    def test_view_hotels(self):
        response = self.client.get(reverse("hotel_your_choice:view_hotels"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hotel")

    # New test method
    def test_check_in_date_in_future(self):
        """
        Test if the check-in date for a booking is in the future.
        """
        future_check_in_date = datetime.now().date() + timedelta(days=3)
        future_check_out_date = future_check_in_date + timedelta(days=5)
        future_booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            check_in_date=future_check_in_date,
            check_out_date=future_check_out_date,
            guests=2,
            status="active",
        )
        self.assertTrue(future_booking.check_in_date > datetime.now().date())

    def test_booking_check_in_date(self):
        self.assertEqual(self.booking.check_in_date, datetime.now().date())

    def test_booking_check_out_date(self):
        expected_check_out_date = (
            self.booking.check_in_date + timedelta(days=5)
        )
        self.assertEqual(self.booking.check_out_date, expected_check_out_date)

    def test_booking_guests_count(self):
        self.assertEqual(self.booking.guests, 2)

    def test_booking_status_active(self):
        self.assertEqual(self.booking.status, "active")

    def test_invalid_guests_count(self):
        """
        Test if an invalid number of guests for a booking raises an exception.
        """
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                hotel=self.hotel,
                check_in_date=datetime.now().date(),
                check_out_date=datetime.now().date() + timedelta(days=5),
                guests=-1,  # Invalid number of guests
                status="active",
            )

    def test_booking_status_cancelled(self):
        """
        Test if a booking can be cancelled successfully.
        """
        # Create a new booking
        new_booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            check_in_date=datetime.now().date(),
            check_out_date=datetime.now().date() + timedelta(days=5),
            guests=2,
            status="active",
        )

        # Cancel the booking
        new_booking.cancel()

        # Check if the status is now 'cancelled'
        self.assertEqual(new_booking.status, "cancelled")


class TestCustomRegistrationForm(unittest.TestCase):
    def test_clean_contact_number_with_plus(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {"contact_number": "+15551234"}
        contact_number = form.clean_contact_number()
        self.assertEqual(contact_number, "+15551234")

    def test_clean_contact_number_without_plus(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {"contact_number": "15551234"}
        with self.assertRaises(ValidationError):
            form.clean_contact_number()

    def test_clean_with_both_roles(self):
        form = CustomRegistrationForm()
        form.cleaned_data = {"is_hotel_manager": True, "is_client_user": True}
        with self.assertRaises(ValidationError):
            form.clean()


os.environ["DJANGO_SETTINGS_MODULE"] = "hotels_booking.settings"


django.setup()


class TestCustomUser(unittest.TestCase):
    def setUp(self):
        # Create any initial data or setup required for the tests
        pass

    def tearDown(self):
        # Clean up any data or resources created during the tests
        CustomUser.objects.all().delete()

    def test_custom_user_saved_with_valid_data(self):
        user = CustomUser(
            username="test1", email="test1@example.com", password="password123"
        )
        user.save()
        self.assertIsNotNone(user.id)

    def test_custom_user_raises_error_with_invalid_data(self):
        user = CustomUser(username="")
        # Empty username to trigger
        # the validation error
        with self.assertRaises(ValidationError):
            user.full_clean()  # Validate the user without saving

    def test_generate_reset_token(self):
        user = CustomUser(
            username="test2", email="test2@example.com", password="password123"
        )
        user.save()
        token = user.generate_reset_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    def test_fields(self):
        user = CustomUser(
            username="test3", email="test3@example.com", password="password123"
        )
        user.save()
        self.assertEqual(user.username, "test3")

