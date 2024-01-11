# hotels_booking/hotel_your_choice/context_processors.py
def welcome_message(request):
    user_welcome = ""
    if request.user.is_authenticated:
        user_welcome = f"Welcome, {request.user.username}!"
    return {'user_welcome': user_welcome}
