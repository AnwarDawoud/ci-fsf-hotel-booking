from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel_your_choice'

    # Check the ready() method for any unwanted setup
    def ready(self):
        pass  # or add your custom logic