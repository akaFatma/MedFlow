import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = '280919'  # Replace this with your actual secret key

# Debug Settings
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = []

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'corsheaders',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'med',  # Ajouter cette ligne pour ton application 'med'
]


# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Placez ceci en premier
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# URL Configuration
ROOT_URLCONF = 'projetigl.urls'  # Replace 'med' with your project name

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Define your templates directory
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

# WSGI Application
  # Replace 'med' with your project name
WSGI_APPLICATION = 'projetigl.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdd',  # Replace with your MySQL database name
        'USER': 'root',                # Your username
        'PASSWORD': '280919',          # Your password
        'HOST': 'localhost',           # Database host
        'PORT': '3306',                # Default MySQL port
    }
}


AUTH_USER_MODEL = 'med.CustomUser'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Define your static files directory

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
