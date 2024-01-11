# hotel_your_choice/tests.py

from django.test import TestCase
from .models import CustomUser, Hotel, Booking
from django.urls import reverse
from datetime import datetime, timedelta

class HotelYourChoiceTests(TestCase):
    def setUp(self):
        # Create a custom user using create_user method from CustomUser manager
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            is_hotel_manager=True,  # Adjust as needed
        )

        # Create a hotel using the custom user as the manager
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            description='Test description',
            address='Test address',
            night_rate=100.0,
            capacity=10,
            room_number=5,
            main_photo='path/to/main_photo.jpg',  # Adjust as needed
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
            status='active',
        )

    def test_hotel_model(self):
        self.assertEqual(str(self.hotel), 'Test Hotel')

    def test_booking_model(self):
        expected_str = f"{self.booking.id} - {self.user.username} - {self.hotel.name} Booking (Active)"
        self.assertEqual(str(self.booking), expected_str)

    def test_view_hotels(self):
        response = self.client.get(reverse('hotel_your_choice:view_hotels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')
