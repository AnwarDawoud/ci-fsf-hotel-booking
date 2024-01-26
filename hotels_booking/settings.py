import os
import dj_database_url
from dotenv import load_dotenv
from django.db import models
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Use environment variables in your settings
DEBUG = os.getenv('DEBUG')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, '.env')
load_dotenv(config_path)

# Continue with the rest of your settings.py
SECRET_KEY = os.getenv('SECRET_KEY')

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

ON_HEROKU = os.getenv('ON_HEROKU', default='False') == 'True'

#DEBUG = not ON_HEROKU

DEBUG = True

ALLOWED_HOSTS = [
    'mysterious-tundra-89304-deptes-8a08ec3a2b87.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'django.contrib.auth',
    'multiupload',
    'hotel_your_choice.apps.YourAppConfig',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotels_booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hotel_your_choice', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]

LOGIN_URL = 'login'
AUTH_USER_MODEL = 'hotel_your_choice.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
