from django.test import TestCase
from .models import Hotel, Booking
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
# hotel_your_choice/tests.py


class HotelYourChoiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            description='A test hotel',
            address='123 Test Street'
        )
        self.booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            check_in='2023-01-01',
            check_out='2023-01-05',
            guests=2
        )

    def test_hotel_model(self):
        self.assertEqual(str(self.hotel), 'Test Hotel')

    def test_booking_model(self):
        self.assertEqual(str(self.booking),
                         'Test Hotel - 2023-01-01 to 2023-01-05')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hotel')

    # Add more tests as needed
