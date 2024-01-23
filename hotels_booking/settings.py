
import os
from pathlib import Path
import dj_database_url
from decouple import config
from django.db import models




BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


ON_HEROKU = config('ON_HEROKU', default=False, cast=bool) 


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = not ON_HEROKU # True if local, False if on Heroku


ALLOWED_HOSTS = [
    'mysterious-tundra-89304-deptes.herokuapp.com',
    'localhost',
    '127.0.0.1'
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
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
 
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.jion(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_URL = 'login'

# Use the default Django login URL
AUTH_USER_MODEL = 'hotel_your_choice.CustomUser'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # other backends if needed
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'