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
# Local app imports 
from .forms import (
    # CommentForm, 
    CustomRegistrationForm, 
    # HotelForm, 
    # ModifyBookingForm, 
    # RatingForm, 
    # YourBookingForm
    )
from .models import (
    # Amenity, 
    # Booking, 
    # Comment, 
    CustomUser, 
    # Hotel, 
    # Photo, 
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