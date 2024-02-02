import logging

# Standard library imports
from urllib.parse import quote 

# Django imports
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError, transaction
from django.db.models import Sum, Avg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError, transaction
# Local app imports 
from .forms import (
    # CommentForm, 
    CustomRegistrationForm, 
    HotelForm, 
    # ModifyBookingForm, 
    # RatingForm, 
    # YourBookingForm
    )
from .models import (
    Amenity, 
    # Booking, 
    # Comment, 
    CustomUser, 
    Hotel, 
    Photo, 
    # Rating, 
    # UserActivity
    )
                     
# Third party imports
import xlsxwriter



import logging

logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Check if a user with the provided username or email already exists
            if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
                # Add error message for existing user
                messages.error(request, "User with this username or email already exists. Please choose a different one.")
            else:
                # Save the user if it's a new user
                user = form.save(commit=True)
                # Add success message for successful registration
                messages.success(request, f"Welcome, {user.username}! You are now registered.")
                
                logger.info(f"User {user.username} successfully registered.")
                
                # Redirect to the appropriate page after successful registration
                return redirect('hotel_your_choice:login')
        else:
            # Add error message for invalid form data
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CustomRegistrationForm()

    return render(request, 'hotel_your_choice/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # If the form is valid, get the authenticated user
            user = form.get_user()
            # Log in the user
            login(request, user)
            # Add a success message
            messages.success(request, f"Welcome, {user.username}!")
            # Redirect to the desired page
            return redirect('hotel_your_choice:view_hotels')
        else:
            # If the form is not valid, display an error message
            messages.error(request, "Login failed. Please check your credentials.")
            # Render the login form template with the form (including errors)
            return render(request, 'hotel_your_choice/login.html', {'form': form})
    else:
        # If the request method is GET, create a new instance of AuthenticationForm
        form = AuthenticationForm()

    # Render the login form template with the form
    return render(request, 'hotel_your_choice/login.html', {'form': form})

def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the desired page
    return redirect('hotel_your_choice:view_hotels')



class CustomPasswordResetView(View):
    template_name = 'hotel_your_choice/password_reset.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            # Retrieve the user by username
            user = get_user_model().objects.get(username=username)

            if user:
                # Allow the user to reset their password
                user.set_password(new_password)
                user.save()

                return redirect('login')  # Redirect to your login page

        except get_user_model().DoesNotExist:
            pass  # Handle the case where the user does not exist

        return render(request, self.template_name)
    
class CustomPasswordResetConfirmView(View):
    template_name = 'hotel_your_choice/password_reset_confirm.html'  # Create this template

    def get(self, request, email, token):
        context = {'email': email, 'token': token}
        return render(request, self.template_name, context)

    def post(self, request, email, token):
        try:
            # Verify the token against the stored token
            user = get_user_model().objects.get(email=email, reset_token=token)

            if user:
                # Allow the user to reset their password
                new_password = request.POST.get('new_password')
                user.set_password(new_password)
                user.reset_token = None  # Clear the reset token after resetting the password
                user.save()

                messages.success(request, 'Password reset successfully.')
                return redirect('login')  # Redirect to your login page

        except get_user_model().DoesNotExist:
            pass  # Handle the case where the user or token does not exist

        messages.error(request, 'Invalid email or token.')
        return render(request, self.template_name, {'email': email, 'token': token})
        

@login_required
def unsubscribe_view(request):
    if request.method == 'POST':
        user = request.user

        # Implement logic for user unsubscribe
        # For example, set a flag in the user's profile indicating unsubscribed status
        # Replace 'is_subscribed' with the field that indicates the subscription status in your User model
        User = get_user_model()

        try:
            user_profile = User.objects.get(pk=user.pk)
            user_profile.is_subscribed = False  # Set the flag to indicate unsubscribed status
            user_profile.save()

            # Log the user out
            logout(request)

            # Remove the user from the user database
            user_profile.delete()

            # Display a success message
            messages.success(request, 'You have been unsubscribed successfully.')

            # Redirect to the home page or any other desired page after successful unsubscribe and logout
            return redirect('hotel_your_choice:view_hotels')

        except User.DoesNotExist:
            # Handle the case where the user doesn't exist (optional)
            messages.error(request, 'User not found.')
    return render(request, 'hotel_your_choice/unsubscribe.html')


# Common pages Views

def view_hotels(request):
 
    return render(request, 'hotel_your_choice/common/view_hotels.html', context={})


# Hotel Manager views 

@login_required
def hotel_manager_dashboard(request):
    hotels_managed = Hotel.objects.filter(manager=request.user)

    if hotels_managed.exists():
        bookings = Booking.objects.filter(hotel__in=hotels_managed)
    else:
        bookings = []

    return render(request, 'hotel_your_choice/hotel_manager/dashboard.html', {'bookings': bookings})

@login_required
def handle_amenities(hotel_instance, amenity_ids):
    print("Handling Amenities...")
    
    # Clear existing amenities
    hotel_instance.amenities = ''

    # Iterate through amenity_ids and append them to the amenities field
    amenities = Amenity.objects.filter(id__in=amenity_ids)
    amenity_names = ', '.join(amenity.name for amenity in amenities)
    hotel_instance.amenities = amenity_names
    hotel_instance.save()

    print(f"Amenities updated: {hotel_instance.amenities}")

def handle_other_photos(hotel_instance, other_photos):
    print("Handling Other Photos...")

    hotel_instance.other_photos.clear()  # Clear existing photos

    for photo in other_photos:
        try:
            # Create a new Photo instance and link it to the current Hotel instance
            photo_instance = Photo.objects.create(image=photo, hotel=hotel_instance)
            hotel_instance.other_photos.add(photo_instance)
        except Exception as e:
            print(f'Error uploading photo: {e}')

    hotel_instance.save()

    print(f"Other Photos updated: {hotel_instance.other_photos.all()}")



@login_required
def add_hotel(request):
    if request.method == 'POST':
        hotel_form = HotelForm(request.POST, request.FILES)
        if hotel_form.is_valid():
            try:
                with transaction.atomic():
                    # Process the form data and save the hotel instance
                    hotel_instance = hotel_form.save(commit=False)
                    hotel_instance.manager = request.user
                    hotel_instance.save()

                    # Handle other photos within the transaction
                    try:
                        handle_other_photos(hotel_instance, request.FILES.getlist('other_photos'))
                    except Exception as e:
                        # Handle any exceptions related to other photos but continue with the transaction
                        print(f'Error handling other photos: {e}')
                    
                    # Commit the transaction
                    messages.success(request, 'Hotel added successfully!')
                    return redirect('hotel_your_choice:view_hotels')
            except Exception as e:
                # Handle any exceptions that occur during the transaction
                messages.error(request, f'Error adding hotel: {e}')
        else:
            # Handle form validation errors
            print("Form errors:", hotel_form.errors)
            messages.error(request, 'Error adding hotel. Please check the form.')
    else:
        hotel_form = HotelForm()

    amenities = Amenity.objects.all()
    return render(request, 'hotel_your_choice/hotel_manager/add_hotel.html', {'hotel_form': hotel_form, 'amenities': amenities})

@login_required
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.user == hotel.manager:
        hotel.delete()
        messages.success(request, 'Hotel deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this hotel.')
    return redirect('hotel_your_choice:view_hotels')



@login_required
def edit_hotel(request, hotel_id):
    hotel_instance = get_object_or_404(Hotel, id=hotel_id)

    # Check if the logged-in user is the manager of the hotel
    if request.user != hotel_instance.manager:
        messages.error(request, 'You do not have permission to edit this hotel.')
        return redirect('hotel_your_choice:view_hotels')

    if request.method == 'POST':
        hotel_form = HotelForm(request.POST, request.FILES, instance=hotel_instance)
        if hotel_form.is_valid():
            try:
                with transaction.atomic():
                    hotel_instance = hotel_form.save()

                    # Handle amenities (unchanged)
                    amenities_str = request.POST.get('amenities', '')  # Get comma-separated string of amenities
                    amenities_list = [amenity.strip() for amenity in amenities_str.split(',')]  # Split string into list
                    hotel_instance.amenities = ', '.join(amenities_list)  # Join list back into comma-separated string

                    # Save the updated hotel instance
                    hotel_instance.save()

                    # Handle other photos
                    handle_other_photos(hotel_instance, request.FILES.getlist('other_photos'))

                    messages.success(request, 'Hotel edited successfully!')
                    return redirect('hotel_your_choice:view_hotels')
            except Exception as e:
                # Handle any exceptions that occur during the transaction
                messages.error(request, f'Error editing hotel: {e}')
        else:
            messages.error(request, 'Error editing hotel. Please check the form.')
    else:
        hotel_form = HotelForm(instance=hotel_instance)

    return render(
        request,
        'hotel_your_choice/hotel_manager/edit_hotel.html',
        {'hotel_form': hotel_form, 'hotel': hotel_instance}
    )


@login_required
def manage_bookings(request, booking_id=None):
    # Get all bookings for the hotels managed by the user
    bookings = Booking.objects.filter(hotel__manager=request.user)

    # Add sorting and filtering logic based on user input (you can customize this)
    sort_by = request.GET.get('sort_by', 'check_in_date')
    status_filter = request.GET.get('status_filter', 'all')

    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)

    bookings = bookings.order_by(sort_by)

    # Pagination logic (you can adjust the number per page)
    page = request.GET.get('page', 1)
    items_per_page = 10  # Adjust as needed
    paginator = Paginator(bookings, items_per_page)

    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        bookings = paginator.page(1)
    except EmptyPage:
        bookings = paginator.page(paginator.num_pages)

    # Additional features
    if request.method == 'POST':
        # Handle form submissions for modifying bookings
        modify_form = ModifyBookingForm(request.POST)
        if modify_form.is_valid():
            # Process the modification and save the changes
            booking_id = modify_form.cleaned_data['booking_id']
            modified_booking = get_object_or_404(Booking, id=booking_id)
            # Update booking details based on the form data
            # Modify the code below based on your form and model structure
            # Example: modified_booking.status = modify_form.cleaned_data['new_status']
            modified_booking.save()

            # Redirect to the Manage Bookings page after modification
            return HttpResponseRedirect(request.path_info)
    else:
        modify_form = ModifyBookingForm()

    # View Booking Details logic
    if booking_id:
        selected_booking = get_object_or_404(Booking, id=booking_id)
        return render(request, 'hotel_your_choice/hotel_manager/view_booking_details.html', {'selected_booking': selected_booking})

    return render(request, 'hotel_your_choice/hotel_manager/manage_bookings.html', {
        'bookings': bookings,
        'modify_form': modify_form,
    })


def generate_excel(request):
    # Fetch all bookings or filter based on your requirements
    bookings = Booking.objects.all()

    # Create a BytesIO buffer to store the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bookings.xlsx'

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Write the header row.
    header_format = workbook.add_format({'bold': True})
    headers = ['ID', 'Check-in Date', 'Check-out Date', 'Status', 'Guests', 'User ID', 'Username', 'Email', 'Hotel Name']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Define a date format
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    # Write the booking data.
    for row_num, booking in enumerate(bookings, start=1):
        worksheet.write(row_num, 0, booking.id)
        worksheet.write(row_num, 1, booking.check_in_date, date_format)
        worksheet.write(row_num, 2, booking.check_out_date, date_format)
        worksheet.write(row_num, 3, booking.status)
        worksheet.write(row_num, 4, booking.guests)
        worksheet.write(row_num, 5, booking.user.id)
        worksheet.write(row_num, 6, booking.user.username)
        worksheet.write(row_num, 7, booking.user.email)

        # Include hotel name if available
        if hasattr(booking, 'hotel') and booking.hotel:
            worksheet.write(row_num, 8, booking.hotel.name)
        else:
            worksheet.write(row_num, 8, 'N/A')

    workbook.close()

    return response


def view_booking_details(request, booking_id):
    # Fetch the selected booking
    selected_booking = get_object_or_404(Booking, id=booking_id)

    # Render the template with the booking details
    return render(request, 'hotel_your_choice/hotel_manager/view_booking_details.html', {'selected_booking': selected_booking})

