import os
import dj_database_url
from dotenv import load_dotenv
from django.db import models
from pathlib import Path
from decouple import config

import logging

# Load environment variables from .env file
load_dotenv()

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent


# Secret key for Django application
SECRET_KEY = os.getenv('SECRET_KEY')

# Directory where Django will look for templates
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# Determine if running on Heroku based on environment variable
ON_HEROKU = os.getenv('ON_HEROKU', default='False').lower() == 'true'

# Set DEBUG to False if running on Heroku
if ON_HEROKU:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = [
    'ci-fsf-hotel-booking-ae5af0acfb8b.herokuapp.com',
    'localhost',
    '127.0.0.1',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',  # Keep only one entry for contenttypes
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'hotel_your_choice.apps.YourAppConfig',  # Your custom app
    'django.contrib.auth',  # Make sure this comes after your custom app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotels_booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Updated directory path
            # Add other directories if needed
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database configuration
if ON_HEROKU:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES = {'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))}
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Static files configuration
# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Change this line
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
CLOUDINARY = {
    'cloud_name': config('CLOUDINARY_CLOUD_NAME'),
    'api_key': config('CLOUDINARY_API_KEY'),
    'api_secret': config('CLOUDINARY_API_SECRET'),
    'secure': True  # Ensure HTTPS URLs
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


        
LOGIN_URL = 'login'
AUTH_USER_MODEL = 'hotel_your_choice.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Define the directory for log files
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGGING_DIR, exist_ok=True)

# Configure logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'django_db.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'hotel_your_choice': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
}



SESSION_COOKIE_SAMESITE = 'None'

SESSION_COOKIE_SECURE = True