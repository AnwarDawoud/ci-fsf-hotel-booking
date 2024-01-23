
import os
from pathlib import Path
import dj_database_url
from decouple import config
from django.db import models




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 


ON_HEROKU = config('ON_HEROKU', default=False, cast=bool) 


SECRET_KEY = '9q=3tig&^s7zoq@16ir2hz-q$+af^9tqy7=v^_b&i!uf0q8$%i' # Set DEBUG based on the environment


DEBUG = not ON_HEROKU # True if local, False if on Heroku


ALLOWED_HOSTS = [
    'mysterious-tundra-89304-deptes-8a08ec3a2b87.herokuapp.com',
    '.localhost',
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
        'DIRS': [],
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
    DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}



MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
 
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

LOGIN_URL = 'login'

# Use the default Django login URL
AUTH_USER_MODEL = 'hotel_your_choice.CustomUser'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # other backends if needed
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'