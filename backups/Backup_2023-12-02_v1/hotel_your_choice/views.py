# hotel_your_choice/views.py

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from .models import Hotel, Booking, CustomUser
from .forms import YourBookingForm, CustomRegistrationForm, HotelForm
import logging
from django.contrib.auth import login, logout

logger = logging.getLogger(__name__)

# Common Views
def view_hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_your_choice/view_hotels.html', {'hotels': hotels})

# Hotel Manager Views
@login_required
def hotel_manager_dashboard(request):
    bookings = Booking.objects.filter(hotel__managers=request.user)
    return render(request, 'hotel_your_choice/hotel_manager/dashboard.html', {'bookings': bookings})

@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.save()
            hotel.managers.add(request.user)
            messages.success(request, "Hotel added/updated successfully.")
            return redirect('hotel_your_choice:hotel_manager_dashboard')
    else:
        form = HotelForm()

    return render(request, 'hotel_your_choice/hotel_manager/add_hotel.html', {'form': form})

@login_required
def manage_bookings(request):
    bookings = Booking.objects.filter(hotel__managers=request.user)
    return render(request, 'hotel_your_choice/hotel_manager/manage_bookings.html', {'bookings': bookings})

# Client Views
@login_required
def book_hotel(request, hotel_id):
    available_hotels = Hotel.objects.all()

    if request.method == 'POST':
        form = YourBookingForm(request.POST)
        if form.is_valid():
            selected_hotel_id = form.cleaned_data['hotel'].id
            selected_hotel = get_object_or_404(Hotel, pk=selected_hotel_id)

            check_in_date = form.cleaned_data['check_in']
            check_out_date = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']

            Booking.objects.create(
                user=request.user,
                hotel=selected_hotel,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                guests=guests
            )

            messages.success(request, "Booking created successfully.")
            return redirect('hotel_your_choice:client_dashboard')
    else:
        form = YourBookingForm()

    return render(request, 'hotel_your_choice/client/book_hotel.html', {'form': form, 'available_hotels': available_hotels, 'selected_hotel_id': hotel_id})

@login_required
def client_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'hotel_your_choice/client/client_dashboard.html', {'bookings': bookings})

@login_required
def rate_experience(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        booking.rating = rating
        booking.save()

        messages.success(request, "Rating submitted successfully.")
        return redirect('hotel_your_choice:client_dashboard')

    return render(request, 'hotel_your_choice/client/rate_experience.html', {'booking': booking})

# Site Administrator Views
def get_analytics_data():
    # Replace this with your actual logic to fetch analytics data
    return {'total_bookings': 100, 'revenue': 5000, 'average_rating': 4.5}

@login_required
def system_overview(request):
    # Assuming analytics is a variable or function you want to use in this view
    analytics = get_analytics_data()  # Replace with your actual logic to get analytics data
    return render(request, 'hotel_your_choice/system_overview.html', {'analytics': analytics})

@login_required
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'hotel_your_choice/site_administrator/manage_users.html', {'users': users})

@login_required
def troubleshoot(request):
    # Implement logic for troubleshooting
    return render(request, 'hotel_your_choice/site_administrator/troubleshoot.html')

# Authentication and Authorization Views
def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, f"Welcome, {user.username}! You are now registered.")
            return redirect('hotel_your_choice:view_hotels')
        else:
            messages.error(request, "Registration failed. Please correct the errors in the form.")
    else:
        form = CustomRegistrationForm()

    return render(request, 'hotel_your_choice/authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('hotel_your_choice:view_hotels')
        else:
            messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'hotel_your_choice/authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('hotel_your_choice:view_hotels')

def password_reset_view(request):
    # Implement logic for password reset
    return render(request, 'hotel_your_choice/authentication/password_reset.html')

def unsubscribe_view(request):
    # Implement logic for user unsubscribe
    return render(request, 'hotel_your_choice/authentication/unsubscribe.html')
