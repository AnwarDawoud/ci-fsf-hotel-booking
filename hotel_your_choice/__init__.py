from django.apps import AppConfig

class HotelYourChoiceConfig(AppConfig):
    name = 'hotel_your_choice'
    verbose_name = 'Hotel Your Choice'

# In the __init__.py file of the app:
default_app_config = 'hotel_your_choice.apps.HotelYourChoiceConfig'