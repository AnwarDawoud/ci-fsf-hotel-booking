import os
import django
import unittest

from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from django.forms import ValidationError
from hotel_your_choice.forms import CustomRegistrationForm, YourBookingForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Hotel, Booking, Amenity, Photo, Rating
from django.contrib.auth import get_user_model

os.environ["DJANGO_SETTINGS_MODULE"] = "hotels_booking.settings"
django.setup()


class HotelYourChoiceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            is_hotel_manager=True,
        )

        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test address",
            night_rate=100.0,
            capacity=10,
            room_number=5,
            main_photo="path/to/main_photo.jpg",
            manager=self.user,
        )

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

    def test_check_in_date_in_future(self):
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
        expected_check_out_date = self.booking.check_in_date + timedelta(days=5)
        self.assertEqual(self.booking.check_out_date, expected_check_out_date)

    def test_booking_guests_count(self):
        self.assertEqual(self.booking.guests, 2)

    def test_booking_status_active(self):
        self.assertEqual(self.booking.status, "active")

    def test_invalid_guests_count(self):
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                hotel=self.hotel,
                check_in_date=datetime.now().date(),
                check_out_date=datetime.now().date() + timedelta(days=5),
                guests=-1,
                status="active",
            )

    def test_booking_status_cancelled(self):
        new_booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            check_in_date=datetime.now().date(),
            check_out_date=datetime.now().date() + timedelta(days=5),
            guests=2,
            status="active",
        )

        new_booking.cancel()
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


class TestCustomUser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_custom_user_saved_with_valid_data(self):
        user = CustomUser(
            username="test1", email="test1@example.com", password="password123"
        )
        user.save()
        self.assertIsNotNone(user.id)

    def test_custom_user_raises_error_with_invalid_data(self):
        user = CustomUser(username="")
        with self.assertRaises(ValidationError):
            user.full_clean()

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


class HotelModelTestCase(TestCase):
    def setUp(self):
        self.manager = get_user_model().objects.create_user(
            username="hotelmanager",
            email="manager@example.com",
            password="HOTmanager123",
        )

    def test_hotel_creation(self):
        hotel = Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test address",
            night_rate=100.0,
            capacity=10,
            room_number=5,
            main_photo="test_main_photo.jpg",
            manager=self.manager,
        )


class AmenityModelTestCase(TestCase):
    def setUp(self):
        self.amenity = Amenity.objects.create(name="Wi-Fi")

    def test_amenity_creation(self):
        self.assertEqual(self.amenity.name, "Wi-Fi")


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="test@example.com")

    def test_user_creation(self):
        self.assertEqual(str(self.user), "testuser")
        self.assertEqual(self.user.email, "test@example.com")


class CustomRegistrationFormTestCase(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = CustomRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        form_data = {
            "username": "",
            "email": "invalid_email",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = CustomRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class YourBookingFormTestCase(TestCase):
    def test_valid_booking_form(self):
        form_data = {"check_in_date": "2024-02-10", "check_out_date": "2024-02-15", "guests": 2}
        form = YourBookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_booking_form(self):
        form_data = {"check_in_date": "2024-02-15", "check_out_date": "2024-02-10", "guests": -1}
        form = YourBookingForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterViewTestCase(TestCase):
    def test_register_new_user(self):
        url = reverse("hotel_your_choice:register")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="testuser").exists())


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test_user", email="test@example.com", password="password123"
        )

    def test_logout_logged_in_user(self):
        self.client.login(username="test_user", password="password123")
        url = reverse("hotel_your_choice:logout")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_no_user_logged_in(self):
        url = reverse("hotel_your_choice:logout")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/"))
        self.assertNotIn("_auth_user_id", self.client.session)


class BookingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_booking_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("hotel_your_choice:book_hotel", kwargs={"hotel_id": 1, "hotel_name": "test-hotel"}))
        self.assertEqual(response.status_code, 200)

    def test_create_booking(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("hotel_your_choice:book_hotel", kwargs={"hotel_id": 1, "hotel_name": "test-hotel"}), {"booking_data": "data"}, follow=True)
        self.assertEqual(response.status_code, 200)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_login_with_valid_credentials(self):
        url = reverse("hotel_your_choice:login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/"))
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_with_invalid_credentials(self):
        url = reverse("hotel_your_choice:login")
        data = {"username": "testuser", "password": "invalidpassword"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_access_login_page(self):
        url = reverse("hotel_your_choice:login")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_register_existing_user(self):
        existing_user = self.User.objects.create_user(
            "existinguser", "existinguser@example.com", "existingpassword"
        )

        url = reverse("hotel_your_choice:register")
        data = {
            "username": "existinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(username="testuser").exists())

    def test_register_invalid_data(self):
        url = reverse("hotel_your_choice:register")
        data = {
            "username": "",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username="").exists())


if __name__ == "__main__":
    unittest.main()
