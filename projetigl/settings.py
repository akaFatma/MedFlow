import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key
SECRET_KEY = '280919'  # Remplacez ceci par votre clé secrète réelle

# Debug Settings
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = ['*']  # Changez '*' par un domaine spécifique si nécessaire, ou laissez '*' pour tout accepter

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'corsheaders',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'med',  # Application personnalisée
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Cela doit être mis en premier
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = False  # Mettez False pour restreindre les origines
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # URL de votre frontend Angular
]
CORS_ALLOW_CREDENTIALS = True  # Permet d'envoyer des cookies avec les requêtes

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',  # Ajoutez l'URL de votre frontend ici
]

# URL Configuration
ROOT_URLCONF = 'projetigl.urls'  # Remplacez 'projetigl' par le nom de votre projet

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Votre répertoire de templates
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
WSGI_APPLICATION = 'projetigl.wsgi.application'  # Remplacez 'projetigl' par le nom de votre projet

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdd',  # Votre base de données MySQL
        'USER': 'root',  # Votre nom d'utilisateur
        'PASSWORD': '280919',  # Votre mot de passe
        'HOST': 'localhost',  # Hôte de la base de données
        'PORT': '3306',  # Port MySQL par défaut
    }
}

# Custom User Model
AUTH_USER_MODEL = 'med.CustomUser'

# Session and Cookie Settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = False  # Mettez True lorsque vous utilisez HTTPS en production

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
STATICFILES_DIRS = [BASE_DIR / 'static']  # Votre répertoire de fichiers statiques

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media Files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Répertoire de fichiers médias

